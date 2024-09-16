"use strict";

sap.ui.define([], function () {
  "use strict";

  /**
   *
   * Checks if a date fits in all ranges.
   * Todo better documentation
   * @param {{start_date: Date, end_date: Date}} date
   * @param {{start_date: Date, end_date: Date}[]} slots
   */
  function dateFitsInAllRanges(date, ranges) {
    ranges.push(range(dateToTimeStamp(date.start_date), dateToTimeStamp(date.end_date)));
    const expectedLength = dateToTimeStamp(date.end_date) - dateToTimeStamp(date.start_date);
    const checkLength = overlapOfSets(ranges).size;
    return checkLength === expectedLength;
  }

  /**
   * Checks if a date fits in all slots
   * Todo better documentation
   * @param {{start_date: Date, end_date: Date}} date
   * @param {{start_date: Date, end_date: Date}[]} slots
   */
  function dateFitsInAllSlots(date, slots) {
    const toCheck = [date, ...slots];
    const expectedLength = dateToTimeStamp(date.end_date) - dateToTimeStamp(date.start_date);
    const checkLength = overlapOfSlots(toCheck).size;
    return checkLength === expectedLength;
  }

  /**
   * Returns true if the appointments' participants are available for the duration of the
   * appointment.
   * @param {Appointment} appointment The appointment to check
   * @param {Slot[]} allSlots All slots of all users in the relevant time frame
   */
  function dateFitsInSlots(appointment, allSlots) {
    const slots = [];
    for (const participant of appointment.participants) {
      const slotsOfUser = allSlots.filter(slot => slot.person === participant && !(slot.end_date.getTime() <= appointment.start_date.getTime()) && !(slot.start_date.getTime() >= appointment.end_date.getTime()));
      const rangesOfUser = getRanges(slotsOfUser);
      slots.push(rangesOfUser);
    }
    return dateFitsInAllRanges(appointment, slots);
  }

  /**
   * Returns a the date object with the minutes and seconds
   * set to the nearest 5 minute interval.
   * Changes the original date object.
   * @param {Date} date
   * @returns {Date}
   */
  function dateToFiveMinutes(date) {
    date.setMinutes(date.getMinutes() - date.getMinutes() % 5);
    date.setSeconds(0);
    date.setMilliseconds(0);
    return date;
  }
  function dateToNextMonday(date) {
    const day = date.getDay();
    if (day !== 1) {
      const diff = day === 0 ? 1 : 8 - day;
      date.setDate(date.getDate() + diff);
    }
    return date;
  }
  function dateToPreviousMonday(date) {
    const day = date.getDay();
    if (day !== 1) {
      const diff = day === 0 ? 6 : day - 1;
      date.setDate(date.getDate() - diff);
    }
    return date;
  }
  function dateToPreviousSunday(date) {
    const day = date.getDay();
    if (day !== 0) {
      date.setDate(date.getDate() - day);
    }
    return date;
  }

  /**
   * Returns the timestamp in 5 minute intervals that
   * passed since 1970-01-01 00:00:00 UTC. Example:
   * - d = new Date("1970-01-01 00:15:00 UTC");
   * - dateToTimeStamp(d) === 3
   * @param {Date} date
   * @returns {number}
   */
  function dateToTimeStamp(date) {
    return date.getTime() / 1000 / 60 / 5;
  }
  function findBetterStartDate(appointment, appointments, slots, earliestDate, latestDate) {
    const possibleSlots = getPossibleSlots(appointment, appointments, slots, earliestDate, latestDate);
    const preferredSlots = getPossibleSlots(appointment, appointments, slots, earliestDate, latestDate, true);
    const minLength = dateToTimeStamp(appointment.end_date) - dateToTimeStamp(appointment.start_date);
    let date = findStartDate(preferredSlots, minLength, 'forward');
    if (date && date.getTime() == appointment.start_date.getTime()) {
      date = findStartDate(preferredSlots, minLength, 'backward');
    }
    if (date) {
      return date.getTime() == appointment.start_date.getTime() ? null // date remains the same
      : date; // Found a preferred slot that fits
    }
    // still null? try all slots, not only preferred ones
    date = findStartDate(possibleSlots, minLength, 'forward');
    if (date && date.getTime() == appointment.start_date.getTime()) {
      date = findStartDate(possibleSlots, minLength, 'backward');
    }
    if (date && date.getTime() == appointment.start_date.getTime()) {
      return null; // No other slot found, keep the original date
    }
    return date; // Found a different slot that fits
  }
  function findStartDate(possibleSlots, minLength, direction) {
    if (direction === 'forward') {
      let actualLength = 1; // Do not start with zero because each slot is a 5 minute interval
      const slotArray = Array.from(possibleSlots).sort();
      for (let i = 0; i <= slotArray.length - 2; i++) {
        if (slotArray[i + 1] - slotArray[i] > 1) {
          actualLength = 1;
        } else {
          actualLength += 1;
        }
        if (actualLength == minLength) {
          return new Date((slotArray[i + 1] - actualLength + 1) * 1000 * 60 * 5);
        }
      }
    } else {
      let actualLength = 1; // Do not start with zero because each slot is a 5 minute interval
      const slotArray = Array.from(possibleSlots).sort().reverse();
      for (let i = 0; i <= slotArray.length - 2; i++) {
        if (slotArray[i] - slotArray[i + 1] > 1) {
          actualLength = 1;
        } else {
          actualLength += 1;
        }
        if (actualLength == minLength) {
          return new Date(slotArray[i + 1] * 1000 * 60 * 5);
        }
      }
    }
  }

  /**
   * Returns a set of all possible slots for the given appointment.
   * Respects the following constraints:
   * - The appointment must not overlap with any other appointment of the participants
   * - The slots of the participants must fully contain the appointment
   * - Only slots in the given time frame are considered
   * - Only preferred slots are considered if onlyPreferred is true
   */
  function getPossibleSlots(appointment, allAppointments, allSlots, earliestDate, latestDate) {
    let onlyPreferred = arguments.length > 5 && arguments[5] !== undefined ? arguments[5] : false;
    const rangesOfSlots = [];
    const rangesOfAppointments = [];
    for (const participant of appointment.participants) {
      const slotsOfUser = allSlots.filter(slot => {
        return slot.person === participant && !(slot.end_date.getTime() < earliestDate.getTime()) && !(slot.start_date.getTime() > latestDate.getTime()) && (!onlyPreferred || slot.is_preferred);
      });
      const appointmentsOfUser = allAppointments.filter(iterAppointment => {
        return appointment.id !== iterAppointment.id && iterAppointment.participants.includes(participant) && !(iterAppointment.end_date.getTime() < earliestDate.getTime()) && !(iterAppointment.start_date.getTime() > latestDate.getTime());
      });
      rangesOfSlots.push(getRanges(slotsOfUser));
      rangesOfAppointments.push(getRanges(appointmentsOfUser));
    }
    if (rangesOfSlots.length === 0) {
      return null;
    }
    let slotRange = rangesOfSlots[0];
    for (let i = 1; i < rangesOfSlots.length; i++) {
      slotRange = slotRange.intersection(rangesOfSlots[i]);
    }
    for (let i = 0; i < rangesOfAppointments.length; i++) {
      slotRange = slotRange.difference(rangesOfAppointments[i]);
    }
    return slotRange;
  }

  /**
   * Returns a set with all numbers in the range [start_date_ts, end_date_ts)
   * where start_date_ts and end_date_ts are the timestamps in 5 minute intervals.
   * @param {{start_date: Date, end_date: Date}[]} slotLike
   */
  function getRanges(slotLike) {
    const result = new Set();
    for (let i = 0; i < slotLike.length; i++) {
      const start = dateToTimeStamp(slotLike[i].start_date);
      const end = dateToTimeStamp(slotLike[i].end_date);
      for (let j = start; j < end; j++) {
        result.add(j);
      }
    }
    return result;
  }

  /**
   * Returns true if any participant of the appointment to check has
   * a conflicting appointment, i.e. an appointment at the same time.
   * @param {Appointment} appointment The appointment to check
   * @param {Appointment[]} appointments All appointments of all users in the relevant time frame
   */
  function hasConflictingAppointments(appointment, appointments) {
    let numberOfConflictingAppointments = 0;
    const appointmentIds = new Set(appointment.participants);
    for (const iteratingAppointment of appointments) {
      if (overlaps(iteratingAppointment, appointment)) {
        if (new Set(iteratingAppointment.participants).intersection(appointmentIds).size >= 1) {
          numberOfConflictingAppointments += 1;
          if (numberOfConflictingAppointments > 1) {
            break;
          }
        }
      }
    }
    return numberOfConflictingAppointments - 1 > 0;
  }

  /**
   * Intersection of slots in 5-Minute intervals
   * @param {{start_date: Date, end_date: Date}[]} slots
   * @returns {Set<number>} The intersection of the slots in 5-Minute intervals
   */
  function overlapOfSets(slotSets) {
    let result = new Set(slotSets[0]);
    for (let i = 1; i < slotSets.length; i++) {
      result = result.intersection(slotSets[i]);
    }
    return result;
  }

  /**
   * Intersection of slots in 5-Minute intervals
   * @param {{start_date: Date, end_date: Date}[]} slots
   * @returns {Set<number>} The intersection of the slots in 5-Minute intervals
   */
  function overlapOfSlots(slots) {
    if (slots.length === 0) {
      return new Set();
    }
    const slotSets = slots.map(slot => {
      const start = dateToTimeStamp(slot.start_date);
      const end = dateToTimeStamp(slot.end_date);
      return range(start, end);
    });
    let result = new Set(slotSets[0]);
    for (let i = 1; i < slotSets.length; i++) {
      result = result.intersection(slotSets[i]);
    }
    return result;
  }

  /**
   * Returns true if the two appointments overlap.
   * @param {Appointment} A - The appointment to check
   * @param {Appointment} B - The appointment to check
   * @returns {boolean}
   */
  function overlaps(A, B) {
    const aStart = A.start_date.getTime();
    const aEnd = A.end_date.getTime();
    const bStart = B.start_date.getTime();
    const bEnd = B.end_date.getTime();
    if (aStart == bEnd) {
      return false;
    } else if (bStart == aEnd) {
      return false;
    } else if (aStart < bStart && aEnd > bEnd) {
      return true;
    } else if (bStart < aStart && bEnd > aEnd) {
      return true;
    } else {
      return aStart <= bEnd && bEnd <= aEnd || aStart <= bStart && bStart <= aEnd;
    }
  }

  /**
   * Set with all numbers in the range [start, stop)
   * @param {number} start
   * @param {number} stop
   * @returns {Set<number>}
   */
  function range(start, stop) {
    const result = new Set();
    for (let i = start; i < stop; i++) {
      result.add(i);
    }
    return result;
  }
  var __exports = {
    __esModule: true
  };
  __exports.dateFitsInAllRanges = dateFitsInAllRanges;
  __exports.dateFitsInAllSlots = dateFitsInAllSlots;
  __exports.dateFitsInSlots = dateFitsInSlots;
  __exports.dateToFiveMinutes = dateToFiveMinutes;
  __exports.dateToNextMonday = dateToNextMonday;
  __exports.dateToPreviousMonday = dateToPreviousMonday;
  __exports.dateToPreviousSunday = dateToPreviousSunday;
  __exports.findBetterStartDate = findBetterStartDate;
  __exports.getRanges = getRanges;
  __exports.hasConflictingAppointments = hasConflictingAppointments;
  __exports.overlapOfSets = overlapOfSets;
  return __exports;
});
//# sourceMappingURL=Time-dbg.js.map

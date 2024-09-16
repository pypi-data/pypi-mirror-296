"use strict";

sap.ui.define(["./Random"], function (__Random) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const Random = _interopRequireDefault(__Random);
  /**
   * Mock data provider for generating random persons.
   * @namespace demo.spa.controller.utils
   */
  class MockDataProvider {
    MAX_ID = (() => 2 ** 64 - 1)();
    appointmentTitles = ['Meeting', 'Coffee Corner', 'Training', 'Workshop', 'Interview', 'Presentation', 'Conference', 'Tech Talk'];
    firstNames = 'James Olivia Liam Emma Noah Ava Isabella Sophia Mia Jackson Aiden Lucas Sophia Ethan Mia Madison Alexander Henry Amelia Charlotte Michael Benjamin Elijah Grace Ella Carter Chloe Lily Oliver Aria Emily Samuel Jack Abigail Harper Evelyn Daniel Max Avery Mason Scarlett Victoria Logan Eleanor Landon Matthew Mila Ella Hannah David Leo Sofia Asher Nora Riley Zoe Lily Aubrey Grayson Ellie Emma Levi Zoe Aurora Lucy Grace Amelia Liam Harper Ezra Aria Chloe Abigail Sofia Charlotte Owen Ella Sebastian Luna Caleb Avery Stella Scarlett Hudson Evelyn Eli Aria Nathan Addison John Anna Robert Lily Jaxon Layla Camila Elliot Kai Eva'.split(' ');
    frame = 7;
    // day x +/- 7 days
    generatedPersons = (() => [])();
    generatedSlots = (() => [])();
    lastNames = 'Smith Johnson Williams Jones Brown Davis Miller Wilson Moore Taylor Anderson Thomas Jackson White Harris Martin Thompson Garcia Martinez Robinson Clark Rodriguez Lewis Lee Walker Hall Allen Young Hernandez King Wright Lopez Hill Scott Green Adams Baker Gonzalez Nelson Carter Mitchell Perez Roberts Turner Phillips Campbell Parker Evans Edwards Collins Stewart Sanchez Morris Rogers Reed Cook Morgan Bell Murphy Bailey Rivera Cooper Richardson Cox Howard Ward Torres Peterson Gray Ramirez James Watson Brooks Kelly Sanders Price Bennett Wood Barnes Ross Henderson Coleman Jenkins Perry Powell Long Patterson Hughes Flores Washington'.split(' ');
    numberOfAppointments = 25;
    numberOfPersons = 5;
    numberOfSlots = 125;
    rnd = (() => new Random(0))();
    constructor() {
      this.generatedPersons = this.generateRandomPersons();
    }

    /**
     * Generate a random appointment.
     * @returns Random appointment
     */
    generateRandomAppointment() {
      const [randomStartDate, randomEndDate] = this.generateTimeWindow(1, 2);
      const participants = [];
      for (let i = 0; i < this.rnd.randIntBetween(Math.min(1, this.numberOfAppointments), this.numberOfPersons - 1); i++) {
        const person = this.rnd.randomChoice(this.generatedPersons);
        if (!participants.includes(person.id)) {
          participants.push(person.id);
        }
      }
      return {
        _type: 'appointment',
        participants: participants,
        id: this.generateRandomId(),
        title: this.appointmentTitles[this.rnd.randIntBetween(0, this.appointmentTitles.length - 1)],
        start_date: randomStartDate,
        end_date: randomEndDate
      };
    }

    /**
     * Generates a list of random appointments.
     * @param count How many appointments to generate
     * @returns
     */
    generateRandomAppointments() {
      const appointmentsToCreate = [];
      for (let i = 0; i < this.numberOfAppointments; i++) {
        appointmentsToCreate.push(this.generateRandomAppointment());
      }
      return appointmentsToCreate;
    }

    /**
     * Generates a random ID which is a base 36 encoded integer
     * with 13 characters including leading zeros.
     */
    generateRandomId() {
      return this.rnd.randIntBetween(0, this.MAX_ID).toString(36).padStart(13, '0');
    }

    /**
     * Generate a random person.
     * @returns Random person
     */
    generateRandomPerson() {
      const personToCreate = {
        _type: 'person',
        email: '',
        first_name: this.getRandomFirstName(),
        id: this.generateRandomId(),
        key: this.generateRandomId(),
        last_name: this.getRandomLastName(),
        related_user: this.generateRandomId()
      };
      personToCreate.email = personToCreate.first_name.toLowerCase() + personToCreate.last_name.toLowerCase() + '@example.com';
      return personToCreate;
    }

    /**
     * Generate a list of random persons.
     * @returns List of random persons
     */
    generateRandomPersons() {
      if (this.generatedPersons.length > 0) {
        return this.generatedPersons;
      }
      const personsToCreate = [];
      for (let i = 0; i < this.numberOfPersons; i++) {
        personsToCreate.push(this.generateRandomPerson());
      }
      this.generatedPersons = personsToCreate;
      return personsToCreate;
    }

    /**
     * Generate a random slot.
     * @returns Random slot
     */
    generateRandomSlot() {
      const [randomStartDate, randomEndDate] = this.generateTimeWindow(3, 6);
      return {
        _type: 'slot',
        id: String(this.rnd.randIntBetween(100000, 999999)),
        person: this.rnd.randomChoice(this.generatedPersons).id,
        start_date: randomStartDate,
        end_date: randomEndDate,
        is_preferred: this.rnd.randIntBetween(0, 100) < 50
      };
    }
    generateRandomSlots() {
      this.generatedSlots = [];
      while (this.generatedSlots.length < this.numberOfSlots) {
        const slot = this.generateRandomSlot();
        if (this.validateSlot(slot)) {
          this.generatedSlots.push(slot);
        }
      }
      return this.generatedSlots;
    }
    generateTimeWindow(minDuration, maxDuration) {
      const randomStartDate = new Date();
      let randomEndDate;
      do {
        const time = this.rnd.randIntBetween(8, 17);
        randomStartDate.setDate(randomStartDate.getDate() + this.rnd.randIntBetween(-this.frame, this.frame));
        randomStartDate.setMinutes(this.rnd.randIntBetween(0, 1) * 30);
        randomStartDate.setSeconds(0);
        randomStartDate.setMilliseconds(0);
        randomStartDate.setHours(time);
        randomEndDate = new Date(randomStartDate);
        const offsetHour = this.rnd.randIntBetween(minDuration, maxDuration);
        const offsetMinute = this.rnd.randIntBetween(0, 1) * 30;
        randomEndDate.setHours(time + offsetHour, offsetMinute);
      } while ([0, 6].includes(randomStartDate.getDay())); // [0, 6] are Sunday and Saturday
      return [randomStartDate, randomEndDate];
    }

    /**
     * Get a random first name from the list of first names.
     */
    getRandomFirstName() {
      const randomIndex = this.rnd.randIntBetween(0, this.firstNames.length - 1);
      return this.firstNames[randomIndex];
    }

    /**
     * Get a random last name from the list of last names.
     */
    getRandomLastName() {
      const randomIndex = this.rnd.randIntBetween(0, this.lastNames.length - 1);
      return this.lastNames[randomIndex];
    }
    validateSlot(slot) {
      //  checks if the slots' start date and end date are not
      //  between start and end date of another slot:
      const slots = this.generatedSlots.filter(s => s.id !== slot.id && s.person === slot.person);
      for (const s of slots) {
        if (slot.start_date >= s.start_date && slot.start_date < s.end_date || slot.end_date > s.start_date && slot.end_date <= s.end_date || slot.start_date <= s.start_date && slot.end_date >= s.end_date) {
          return false;
        }
      }
      return true;
    }
  }
  return MockDataProvider;
});
//# sourceMappingURL=MockDataProvider-dbg.js.map

"use strict";

sap.ui.define(["sap/ui/Device", "./Time"], function (Device, ___Time) {
  "use strict";

  const dateToFiveMinutes = ___Time["dateToFiveMinutes"];
  /**
   * Applies the offset of the current timezone to the given date
   */
  function adjustDate(d) {
    let adjustment = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'subtract';
    const date = new Date(d);
    const timeZoneOffsetHours = Math.floor(date.getTimezoneOffset() / 60);
    const timeZoneOffsetMinutes = date.getTimezoneOffset() % 60;
    if (adjustment === 'add') {
      date.setHours(date.getHours() + timeZoneOffsetHours);
      date.setMinutes(date.getMinutes() + timeZoneOffsetMinutes);
    } else {
      date.setHours(date.getHours() - timeZoneOffsetHours);
      date.setMinutes(date.getMinutes() - timeZoneOffsetMinutes);
    }
    dateToFiveMinutes(date); // 12:03 -> 12:00 or 00:07 -> 00:05
    return date;
  }

  /**
   * Checks if a given object meets the ISO date-time specification.
   * If so, it returns a Date object, otherwise the object itself.
   */
  function dateTimeReviver(_, object) {
    const isoDateTimeRegex = /^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))$/;
    if (object instanceof Date) {
      return object;
    } else if (isoDateTimeRegex.test(String(object))) {
      return new Date(object);
    } else {
      return object;
    }
  }

  /**
   * Returns empty string for large Screens and the given text for small screens
   * so the overflow menu will show the text of the button.
   */
  function formatBtnTxtForSmallScreen(text) {
    return Device.resize.width < 480 ? text : '';
  }

  /**
   * Returns the error state of the email address input field.
   * @param email The email address to check.
   * @returns 'None' if the email address is valid or empty, 'Error' otherwise.
   */
  function getEmailAddressErrorState(email) {
    return isValidEmailAddress(email) || email === '' ? 'None' : 'Error';
  }

  /**
   * Checks if the given email address is valid. Uses the HTML5 input type=email validation.
   * In case the browser does not support this validation, a regular expression is used.
   */
  function isValidEmailAddress(emailAddress) {
    const input = document.createElement('input');
    input.value = emailAddress;
    input.required = true;
    input.type = 'email';
    return typeof input.checkValidity === 'function' ? input.checkValidity() : /\S+@\S+\.\S+/.test(emailAddress);
  }

  /**
   * Shortens the given string to the given length
   * @param str The string to shorten
   * @param maxLength The maximum length of the string
   * @param alternative The alternative string which will be returned if the given string is falsy
   * @returns The shortened string or the alternative string
   */
  function shortenString(str, maxLength) {
    let alternative = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : '';
    if (str) {
      const length = parseInt(maxLength);
      return str.length > length ? str.substring(0, length) + '...' : str;
    }
    return alternative;
  }

  /**
   * Trims all properties of an object that are strings in place.
   * Does not trim nested objects.
   * Example:
   *
   *  {a: '  a', b: 1} -> {a: 'a', b: 1}
   *
   * @returns The trimmed object.
   */
  function trimValuesShallow(obj) {
    for (const key in obj) {
      if (typeof obj[key] === 'string') {
        obj[key] = obj[key].trim();
      }
    }
    return obj;
  }
  var __exports = {
    __esModule: true
  };
  __exports.adjustDate = adjustDate;
  __exports.dateTimeReviver = dateTimeReviver;
  __exports.formatBtnTxtForSmallScreen = formatBtnTxtForSmallScreen;
  __exports.getEmailAddressErrorState = getEmailAddressErrorState;
  __exports.isValidEmailAddress = isValidEmailAddress;
  __exports.shortenString = shortenString;
  __exports.trimValuesShallow = trimValuesShallow;
  return __exports;
});
//# sourceMappingURL=Formatters-dbg.js.map

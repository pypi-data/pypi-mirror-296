"use strict";

sap.ui.define([], function () {
  "use strict";

  /**
   * Compare function for sorting persons by last name and first name.
   */
  function comparePersons(personOne, personTwo) {
    if (personOne.last_name === '' && personTwo.last_name !== '') {
      return 1;
    } else if (personOne.last_name !== '' && personTwo.last_name === '') {
      return -1;
    } else if (personOne.last_name === personTwo.last_name) {
      return personOne.first_name.localeCompare(personTwo.first_name);
    } else {
      return personOne.last_name.localeCompare(personTwo.last_name);
    }
  }
  var __exports = {
    __esModule: true
  };
  __exports.comparePersons = comparePersons;
  return __exports;
});
//# sourceMappingURL=Comparators-dbg.js.map

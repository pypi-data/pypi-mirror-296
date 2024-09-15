"use strict";

sap.ui.define(["sap/base/Log"], function (Log) {
  "use strict";

  /**
   * Returns true if the two objects have the same
   * JSON representation, false otherwise.
   * Note that the order of the keys in the JSON
   * representation is not considered.
   * Also note that two arrays with the same elements
   * but in different order are considered equal.
   */
  function equals(obj1, obj2) {
    return JSON.stringify(sortKeys(obj1)) === JSON.stringify(sortKeys(obj2));
  }

  /**
   * Returns the path to the resource root based on the settings in the sap-ui-bootstrap script tag
   */
  function getResourceRoot() {
    try {
      const resourceRoots = JSON.parse(document.getElementById('sap-ui-bootstrap').getAttribute('data-sap-ui-resourceroots'));
      return Object.values(resourceRoots)[0];
    } catch (error) {
      logger.error(String(error));
      logger.error('could not find resource root, please check the sap-ui-bootstrap script tag');
      return './';
    }
  }

  /**
   * Sorts the keys of the given object and its arrays
   * so that the JSON representation is the same for
   * objects with the same content.
   */
  function sortKeys(obj) {
    return Object.keys(obj).sort().reduce((acc, key) => {
      acc[key] = obj[key];
      if (Array.isArray(obj[key])) {
        acc[key] = obj[key].sort();
      }
      return acc;
    }, {});
  }
  const logger = Log.getLogger('utils/Misc');
  var __exports = {
    __esModule: true
  };
  __exports.equals = equals;
  __exports.getResourceRoot = getResourceRoot;
  __exports.sortKeys = sortKeys;
  return __exports;
});
//# sourceMappingURL=Misc-dbg.js.map

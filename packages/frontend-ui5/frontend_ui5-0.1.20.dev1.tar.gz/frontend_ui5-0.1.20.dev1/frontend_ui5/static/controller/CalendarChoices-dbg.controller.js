"use strict";

sap.ui.define(["./BaseController", "./utils/Comparators"], function (__BaseController, ___utils_Comparators) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const BaseController = _interopRequireDefault(__BaseController);
  const comparePersons = ___utils_Comparators["comparePersons"];
  /**
   * @namespace demo.spa.controller
   */
  const CalendarChoices = BaseController.extend("demo.spa.controller.CalendarChoices", {
    constructor: function constructor() {
      BaseController.prototype.constructor.apply(this, arguments);
      this.comparePersons = comparePersons;
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    onInit: function _onInit() {
      BaseController.prototype.onInit.call(this);
      this.type = this.getView().getId().includes('availability') ? 'availability' : 'appointments';
    },
    onPersonItemPress: function _onPersonItemPress(event) {
      const selectedPersonId = event.getSource().getCustomData()[0].getValue();
      if (this.type === 'appointments') {
        if (selectedPersonId === 'ALL') {
          void this.getRouter().getHashChanger().setHash(`appointments`);
        } else {
          void this.getRouter().getHashChanger().setHash(`appointments/${selectedPersonId}`);
        }
      } else {
        void this.getRouter().getHashChanger().setHash(`availability/${selectedPersonId}`);
      }
    }
  });
  return CalendarChoices;
});
//# sourceMappingURL=CalendarChoices-dbg.controller.js.map

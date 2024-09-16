"use strict";

sap.ui.define(["../controller/utils/CustomModel"], function (__CustomModel) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const CustomModel = _interopRequireDefault(__CustomModel);
  const initialUserData = {
    appointment_list: [],
    notification_list: [],
    person_list: [],
    slot_list: []
  };
  const userDataModel = new CustomModel(initialUserData);
  var __exports = {
    __esModule: true
  };
  __exports.userDataModel = userDataModel;
  return __exports;
});
//# sourceMappingURL=UserData-dbg.js.map

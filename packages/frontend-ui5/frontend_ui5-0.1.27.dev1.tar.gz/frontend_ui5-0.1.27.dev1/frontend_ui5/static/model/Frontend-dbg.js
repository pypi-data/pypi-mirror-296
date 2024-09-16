"use strict";

sap.ui.define(["sap/ui/model/json/JSONModel", "../controller/utils/Misc"], function (JSONModel, ___controller_utils_Misc) {
  "use strict";

  const getResourceRoot = ___controller_utils_Misc["getResourceRoot"];
  const initialData = {
    svgLogoPath: '',
    resourceRoot: getResourceRoot(),
    fullScreenMode: false,
    currentUser: {
      username: '',
      user_id: ''
    },
    personForm: {
      _type: 'person',
      id: null,
      first_name: '',
      last_name: '',
      email: ''
    },
    loginForm: {
      username: '',
      password: ''
    },
    signUpForm: {
      username: '',
      email: '',
      password: '',
      password_confirmation: '',
      product_key: ''
    },
    appointmentForm: {
      id: null,
      title: '',
      startTime: '',
      endTime: '',
      date: new Date().toISOString().split('T')[0],
      participants: []
    },
    appointmentTitleSuggestions: [],
    availabilityForm: {
      id: null,
      startTime: '',
      endTime: '',
      date: new Date().toISOString().split('T')[0],
      person: '',
      is_preferred: true
    },
    lastChosenPerson: null,
    filteredAppointments: [],
    filteredSlots: [],
    show24hCalendar: false,
    expandAppointmentNavListItem: true,
    expandAvailabilityNavListItem: false,
    selectedCalendarType: 'appointments',
    improveAppointmentPressed: false,
    accessCredentials: {
      username: '',
      password: ''
    }
  };
  const frontendModel = new JSONModel(initialData);
  var __exports = {
    __esModule: true
  };
  __exports.frontendModel = frontendModel;
  return __exports;
});
//# sourceMappingURL=Frontend-dbg.js.map

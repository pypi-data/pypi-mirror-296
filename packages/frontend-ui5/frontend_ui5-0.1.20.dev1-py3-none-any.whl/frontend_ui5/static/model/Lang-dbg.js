"use strict";

sap.ui.define(["sap/ui/model/json/JSONModel"], function (JSONModel) {
  "use strict";

  const languages = {
    supported: [{
      name: 'Deutsch',
      code: 'de'
    }, {
      name: 'English',
      code: 'en'
    }],
    files: ['home', 'legal']
  };
  const languageModel = new JSONModel(languages);
  var __exports = {
    __esModule: true
  };
  __exports.languageModel = languageModel;
  return __exports;
});
//# sourceMappingURL=Lang-dbg.js.map

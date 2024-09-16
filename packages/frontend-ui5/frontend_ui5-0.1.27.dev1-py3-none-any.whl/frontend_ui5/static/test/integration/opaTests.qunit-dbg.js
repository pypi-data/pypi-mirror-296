"use strict";

sap.ui.define([], function () {
  "use strict";

  function __ui5_require_async(path) {
    return new Promise(function (resolve, reject) {
      sap.ui.require([path], function (module) {
        if (!(module && module.__esModule)) {
          module = module === null || !(typeof module === "object" && path.endsWith("/library")) ? {
            default: module
          } : module;
          Object.defineProperty(module, "__esModule", {
            value: true
          });
        }
        resolve(module);
      }, function (err) {
        reject(err);
      });
    });
  }
  // https://api.qunitjs.com/config/autostart/

  QUnit.config.autostart = false;
  void Promise.all([__ui5_require_async('demo/spa/test/integration/AppJourney'), __ui5_require_async('demo/spa/test/integration/arrangements/Startup')]).then(() => {
    QUnit.config.autostart = true;
  });
});
//# sourceMappingURL=opaTests.qunit-dbg.js.map

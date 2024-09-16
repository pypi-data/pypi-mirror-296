"use strict";

sap.ui.define(["demo/spa/controller/App.controller"], function (__App) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const App = _interopRequireDefault(__App);
  QUnit.module('App.controller');
  QUnit.test('The App Controller exists', function (assert) {
    assert.ok(App, 'The app controller could be found');
  });
});
//# sourceMappingURL=App.qunit-dbg.js.map

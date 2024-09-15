"use strict";

sap.ui.define(["sap/ui/test/Opa5", "sap/ui/test/actions/Press", "./Opa5Base"], function (Opa5, Press, __Opa5Base) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const Opa5Base = _interopRequireDefault(__Opa5Base);
  class OnTheAppPage extends Opa5Base {
    appViewName = 'demo.spa.view.App';
    signInViewName = 'demo.spa.view.SignIn';
    signUpViewName = 'demo.spa.view.SignUp';
    iAssertTrueIsTrue() {
      return this.waitFor({
        success: function () {
          Opa5.assert.ok(true, 'Dummy Test');
        }
      });
    }
    iCanDestroyTheErrorMessageBox() {
      return this.waitFor({
        controlType: 'sap.m.Dialog',
        check: function (elements) {
          elements = elements.filter(elem => elem.getId().includes('error'));
          if (elements.length > 0) {
            for (const elem of elements) {
              elem.destroy();
            }
            return true;
          } else {
            return false;
          }
        },
        success: function () {
          Opa5.assert.ok(true, 'Destroyed error message box.');
        },
        errorMessage: 'No error dialog found.'
      });
    }
    iPressTheElement(btnId) {
      let viewName = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : this.appViewName;
      return this.waitFor({
        id: btnId,
        viewName: viewName,
        actions: new Press(),
        errorMessage: `Element with ID ${btnId} not found`
      });
    }
    iSetTheInputFieldToValue(id, value) {
      let viewName = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : this.appViewName;
      return this.waitFor({
        id: id,
        viewName: viewName,
        actions: function (input) {
          input.setValue(value);
        },
        errorMessage: `Input field with ID ${id} not found`,
        timeout: 2
      });
    }
    iShouldNotSeeAnErrorMessageBox() {
      return this.waitFor({
        controlType: 'sap.m.Dialog',
        check: function (elements) {
          elements = elements.filter(elem => elem.getId().includes('error'));
          if (elements.length > 0) {
            console.error(elements);
            return false;
          } else {
            return true;
          }
        },
        success: function () {
          Opa5.assert.ok(true, 'No error message box found.');
        },
        errorMessage: 'Found an error message box.'
      });
    }
    iShouldSeeAnDisabledElement(id) {
      let viewName = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : this.appViewName;
      return this.waitFor({
        id: id,
        viewName: viewName,
        success: function (element) {
          Opa5.assert.strictEqual(element.getEnabled(), false, `The element with ID ${id} is disabled`);
        },
        errorMessage: `Element with ID ${id} not found`
      });
    }
    iShouldSeeAnEnabledElement(id) {
      let viewName = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : this.appViewName;
      return this.waitFor({
        id: id,
        viewName: viewName,
        success: function (element) {
          Opa5.assert.strictEqual(element.getEnabled(), true, `The element with ID ${id} is enabled`);
        },
        errorMessage: `Element with ID ${id} not found`
      });
    }
    iShouldSeeAnErrorMessageBox() {
      return this.waitFor({
        controlType: 'sap.m.Dialog',
        check: function (elements) {
          elements = elements.filter(elem => elem.getId().includes('error'));
          if (elements.length > 0) {
            return true;
          } else {
            return false;
          }
        },
        success: function () {
          Opa5.assert.ok(true, 'Found error message box');
        },
        errorMessage: 'No error message box found.'
      });
    }
    iShouldSeeTheDialogWithId(id) {
      let viewName = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : this.appViewName;
      return this.waitFor({
        id: id,
        viewName: viewName,
        success: function (dialog) {
          Opa5.assert.ok(dialog.isOpen(), `The dialog with ID ${id} is open`);
        },
        errorMessage: `Dialog with ID ${id} not found`
      });
    }
    iShouldSeeTheUserActionSheet() {
      return this.waitFor({
        id: 'idUserActionSheet',
        viewName: this.appViewName,
        success: function (actionSheet) {
          Opa5.assert.strictEqual(actionSheet.isOpen(), true, 'The user action sheet is open');
        },
        errorMessage: 'User Action Sheet not found'
      });
    }
    theUserActionSheetShouldNotExist() {
      return this.waitFor({
        controlType: 'sap.ui.core.Control',
        success: function (elements) {
          elements = elements.filter(element => element.getMetadata().getName() === 'sap.m.ActionSheet');
          Opa5.assert.equal(elements.length, 0, 'The user action sheet does not exist');
        },
        errorMessage: 'User Action Sheet still exists'
      });
    }
  }
  return OnTheAppPage;
});
//# sourceMappingURL=App.page-dbg.js.map

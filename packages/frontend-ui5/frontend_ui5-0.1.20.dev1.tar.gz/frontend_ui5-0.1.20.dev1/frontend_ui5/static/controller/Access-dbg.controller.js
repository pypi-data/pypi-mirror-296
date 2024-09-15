"use strict";

sap.ui.define(["sap/base/Log", "./BaseController", "./utils/Cookies"], function (Log, __BaseController, ___utils_Cookies) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const BaseController = _interopRequireDefault(__BaseController);
  const getCSRFCookie = ___utils_Cookies["getCSRFCookie"];
  /**
   * @namespace demo.spa.controller
   */
  const Access = BaseController.extend("demo.spa.controller.Access", {
    constructor: function constructor() {
      BaseController.prototype.constructor.apply(this, arguments);
      this.logger = Log.getLogger(Access.getMetadata().getName());
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    onContinuePress: function _onContinuePress() {
      const userNameInput = this.byId('idNameInput');
      const userName = userNameInput.getValue().replaceAll(' ', '').toLowerCase();
      userNameInput.setValue('');
      BaseController.connector.signIn({
        username: this.userKey,
        password: userName
      }).then(response => this.handleSuccess(response), this.handleFailure.bind(this));
    },
    onCancelPress: function _onCancelPress() {
      this.dialog.close();
      this.navToHome();
    },
    onInit: function _onInit() {
      this.getRouter().attachRoutePatternMatched(event => {
        if (event.getParameter('name') == 'ACCESS FULLSCREEN') {
          this.userKey = event.getParameter('arguments').userKey;
          this.openAccessDialog();
        }
      });
    },
    /**
     * Opens the access dialog.
     * Creates the dialog if it does not exist yet.
     */
    openAccessDialog: function _openAccessDialog() {
      if (!getCSRFCookie()) {
        void this.noCSRFTokenMessageBox();
        return;
      } else if (this.dialog) {
        this.dialog.open();
      } else {
        this.loadFragment({
          name: 'demo.spa.view.AccessDialog'
        }).then(dialog => {
          this.dialog = dialog;
          this.dialog.open();
        }).catch(error => {
          this.logger.error(String(error));
        });
      }
    },
    /** Handler for a failed signup */handleFailure: function _handleFailure(result) {
      this.dialog.setBusy(false);
      this.failedResponseToMessageBox(result);
    },
    /**
     * Handles a successful sign up.
     * Sets the username of the current user in the model and navigates back.
     * @param userName The username of the user that signed up
     */
    handleSuccess: function _handleSuccess(response) {
      response.json().then(data => {
        this.loginUser(data.username, data.user_id);
        this.getRouter().fireRouteMatched({
          name: 'AVAILABILITY CHOICES'
        });
        this.getRouter().navTo('AVAILABILITY CHOICES');
      }).catch(error => {
        this.logger.error(String(error));
      }).finally(() => {
        this.dialog.setBusy(false);
        this.dialog.close();
      });
    }
  });
  return Access;
});
//# sourceMappingURL=Access-dbg.controller.js.map

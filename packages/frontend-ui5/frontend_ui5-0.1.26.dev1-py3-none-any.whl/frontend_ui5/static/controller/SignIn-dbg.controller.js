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
  const SignIn = BaseController.extend("demo.spa.controller.SignIn", {
    constructor: function constructor() {
      BaseController.prototype.constructor.apply(this, arguments);
      this.logger = Log.getLogger(SignIn.getMetadata().getName());
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    /**
     * Event handler called when the login dialog is canceled.
     */
    onCloseSignInDialog: function _onCloseSignInDialog() {
      this.signInDialog.close();
    },
    onInit: function _onInit() {
      BaseController.prototype.onInit.call(this);
      this.getRouter().attachRoutePatternMatched(event => {
        if (event.getParameter('name') == 'SIGN IN FULLSCREEN') {
          this.openSignInDialog();
        }
      });
    },
    /*
     * Event handler for the login button in the login dialog.
     * Sends the login request to the backend.
     */
    onSignInPress: function _onSignInPress() {
      const credentials = this.getFrontendModel().getProperty('/loginForm');
      // double check the credentials because ctrl + enter will circumvent the validation and trigger the
      // login button press event which is not intended
      if (credentials.username && credentials.password) {
        this.signInDialog.setBusy(true);
        BaseController.connector.signIn(credentials).then(response => this.handleLoginSuccess(response), this.handleSignInFailure.bind(this));
      }
    },
    /**
     * Opens the login dialog.
     * Creates the dialog if it does not exist yet.
     */
    openSignInDialog: function _openSignInDialog() {
      if (!getCSRFCookie()) {
        void this.noCSRFTokenMessageBox();
        return;
      } else if (this.signInDialog) {
        this.signInDialog.open();
      } else {
        this.loadFragment({
          name: 'demo.spa.view.SignInDialog'
        }).then(dialog => {
          this.signInDialog = dialog;
          this.signInDialog.attachBeforeClose(() => {
            this.getFrontendModel().setProperty('/loginForm/password', '');
            this.navToHome();
          });
          this.signInDialog.open();
        }).catch(error => {
          this.logger.error(String(error));
        });
      }
    },
    /**
     * Handler for a successful login.
     * Sets the username in the frontend model and closes the login dialog.
     */
    handleLoginSuccess: function _handleLoginSuccess(response) {
      let userName = '???';
      let userId = '!?!';
      response.json().then(data => {
        // assume data can be parsed.
        if (data.username) {
          userName = data.username;
          userId = data.user_id;
        }
        this.loginUser(userName, userId);
        this.getUserDataModel().fetch(['person', 'slot', 'appointment']);
      }).catch(error => {
        this.logger.error(String(error));
      }).finally(() => {
        this.signInDialog.setBusy(false);
        this.signInDialog.close();
      });
    },
    /** Handler for a failed login */handleSignInFailure: function _handleSignInFailure(result) {
      this.signInDialog.setBusy(false);
      this.failedResponseToMessageBox(result);
    }
  });
  return SignIn;
});
//# sourceMappingURL=SignIn-dbg.controller.js.map

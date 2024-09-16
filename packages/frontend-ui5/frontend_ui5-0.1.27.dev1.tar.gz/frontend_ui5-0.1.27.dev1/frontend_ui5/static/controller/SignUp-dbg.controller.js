"use strict";

sap.ui.define(["sap/base/Log", "sap/m/MessageToast", "./BaseController", "./utils/Cookies", "./utils/Formatters"], function (Log, MessageToast, __BaseController, ___utils_Cookies, ___utils_Formatters) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const BaseController = _interopRequireDefault(__BaseController);
  const getCSRFCookie = ___utils_Cookies["getCSRFCookie"];
  const getEmailAddressErrorState = ___utils_Formatters["getEmailAddressErrorState"];
  /**
   * @namespace demo.spa.controller
   */
  const SignUp = BaseController.extend("demo.spa.controller.SignUp", {
    constructor: function constructor() {
      BaseController.prototype.constructor.apply(this, arguments);
      this.logger = Log.getLogger(SignUp.getMetadata().getName());
      this.getEmailAddressErrorState = getEmailAddressErrorState;
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    /**
     * Event handler called when the login dialog is canceled.
     */
    onCloseSignUpDialog: function _onCloseSignUpDialog() {
      this.signUpDialog.close();
      this.navToHome();
    },
    onInit: function _onInit() {
      BaseController.prototype.onInit.call(this);
      this.getRouter().attachRoutePatternMatched(event => {
        if (event.getParameter('name') == 'SIGN UP FULLSCREEN') {
          this.openSignUpDialog();
        }
      });
    },
    /**
     * Event handler for the sign up button in the sign up dialog.
     * Sends the sign up request to the backend.
     */
    onSignUpPress: function _onSignUpPress() {
      const formData = this.getFrontendModel().getProperty('/signUpForm');
      // double check the credentials because ctrl + enter will circumvent the validation and trigger
      // onSignUpPress which is not intended
      if (this.validateSignUpForm(formData)) {
        this.signUpDialog.setBusy(true);
        BaseController.connector.signUp(formData).then(response => this.handleSignUpSuccess(response), this.handleSignUpFailure.bind(this));
      }
    },
    /** Handler for a failed signup */handleSignUpFailure: function _handleSignUpFailure(result) {
      this.signUpDialog.setBusy(false);
      this.failedResponseToMessageBox(result);
    },
    /**
     * Handles a successful sign up.
     * Sets the username of the current user in the model and navigates back.
     * @param userName The username of the user that signed up
     */
    handleSignUpSuccess: function _handleSignUpSuccess(response) {
      MessageToast.show('Signed up successfully'); // todo i18n
      response.json().then(data => {
        this.loginUser(data.username, data.user_id);
      }).catch(error => {
        this.logger.error(String(error));
      }).finally(() => {
        this.signUpDialog.setBusy(false);
        this.navToHome();
      });
    },
    /**
     * Opens the sign up dialog.
     * Creates the dialog if it does not exist yet.
     */
    openSignUpDialog: function _openSignUpDialog() {
      if (!getCSRFCookie()) {
        void this.noCSRFTokenMessageBox();
        return;
      } else if (this.signUpDialog) {
        this.getFrontendModel().setProperty('/signUpForm', {
          ...SignUp.initialSignUpData
        });
        this.signUpDialog.open();
      } else {
        this.loadFragment({
          name: 'demo.spa.view.SignUpDialog'
        }).then(dialog => {
          this.signUpDialog = dialog;
          this.getFrontendModel().setProperty('/signUpForm', {
            ...SignUp.initialSignUpData
          });
          this.signUpDialog.attachBeforeClose(() => {
            this.getFrontendModel().setProperty('/signUpForm', {
              ...SignUp.initialSignUpData
            });
          });
          this.signUpDialog.open();
        }).catch(error => {
          this.logger.error(String(error));
        });
      }
    },
    /**
     * Double checks the sign up form because
     * the validation of the view can by circumvented which is
     * a bug in ui5 (version <=1.121) and will
     * probably be resolved in the future.
     * @param formData The sign up form to validate
     * @returns true if the form is valid, false otherwise
     */
    validateSignUpForm: function _validateSignUpForm(formData) {
      const {
        username,
        email,
        password,
        password_confirmation
      } = formData;
      if (username && email && password && password_confirmation) {
        if (password !== password_confirmation) {
          MessageToast.show('Passwords do not match'); // todo i18n
          return false;
        }
        if (this.getEmailAddressErrorState(email) !== 'None') {
          MessageToast.show('Email is not valid'); // todo i18n
          return false;
        }
        return true; // all required fields filled in correctly
      } else {
        MessageToast.show('Please fill out all required fields'); // todo i18n
        return false;
      }
    }
  });
  /**
   * The initial data for the sign up form.
   * Used for testing purposes.
   */
  SignUp.initialSignUpData = {
    username: '',
    email: '',
    password: '',
    password_confirmation: '',
    product_key: ''
  };
  /**
   * Sets the data in the sign up form for testing purposes.
   * @param data The SignUpForm
   */
  SignUp.setInitialSignUpData = function setInitialSignUpData(data) {
    this.initialSignUpData = data;
  };
  return SignUp;
});
//# sourceMappingURL=SignUp-dbg.controller.js.map

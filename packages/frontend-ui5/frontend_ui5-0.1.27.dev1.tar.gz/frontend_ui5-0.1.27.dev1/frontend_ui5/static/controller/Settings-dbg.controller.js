"use strict";

sap.ui.define(["sap/base/i18n/Localization", "sap/base/Log", "./BaseController", "./utils/Cookies"], function (Localization, Log, __BaseController, ___utils_Cookies) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const BaseController = _interopRequireDefault(__BaseController);
  const getCookie = ___utils_Cookies["getCookie"];
  const getCookieConsent = ___utils_Cookies["getCookieConsent"];
  const setCookie = ___utils_Cookies["setCookie"];
  const setCookieConsent = ___utils_Cookies["setCookieConsent"];
  const unsetCookieConsent = ___utils_Cookies["unsetCookieConsent"];
  /**
   * @namespace demo.spa.controller
   */
  const Settings = BaseController.extend("demo.spa.controller.Settings", {
    constructor: function constructor() {
      BaseController.prototype.constructor.apply(this, arguments);
      /** Logger for the Settings controller */
      this.logger = Log.getLogger(Settings.prototype.getMetadata().getName());
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    /**
     * Called after rendering the view.
     */
    onAfterRendering: function _onAfterRendering() {
      this.selectItems();
    },
    /**
     * Called when the user changes the cookie consent.
     * Side effect: Deletes all cookies in case the consent is revoked.
     */
    onChangeCookieConsent: function _onChangeCookieConsent(event) {
      const state = event.getSource().getState();
      if (state) {
        setCookieConsent();
      } else {
        if (this.getOwnerComponent().getModel('frontend').getProperty('/currentUser/username')) {
          void this.errorToMessageBox('error.revokeConsent');
          event.getSource().setState(true);
        } else {
          unsetCookieConsent();
        }
      }
    },
    /**
     * Called when the language input changes its value.
     */
    onChangeLanguageByInput: function _onChangeLanguageByInput(event) {
      this.changeLanguage(event.getSource().getSelectedKey());
    },
    /**
     * Called when the user changes the theme.
     */
    onChangeTheme: function _onChangeTheme(event) {
      setCookie('THEME', event.getSource().getSelectedKey());
      this.setTheme(event.getSource().getSelectedKey());
    },
    /**
     * Preselects the items based on settings in cookies.
     */
    selectItems: function _selectItems() {
      const selectLanguage = this.byId('idSelectLanguage');
      if (getCookie('LANG')) {
        selectLanguage.setSelectedKey(getCookie('LANG'));
      } else {
        const langKey = Localization.getLanguage().slice(0, 2);
        selectLanguage.setSelectedKey(langKey);
      }
      const selectTheme = this.byId('idSelectTheme');
      selectTheme.setSelectedKey(getCookie('THEME') || 'system');
      const switchCookieConsent = this.byId('idSwitchCookieConsent');
      switchCookieConsent.setState(getCookieConsent());
    }
  });
  return Settings;
});
//# sourceMappingURL=Settings-dbg.controller.js.map

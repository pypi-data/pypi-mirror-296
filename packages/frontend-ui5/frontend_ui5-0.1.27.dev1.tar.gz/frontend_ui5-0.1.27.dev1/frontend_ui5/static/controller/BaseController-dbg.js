"use strict";

sap.ui.define(["sap/base/Log", "sap/base/i18n/Localization", "sap/m/ActionSheet", "sap/m/Button", "sap/m/MessageBox", "sap/m/library", "sap/ui/core/Theming", "sap/ui/core/UIComponent", "sap/ui/core/mvc/Controller", "sap/ui/core/routing/History", "../model/Frontend", "../model/Lang", "../model/UserData", "./utils/BackendConnector", "./utils/Cookies", "./utils/Formatters", "./utils/MockConnector"], function (Log, Localization, ActionSheet, Button, MessageBox, sap_m_library, Theming, UIComponent, Controller, History, ___model_Frontend, ___model_Lang, ___model_UserData, __BackendConnector, ___utils_Cookies, ___utils_Formatters, __MockConnector) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const PlacementType = sap_m_library["PlacementType"];
  const frontendModel = ___model_Frontend["frontendModel"];
  const languageModel = ___model_Lang["languageModel"];
  const userDataModel = ___model_UserData["userDataModel"];
  const BackendConnector = _interopRequireDefault(__BackendConnector);
  const getCookie = ___utils_Cookies["getCookie"];
  const setCookie = ___utils_Cookies["setCookie"];
  const setCookieConsent = ___utils_Cookies["setCookieConsent"];
  const setDummyCSRFCookie = ___utils_Cookies["setDummyCSRFCookie"];
  const formatBtnTxtForSmallScreen = ___utils_Formatters["formatBtnTxtForSmallScreen"];
  const MockConnector = _interopRequireDefault(__MockConnector);
  /**
   * @namespace demo.spa.controller
   */
  const BaseController = Controller.extend("demo.spa.controller.BaseController", {
    constructor: function constructor() {
      Controller.prototype.constructor.apply(this, arguments);
      /**
       * Returns empty string for large Screens and the given text for small screens
       * so the overflow menu will show the text of the button.
       */
      this.formatBtnTxtForSmallScreen = formatBtnTxtForSmallScreen;
      /** Logger for the BaseController */
      this.logger = Log.getLogger(BaseController.prototype.getMetadata().getName());
      /** Maps back theme names to theme aliases */
      this.mapThemeToAlias = {
        sap_horizon_dark: 'dark',
        sap_horizon: 'light'
      };
      /** Timestamp of the last error message to make sure not too many error messages are shown
       * in case of network errors. */
      this.lastErrorTimestamp = 0;
      /** Maps theme aliases to actual theme names */
      this.themes = {
        _controller: this,
        dark: 'sap_horizon_dark',
        light: 'sap_horizon',
        get system() {
          let theme = this.light;
          try {
            theme = window.matchMedia('(prefers-color-scheme:dark)').matches ? this.dark : this.light;
          } catch (error) {
            this._controller.logger.error(String(error));
          }
          return theme;
        }
      };
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    /**
     * Changes the language of the app and reloads the page.
     * Uses the URL parameter if cookie consent is not given, otherwise uses the 'LANG' cookie.
     * @param languageCode The language code to change to
     */
    changeLanguage: function _changeLanguage(languageCode) {
      if (Localization.getLanguage() !== languageCode) {
        const currentUrl = new URL(window.location.href);
        if (!setCookie('LANG', languageCode)) {
          // if cookie consent is not given, we change lange with URL parameter
          currentUrl.searchParams.set('lang', languageCode);
          window.history.pushState({
            path: currentUrl.href
          }, '', currentUrl.href);
        } else {
          // if cookie consent is given, we change lange with cookie and remove URL parameter
          // since we don't need it anymore
          currentUrl.searchParams.delete('lang');
          window.history.pushState({
            path: currentUrl.href
          }, '', currentUrl.href);
        }
        window.location.reload();
      }
    },
    /**
     * Creates an action sheet with the available languages and opens it by the source button.
     * @param event The button press event
     */
    createLanguageActionSheet: function _createLanguageActionSheet(event) {
      const source = event.getSource();
      const langModel = this.getLangModel();
      const buttons = langModel.getData().supported.map(lang => {
        return new Button({
          text: lang.name,
          press: () => this.changeLanguage(lang.code)
        });
      });
      const actionSheet = new ActionSheet({
        placement: PlacementType.Bottom,
        buttons: buttons
      });
      actionSheet.openBy(source);
    },
    /**
     * Shows a message box with the text that is stored in the i18n model under the given key
     * @param i18nKey the key for the text in the i18n model
     */
    errorToMessageBox: async function _errorToMessageBox(i18nKey, error) {
      let msgText = await this.getBundleText(i18nKey);
      if (msgText === i18nKey) {
        // no translation found
        msgText = await this.getBundleText('error.unknown');
      }
      MessageBox.error(msgText, {
        details: error ? String(error) : undefined
      });
    },
    /**
     * Handles failures that occur during the communication with the backend
     * @param failure Carries the information to display to the user.
     * Can either be a Response with a status code >= 400 or an Error
     */
    failedResponseToMessageBox: function _failedResponseToMessageBox(failure) {
      if (failure instanceof Response) {
        if (failure.status >= 500) {
          void this.errorToMessageBox('error.5xx');
        } else if (failure.status >= 400) {
          failure.json().then(json => {
            if (String(json.details).toLowerCase().includes('csrf failed')) {
              void this.errorToMessageBox('error.403CSRF', new Error(JSON.stringify(json)));
            } else if (json.i18n) {
              // server provided i18n key for error message
              if (json.i18n === 'error.404') {
                void this.errorToMessageBox(json.i18n, new Error(failure.url));
              } else {
                void this.errorToMessageBox(json.i18n);
              }
            } else {
              // no i18n key provided by server
              if (failure.status === 404) {
                void this.errorToMessageBox(json.i18n, new Error(failure.url));
              } else {
                void this.errorToMessageBox(`error.${failure.status}`);
              }
            }
          }).catch(error => {
            // error parsing JSON
            this.logger.error(String(error));
            if (failure.status === 404) {
              void this.errorToMessageBox('error.404', new Error(failure.url));
            } else {
              void this.errorToMessageBox(`error.${failure.status}`);
            }
          });
        } else {
          this.logger.error('Response is not an error, since its status code is less than 400. ' + 'Thus, it should not be handled as a failed response.');
          return;
        }
      } else if (failure instanceof TypeError && (failure.message.includes('to fetch') || failure.message.includes('to load resource'))) {
        // "NetworkError when attempting to fetch resource" (Firefox) / "Failed to fetch" (Chrome) / "Failed to load resource" (Safari)
        this.logger.error(String(failure));
        void this.errorToMessageBox('error.checkConnection');
      } else {
        this.logger.error(String(failure));
        void this.errorToMessageBox('error.unknown', failure);
      }
    },
    /**
     * Returns a promise which resolves with the resource bundle value of the given key <code>sI18nKey</code>
     * @param i18nKey The key
     * @param placeholderValues The values which will replace the placeholders in the i18n value
     * @returns The promise which resolves with the i18n value
     */
    getBundleText: function _getBundleText(i18nKey, placeholderValues) {
      return this.getBundleTextByModel(i18nKey, this.getModel('i18n'), placeholderValues);
    },
    /**
     * Returns a promises which resolves with the resource bundle value of the given key <code>sI18nKey</code>
     * @param i18key The key
     * @param resourceModel The resource model
     * @param placeholderValues The values which will replace the placeholders in the i18n value
     * @returns A promise which resolves with the i18n value to a string
     */
    getBundleTextByModel: async function _getBundleTextByModel(i18key, resourceModel, placeholderValues) {
      return resourceModel.getResourceBundle().then(function (bundle) {
        return bundle.getText(i18key, placeholderValues);
      });
    },
    /**
     * Convenience method for getting the frontend model
     * @returns The frontend model
     */
    getFrontendModel: function _getFrontendModel() {
      return this.getOwnerComponent().getModel('frontend');
    },
    /**
     * Convenience method for getting the view's i18n bundle
     */
    getI18nBundle: function _getI18nBundle() {
      return this.getI18nModel().getResourceBundle();
    },
    /**
     * Convenience method for getting the view's i18n model
     * @public
     * @returns {sap.ui.model.resource.ResourceModel} the i18n model of the view
     */
    getI18nModel: function _getI18nModel() {
      return this.getModel('i18n');
    },
    /**
     * Convenience method for getting the language model
     * @returns The language model
     */
    getLangModel: function _getLangModel() {
      return this.getOwnerComponent().getModel('lang');
    },
    /**
     * Convenience method for getting the view model by name.
     */
    getModel: function _getModel(modelName) {
      return this.getView().getModel(modelName);
    },
    /**
     * Convenience method for accessing the router.
     */
    getRouter: function _getRouter() {
      return UIComponent.getRouterFor(this);
    },
    /**
     * Convenience method for getting the user data model
     * @returns The user data model
     */
    getUserDataModel: function _getUserDataModel() {
      return this.getOwnerComponent().getModel('userData');
    },
    /**
     * Checks if the mock connector should be used.
     * @returns True if the mock connector should be used, false otherwise.
     */
    hasMockBackend: function _hasMockBackend() {
      if (URLSearchParams && window.location.search) {
        const params = new URLSearchParams(window.location.search);
        const useMockConnector = params.get('useMockConnector') == 'true';
        if (useMockConnector) {
          return true;
        }
      }
      return false;
    },
    /**
     * Set user name in frontend model and updates user data.
     * @param username The username to set in the frontend model
     */
    loginUser: function _loginUser(username, user_id) {
      window.django = {
        username: username,
        user_id: user_id
      };
      this.logger.info(`logged in ${username} with id ${user_id}`);
      this.setUserNameAndId(username, user_id);
      this.getUserDataModel().fetch(['person', 'appointment', 'slot']);
    },
    /**
     * Navigates back in app history or to the home screen if there is no history.
     */
    navBack: function _navBack() {
      const history = History.getInstance();
      const prevHash = history.getPreviousHash();
      if (prevHash !== undefined) {
        window.history.go(-1);
      } else {
        this.getRouter().navTo('HOME');
      }
    },
    navToHome: function _navToHome() {
      this.getRouter().fireRouteMatched({
        name: 'HOME'
      });
      this.getRouter().navTo('HOME');
    },
    /**
     * Shows a message box saying that cookie consent is needed for the app to work.
     */
    noCSRFTokenMessageBox: async function _noCSRFTokenMessageBox() {
      const navBack = () => {
        this.navBack();
      };
      MessageBox.confirm(await this.getBundleText('cookieConsent.text'), {
        title: await this.getBundleText('cookieConsent.title'),
        actions: [MessageBox.Action.YES, MessageBox.Action.NO],
        onClose: function (action) {
          if (action === MessageBox.Action.YES) {
            setCookieConsent();
            setDummyCSRFCookie();
            document.location.reload();
          } else {
            navBack();
          }
        },
        emphasizedAction: MessageBox.Action.YES
      });
    },
    /**
     * Called when the controller is instantiated.
     */
    onInit: function _onInit() {
      if (!BaseController.isInitialized) {
        this.initLogger();
        this.applyCookieAndUrlBasedSettings();
        this.initModels();
        this.initBackendConnection();
        this.attachNetworkErrorHandler();
        this.getRouter().attachRoutePatternMatched(event => {
          this.adjustFullScreenToRoute(event);
        });
        BaseController.isInitialized = true;
        this.logger.info('Base Initialization Done.');
      } else {
        this.logger.info('Skipping Base Initialization.');
      }
    },
    /**
     * Called when a nav back button is pressed.
     */
    onNavBack: function _onNavBack() {
      this.navBack();
    },
    /**
     * Convenience method for setting the view model.
     */
    setModel: function _setModel(model, modelName) {
      return this.getView().setModel(model, modelName);
    },
    /**
     * Sets the theme for the application.
     */
    setTheme: function _setTheme(theme) {
      const themeName = this.themes[theme];
      if (themeName) {
        Theming.setTheme(themeName);
      } else {
        this.logger.warning(`Theme "${theme}" not found!`);
      }
    },
    /**
     * Sets user name and id in frontend model and updates model
     */
    setUserNameAndId: function _setUserNameAndId(username, userId) {
      this.getFrontendModel().setProperty('/currentUser/username', username);
      this.getFrontendModel().setProperty('/currentUser/user_id', userId);
    },
    /**
     * Adjusts the full screen mode according to the route.
     * In case the route name contains 'FULLSCREEN', the full screen mode will be set to true,
     * otherwise it will be set to false.
     */
    adjustFullScreenToRoute: function _adjustFullScreenToRoute(event) {
      if (event.getParameter('name').includes('FULLSCREEN')) {
        this.setFullScreenMode(true);
      } else {
        this.setFullScreenMode(false);
      }
    },
    /**
     * Applies language and theme settings.
     */
    applyCookieAndUrlBasedSettings: function _applyCookieAndUrlBasedSettings() {
      // Apply theme
      if (getCookie('THEME')) {
        this.setTheme(getCookie('THEME'));
        this.logger.info(`Theme set to ${getCookie('THEME')}`);
      } else {
        this.setTheme('system');
        this.logger.info('Theme set to system');
      }
      // Apply language setting
      const currentUrl = new URL(window.location.href);
      const langCode = currentUrl.searchParams.get('lang');
      if (getCookie('LANG')) {
        Localization.setLanguage(getCookie('LANG'));
        currentUrl.searchParams.delete('lang');
        window.history.pushState({
          path: currentUrl.href
        }, '', currentUrl.href);
        this.logger.info(`Language set to ${getCookie('LANG')}`);
      } else if (langCode) {
        Localization.setLanguage(langCode);
        this.logger.info('Language not set');
      }
    },
    attachNetworkErrorHandler: function _attachNetworkErrorHandler() {
      this.lastErrorTimestamp = Date.now();
      window.addEventListener('unhandledrejection', rejection => {
        const now = Date.now();
        try {
          const includesKeywords = rejection.reason.message.includes('to fetch') || rejection.reason.message.includes('to load') || rejection.reason.message.includes('Load failed');
          if (rejection.reason instanceof TypeError && includesKeywords && now - this.lastErrorTimestamp > 2000) {
            this.logger.error(`NETWORK ERROR (${now - this.lastErrorTimestamp}ms since last): ${rejection.reason.message}`);
            this.lastErrorTimestamp = now;
            void this.errorToMessageBox('error.checkConnection', rejection.reason);
          }
        } catch (error) {
          this.logger.error(String(error));
        }
      });
    },
    /**
     * Initializes the backend connection based on the URL parameters.
     * If the URL parameter use Connector is set to true, the mock connector will be used.
     * Otherwise the backend connector will be used.
     */
    initBackendConnection: function _initBackendConnection() {
      if (this.hasMockBackend()) {
        BaseController.connector = new MockConnector();
        this.logger.info('Using mock connector');
      } else {
        BaseController.connector = new BackendConnector();
        this.logger.info('Using backend connector');
      }
    },
    /**
     * Initializes the logLevel with the value from the URL parameter logLevel.
     * If not specified, the logLevel will be set to ERROR.
     */
    initLogger: function _initLogger() {
      Log.setLevel(Log.Level.ERROR);
      if (URLSearchParams && window.location.search) {
        const params = new URLSearchParams(window.location.search);
        const logLevel = params.get('loglevel');
        if (['ALL', 'DEBUG', 'ERROR', 'FATAL', 'INFO', 'NONE', 'TRACE', 'WARNING'].includes(logLevel)) {
          Log.setLevel(Log.Level[logLevel]);
          this.logger.info(`Log level set to ${logLevel}`);
        }
      }
    },
    /**
     * Initializes userData, Frontend and Lang model.
     */
    initModels: function _initModels() {
      this.getOwnerComponent().setModel(frontendModel, 'frontend');
      this.getOwnerComponent().setModel(userDataModel, 'userData');
      this.getUserDataModel().setFailureMessageHandler(this.failedResponseToMessageBox.bind(this));
      this.getOwnerComponent().setModel(languageModel, 'lang');
    },
    /**
     * Sets the full screen mode to the given value
     * @param fullScreenMode The new value for the full screen mode
     */
    setFullScreenMode: function _setFullScreenMode(fullScreenMode) {
      this.getFrontendModel().setProperty('/fullScreenMode', fullScreenMode);
    }
  });
  /** Indicates whether the controller is initialized. If so, the onInit method skips the initialization. */
  BaseController.isInitialized = false;
  return BaseController;
});
//# sourceMappingURL=BaseController-dbg.js.map

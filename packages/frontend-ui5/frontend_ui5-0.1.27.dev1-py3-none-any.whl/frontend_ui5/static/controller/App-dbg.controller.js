"use strict";

sap.ui.define(["sap/base/Log", "sap/m/Button", "sap/m/MessageToast", "sap/m/NotificationListItem", "sap/m/ResponsivePopover", "sap/m/library", "sap/ui/Device", "sap/ui/core/CustomData", "sap/ui/core/Theming", "sap/ui/core/library", "./BaseController", "./utils/Comparators", "./utils/Cookies", "./utils/Formatters"], function (Log, Button, MessageToast, NotificationListItem, ResponsivePopover, sap_m_library, Device, CustomData, Theming, sap_ui_core_library, __BaseController, ___utils_Comparators, ___utils_Cookies, ___utils_Formatters) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const PlacementType = sap_m_library["PlacementType"];
  const ValueState = sap_ui_core_library["ValueState"];
  const BaseController = _interopRequireDefault(__BaseController);
  const comparePersons = ___utils_Comparators["comparePersons"];
  const deleteCookie = ___utils_Cookies["deleteCookie"];
  const getCookie = ___utils_Cookies["getCookie"];
  const setCookie = ___utils_Cookies["setCookie"];
  const setCookieConsent = ___utils_Cookies["setCookieConsent"];
  const setDummyCSRFCookie = ___utils_Cookies["setDummyCSRFCookie"];
  const shortenString = ___utils_Formatters["shortenString"];
  /**
   * @namespace demo.spa.controller
   */
  const App = BaseController.extend("demo.spa.controller.App", {
    constructor: function constructor() {
      BaseController.prototype.constructor.apply(this, arguments);
      this.comparePersons = comparePersons;
      /** Logger for the app controller */
      this.logger = Log.getLogger(App.prototype.getMetadata().getName());
      /** Formatter to shorten strings to a given length */
      this.shortenString = shortenString;
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    formatPersonNameInNavList: async function _formatPersonNameInNavList(userId, currentUserId, firstName, lastName) {
      const meMarker = await this.getBundleText('thatsMe');
      const fullName = `${firstName} ${lastName}`;
      return userId === currentUserId ? fullName + ' ' + meMarker : fullName;
    },
    /**
     * Called after the view is rendered.
     * Collapses the side navigation in case the screen is smaller 1024px.
     */
    onAfterRendering: function _onAfterRendering() {
      if (Device.resize.width <= 1024 && Device.system.desktop) {
        const toggleBtn = this.byId('idSideNavigationToggleButton');
        // setExpanded is not working properly, so we need to use fireEvent here
        // to trigger sideNav collapse
        setTimeout(() => {
          if (!this.getRouter().getRouteInfoByHash(window.location.hash.slice(1))?.name.includes('FULLSCREEN')) {
            toggleBtn.fireEvent('press');
          }
        }, 1500);
      }
    },
    /**
     * Called before the view is rendered.
     * Calls onThemeChanged so the images will adjust to the current theme.
     */
    onBeforeRendering: function _onBeforeRendering() {
      this.onThemeChanged();
    },
    /**
     * Called when the controller is destroyed. Use this one to free resources
     * and finalize activities.
     */
    onExit: function _onExit() {
      Device.media.detachHandler(this.handleWindowResize.bind(this), this);
    },
    /**
     * Called when the controller is instantiated.
     */
    onInit: function _onInit() {
      BaseController.prototype.onInit.call(this);
      this.toolPage = this.byId('idToolPage');
      this.prepareSideNavigationLists();
      this.setUpAttachedHandlers();
      this.prepareAccount();
    },
    /**
     * Event handler for the logout button in the user action sheet
     */
    onLogoutPress: function _onLogoutPress() {
      BaseController.connector.signOut().then(this.handleLogoutSuccess.bind(this), this.handleLogoutFailure.bind(this));
    },
    /**
     * Event handler for the menu button.
     * Expands or collapses the side navigation based on the current state.
     */
    onMenuButtonPress: function _onMenuButtonPress() {
      const sideNav = this.byId('idSideNavigation');
      if (!sideNav.getVisible()) {
        sideNav.setVisible(true);
        return;
      }
      const isSideExpanded = this.toolPage.getSideExpanded();
      void this.setToggleButtonTooltip(isSideExpanded);
      this.toolPage.setSideExpanded(!this.toolPage.getSideExpanded());
    },
    /**
     * Event handler for the notification button
     * @param event the button press event
     */
    onNotificationPress: function _onNotificationPress(event) {
      const source = event.getSource();
      this.getI18nBundle().then(bundle => {
        const btn = new Button({
          text: bundle.getText('app.btnBackText'),
          press: () => {
            this.getNotificationMessagePopover().destroy();
          }
        });
        let notificationPopover = this.getNotificationMessagePopover();
        if (!notificationPopover) {
          notificationPopover = new ResponsivePopover(this.getView().createId('idNotificationMessagePopover'), {
            title: bundle.getText('app.notificationTitle'),
            contentWidth: '300px',
            endButton: btn,
            placement: PlacementType.Bottom,
            content: {
              path: 'userData>/notification_list',
              factory: this.createNotification.bind(this)
            },
            afterClose: function () {
              notificationPopover.destroy();
            }
          });
          this.toolPage.addDependent(notificationPopover);
          notificationPopover.openBy(source);
        } else if (notificationPopover.isOpen()) {
          notificationPopover.close();
        }
      }).catch(error => {
        this.logger.error(error.message);
      });
    },
    onOpenSignInDialogPress: function _onOpenSignInDialogPress() {
      this.getRouter().navTo('SIGN IN FULLSCREEN');
    },
    onOpenSignUpDialogPress: function _onOpenSignUpDialogPress() {
      this.getRouter().navTo('SIGN UP FULLSCREEN');
    },
    /**
     * Event handler for the route match event.
     * Closes the side navigation if the device is a phone.
     */
    onRouteChange: function _onRouteChange() {
      if (Device.system.phone) {
        this.toolPage.setSideExpanded(false);
      }
    },
    /** Changes logo of the app based on the theme */onThemeChanged: function _onThemeChanged() {
      const theme = this.getTheme();
      if (theme) {
        this.setSvgLogoPath(theme);
      } else {
        this.logger.error(`Theme is not supported`);
      }
    },
    /**
     * Event handler when the user button is pressed
     * @param event the button press event
     */
    onUserBtnPress: function _onUserBtnPress(event) {
      const actionSheet = this.getView().byId('idUserActionSheet');
      actionSheet.openBy(event.getSource());
    },
    /**
     * Factory function for the notification items
     * @param id The id for the item
     * @param bindingContext The binding context for the item
     * @returns The new notification list item
     */
    createNotification: function _createNotification(id, bindingContext) {
      const boundObject = bindingContext.getObject();
      const notificationItem = new NotificationListItem(id, {
        title: boundObject.title,
        description: boundObject.description,
        priority: boundObject.priority,
        datetime: boundObject.datetime,
        customData: [new CustomData({
          key: 'path',
          value: bindingContext.getPath()
        })],
        close: event => {
          const bindingPath = event.getSource().getCustomData()[0].getValue();
          const index = bindingPath.split('/').pop();
          const items = this.getUserDataModel().getData().notification_list.splice(parseInt(index), 1);
          if (items.length === 0) {
            this.getView().byId('idNotificationMessagePopover');
            this.getNotificationMessagePopover().close();
          }
          this.getUserDataModel().updateBindings(true);
          void this.getBundleText('app.msgNotificationDeleted').then(sMessageText => {
            MessageToast.show(sMessageText);
          });
        }
      });
      return notificationItem;
    },
    /**
     * Convenience method for getting the notification message popover
     * @returns The notification message popover
     */
    getNotificationMessagePopover: function _getNotificationMessagePopover() {
      return this.byId('idNotificationMessagePopover');
    },
    /** Returns the theme alias for the current theme */getTheme: function _getTheme() {
      return this.mapThemeToAlias[Theming.getTheme()];
    },
    /**
     * Handler for a failed logout.
     * Sets cookie so the user is logged out when the page is reloaded.
     */
    handleLogoutFailure: function _handleLogoutFailure() {
      this.getUserDataModel().reset();
      this.setUserNameAndId('', '');
      setCookie('LOG_OUT');
    },
    /**
     * Handler for a successful logout
     */
    handleLogoutSuccess: function _handleLogoutSuccess() {
      this.setUserNameAndId('', '');
      this.getUserDataModel().reset();
    },
    /**
     * Expands or collapses the side navigation based on the current width of the screen
     * @param {object} device the device information from UI5
     */
    handleWindowResize: function _handleWindowResize(device) {
      const isExpanded = this.toolPage.getSideExpanded();
      const isTablet = device.name === 'Tablet';
      const isPhone = device.name === 'Phone';
      const isDesktop = device.name === 'Desktop';
      if (isExpanded && (isTablet || isPhone)) {
        this.toolPage.setSideExpanded(false);
        void this.setToggleButtonTooltip(false);
      } else if (!isExpanded && isDesktop) {
        this.toolPage.setSideExpanded(true);
        void this.setToggleButtonTooltip(true);
      }
    },
    prepareAccount: function _prepareAccount() {
      if (getCookie('LOG_OUT')) {
        deleteCookie('LOG_OUT');
        BaseController.connector.signOut().then(this.handleLogoutSuccess.bind(this), this.handleLogoutFailure.bind(this));
      } else {
        const userIsAuthenticated = globalThis.django && globalThis.django.username;
        if (userIsAuthenticated) {
          this.loginUser(django.username, django.user_id);
        } else if (this.hasMockBackend()) {
          setCookieConsent();
          setDummyCSRFCookie();
          this.loginUser('Benjamin Cooper', '3mzw1aw7iw200');
        }
      }
    },
    prepareSideNavigationLists: function _prepareSideNavigationLists() {
      this.setSelectedNavListItem();
      this.getUserDataModel().attachModelChangedHandler(event => {
        if (event.getParameter('entityName') === 'person') {
          this.setSelectedNavListItem();
        }
      });
      this.getRouter().attachEvent('navigateBackToValidRoute', () => this.setSelectedNavListItem());
      this.getRouter().attachRouteMatched({}, () => this.setSelectedNavListItem());
    },
    setSelectedNavListItem: function _setSelectedNavListItem() {
      const defaultElem = this.byId('idHomeNavListItem');
      const navList = this.byId('idNavList');
      const navListFixed = this.byId('idNavListFixed');
      const itemsNavList = navList.getItems();
      const itemsNavListFixed = navListFixed.getItems();
      const navListItems = [...itemsNavList, ...itemsNavListFixed];
      const subItems = [];
      for (const item of navListItems) {
        item.getAggregation('items')?.forEach(subItem => subItems.push(subItem));
      }
      const selectedItem = [...navListItems, ...subItems].find(item => item.getHref() === window.location.hash);
      if (selectedItem) {
        selectedItem.focus();
        if (itemsNavListFixed.includes(selectedItem)) {
          navListFixed.setSelectedItem(selectedItem);
          navList.setSelectedItem(null);
        } else {
          navList.setSelectedItem(selectedItem);
          navListFixed.setSelectedItem(null);
        }
      } else {
        navList.setSelectedItem(defaultElem);
        navListFixed.setSelectedItem(null);
      }
    },
    /** Sets the svg logo path in the frontend model */setSvgLogoPath: function _setSvgLogoPath(theme) {
      const resourceRoot = this.getFrontendModel().getData().resourceRoot;
      this.getFrontendModel().setProperty('/svgLogoPath', `${resourceRoot}img/logo-${theme}.svg`);
    },
    /**
     * Sets the text to the tooltip of the ToggleButton
     * @param isSideExpanded The value of the property sideExpanded of the ToolPage
     */
    setToggleButtonTooltip: async function _setToggleButtonTooltip(isSideExpanded) {
      const toggleBtn = this.byId('idSideNavigationToggleButton');
      const tooltipText = await this.getBundleText(isSideExpanded ? 'app.btnExpandMenu' : 'app.btnCollapseMenu');
      toggleBtn.setTooltip(tooltipText);
    },
    /**
     * Attaches all needed handlers for the app.
     */
    setUpAttachedHandlers: function _setUpAttachedHandlers() {
      Device.media.attachHandler(this.handleWindowResize.bind(this), this);
      this.getRouter().attachRouteMatched(this.onRouteChange.bind(this));
      Theming.attachApplied(this.onThemeChanged.bind(this));
      sap.ui.getCore().attachValidationError(event => {
        try {
          event.getParameter('element').setValueState(ValueState.Error);
        } catch (error) {
          this.logger.error(String(error));
        }
      });
      sap.ui.getCore().attachValidationSuccess(event => {
        try {
          event.getParameter('element').setValueState(ValueState.None);
        } catch (error) {
          this.logger.error(String(error));
        }
      });
    }
  });
  return App;
});
//# sourceMappingURL=App-dbg.controller.js.map

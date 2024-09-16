"use strict";

sap.ui.define(["sap/base/Log", "sap/ui/Device", "sap/ui/core/UIComponent", "sap/ui/model/BindingMode", "sap/ui/model/json/JSONModel"], function (Log, Device, UIComponent, BindingMode, JSONModel) {
  "use strict";

  /**
   * @namespace demo.spa
   */
  const Component = UIComponent.extend("demo.spa.Component", {
    constructor: function constructor() {
      UIComponent.prototype.constructor.apply(this, arguments);
      this.logger = Log.getLogger(Component.getMetadata().getName());
    },
    /**
     * The component is initialized by UI5 automatically during the startup of the app and calls the init method once.
     * In this method, the device model is set and the router is initialized.
     */
    init: function _init() {
      UIComponent.prototype.init.call(this);
      this.createPolyfillForSets();
      this.setModel(this.createDeviceModel(), 'device');
      this.getRouter().initialize();
    },
    /** Creates a OneWay JSONModel for the device API */createDeviceModel: function _createDeviceModel() {
      const oModel = new JSONModel(Device);
      oModel.setDefaultBindingMode(BindingMode.OneWay);
      return oModel;
    },
    /**
     * Polyfills
     * - Set.prototype.intersection
     * - Set.prototype.difference
     */
    createPolyfillForSets: function _createPolyfillForSets() {
      if (Set.prototype.intersection == undefined) {
        this.logger.warning('Polyfilling Set.prototype.intersection');
        Set.prototype.intersection = function (setB) {
          return new Set([...this].filter(x => setB.has(x)));
        };
      }
      if (Set.prototype.difference == undefined) {
        this.logger.warning('Polyfilling Set.prototype.difference');
        Set.prototype.difference = function (setB) {
          return new Set([...this].filter(x => !setB.has(x)));
        };
      }
    }
  });
  return Component;
});
//# sourceMappingURL=Component-dbg.js.map

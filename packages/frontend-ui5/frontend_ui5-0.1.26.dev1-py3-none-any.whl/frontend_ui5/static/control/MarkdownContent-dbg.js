"use strict";

sap.ui.define(["marked", "sap/base/Log", "sap/ui/core/Control", "sap/ui/dom/includeStylesheet", "sap/base/i18n/Localization"], function (__marked, Log, Control, includeStylesheet, Localization) {
  "use strict";

  const marked = __marked["marked"];
  /**
   * @namespace demo.spa.control
   */
  const MarkdownContent = Control.extend("demo.spa.control.MarkdownContent", {
    /** Renderer for the MarkdownContent control */renderer: {
      apiVersion: 2,
      render: (renderManager, control) => {
        const contentID = 'idMarkdownContent-' + MarkdownContent.controlCounter++;
        renderManager.openStart('div', control);
        renderManager.style('text-align', 'justify');
        renderManager.style('color', 'inherit !important');
        renderManager.class('customMarkdownContent');
        renderManager.openEnd();
        renderManager.unsafeHtml(`<div id="${contentID}"></div>`);
        control.triggerFetch(contentID, control.getSrcPath());
        renderManager.close('div');
      }
    },
    /** Metadata for the MarkdownContent control, holds the properties and events associated with the control */metadata: {
      properties: {
        /** Path to the markdown file. Default: '' */
        src: {
          type: 'string',
          defaultValue: ''
        },
        /** Fallback language in case the current language is not present. Default: en (english) */
        fallback: {
          type: 'string',
          defaultValue: 'en'
        }
      }
    },
    constructor: function _constructor(id, settings) {
      Control.prototype.constructor.call(this, id, settings);
      /** Logger for the MarkdownContent control */
      this.logger = Log.getLogger(MarkdownContent.prototype.getMetadata().getName());
    },
    /** Returns the path to the fallback markdown file in case the current language is not supported */getFallbackSrcPath: function _getFallbackSrcPath() {
      const i18nPath = 'i18n/markdown/';
      return this.getPathPrefix() + i18nPath + this.getSrc() + '_' + this.getFallback() + '.md';
    },
    /** Returns the path to the markdown file based on the current language */getSrcPath: function _getSrcPath() {
      const languageCode = Localization.getLanguage().slice(0, 2).toLowerCase();
      const i18nPath = 'i18n/markdown/';
      return this.getPathPrefix() + i18nPath + this.getSrc() + '_' + languageCode + '.md';
    },
    /** Initializes the control with a custom style control style sheet */init: function _init() {
      void includeStylesheet(this.getPathPrefix() + 'control/MarkdownContent.css');
    },
    /**
     * Returns the path to the resource roots based on the settings in the sap-ui-bootstrap script tag.
     * Returns './' if the parsing of the resource roots fails.
     * @returns {string} Path to the resource roots
     */
    getPathPrefix: function _getPathPrefix() {
      try {
        const resourceRoots = JSON.parse(document.getElementById('sap-ui-bootstrap').getAttribute('data-sap-ui-resourceroots'));
        return Object.values(resourceRoots)[0];
      } catch {
        return './';
      }
    },
    /** Triggers the fetch of the markdown file and renders it to the custom control */triggerFetch: function _triggerFetch(contentID, path) {
      void fetch(path).then(response => {
        if (response.status >= 400) {
          if (path !== this.getFallbackSrcPath()) {
            this.triggerFetch(contentID, this.getFallbackSrcPath());
          }
          throw new Error('Bad response status code from server ' + response.status + ' for path ' + path);
        } else return response.text();
      }).then(markdown => {
        if (document.getElementById(contentID)) {
          document.getElementById(contentID).innerHTML = marked(markdown);
        }
      });
    }
  });
  /** Counter for the MarkdownContent control for unique IDs */
  MarkdownContent.controlCounter = 0;
  return MarkdownContent;
});
//# sourceMappingURL=MarkdownContent-dbg.js.map

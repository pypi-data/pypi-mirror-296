"use strict";

sap.ui.define(["sap/ui/test/Opa5"], function (Opa5) {
  "use strict";

  class Opa5Base extends Opa5 {
    iRestoreBodyStyles() {
      return this.waitFor({
        success: () => {
          document.body.style.width = '';
          document.body.style.left = '';
          document.body.style.position = '';
          document.body.classList.remove('sapUiOpaBodyComponent');
        }
      });
    }
  }
  return Opa5Base;
});
//# sourceMappingURL=Opa5Base-dbg.js.map

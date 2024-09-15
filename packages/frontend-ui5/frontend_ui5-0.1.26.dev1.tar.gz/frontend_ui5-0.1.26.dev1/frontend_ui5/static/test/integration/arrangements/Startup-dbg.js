"use strict";

sap.ui.define([], function () {
  "use strict";

  /* global document */

  const startUp = {
    setUpHTMLBody() {
      document.body.style.width = '80%';
      document.body.style.left = '20%';
      document.body.style.position = 'absolute';
      if (!document.body.classList.contains('sapUiOpaBodyComponent')) {
        document.body.classList.add('sapUiOpaBodyComponent');
      }
    }
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => startUp.setUpHTMLBody());
  } else {
    startUp.setUpHTMLBody();
  }
  return startUp;
});
//# sourceMappingURL=Startup-dbg.js.map

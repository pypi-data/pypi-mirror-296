"use strict";

const serviceWorkerGlobalScope = globalThis;
// not necessary of course, just to emphasize that the globalThis is
// different from the globalThis in the web app.

serviceWorkerGlobalScope.addEventListener('install', () => {
  console.info('service-worker installed');
});
//# sourceMappingURL=service-worker-dbg.js.map

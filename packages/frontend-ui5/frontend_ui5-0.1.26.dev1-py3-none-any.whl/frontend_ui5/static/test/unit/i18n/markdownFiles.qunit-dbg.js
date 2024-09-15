"use strict";

sap.ui.define(["demo/spa/model/Lang", "sap/base/Log"], function (__demo_spa_model_Lang, Log) {
  "use strict";

  const languageModel = __demo_spa_model_Lang["languageModel"];
  const logger = Log.getLogger('test/unit/i18n/markdownFiles.qunit.ts');
  QUnit.module('i18n markdown files check');
  QUnit.test('i18n.properties', function (assert) {
    const done = assert.async();
    const storeForMarkdownStrings = [];
    const languages = languageModel.getData();
    let openGetRequests = languages.supported.length * languages.files.length;
    function fetchAndStoreInObject(filename) {
      const pathToMdFile = '../../i18n/markdown/' + filename;
      fetch(pathToMdFile).then(response => {
        assert.ok(response.status < 400, 'Found ' + filename);
        if (response.status >= 400) {
          throw new Error('File not found: ' + filename);
        }
        return response.text();
      }).then(text => {
        storeForMarkdownStrings.push(text);
        openGetRequests--;
        if (openGetRequests === 0) {
          done();
        }
      }).catch(error => logger.error(String(error)));
    }
    for (let i = 0; i < languages.supported.length; i++) {
      const lang = languages.supported[i].code;
      for (let j = 0; j < languages.files.length; j++) {
        const filename = `${languages.files[j]}_${lang}.md`;
        fetchAndStoreInObject(filename);
      }
    }
  });
});
//# sourceMappingURL=markdownFiles.qunit-dbg.js.map

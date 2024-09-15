"use strict";

sap.ui.define(["demo/spa/model/Lang", "sap/base/Log"], function (__demo_spa_model_Lang, Log) {
  "use strict";

  const languageModel = __demo_spa_model_Lang["languageModel"];
  const logger = Log.getLogger('test/unit/i18n/properties.qunit.ts');
  QUnit.module('i18n property check');
  QUnit.test('i18n.properties', function (assert) {
    const done = assert.async();
    const propFileUrl = '../../i18n/i18n.properties';
    const languages = languageModel.getData();
    let openGetRequests = languages.supported.length;
    let i18nProperties = '';
    fetch(propFileUrl).then(response => {
      assert.ok(response.status < 400, 'Found ' + propFileUrl);
      if (response.status >= 400) {
        throw new Error('File not Found.');
      }
      return response.text();
    }).then(text => {
      i18nProperties = text;
      for (const item of languages.supported) {
        checkI18nProperties(`../../i18n/i18n_${item.code}.properties`);
      }
    }).catch(error => {
      logger.error(String(error));
    });
    function checkI18nProperties(path) {
      fetch(path).then(response => {
        assert.ok(response.status < 400, 'Found ' + path);
        if (response.status >= 400) {
          throw new Error('Did not find ' + path);
        }
        return response.text();
      }).then(text => {
        assert.strictEqual(compareI18nClassifications(text, i18nProperties), 0, path + ' has the same classifications as i18n.properties');
        assert.strictEqual(compareI18ClassificationsWithAssignments(text), 0, path + ' has the same number of classifications and assignments');
        openGetRequests--;
        if (openGetRequests === 0) {
          done();
        }
      }).catch(error => {
        logger.error(String(error));
      });
    }
  });

  /**
   * Compares the classifications of two i18n properties files
   * @param propertiesA Content of the i18n properties file A
   * @param propertiesB Content of the i18n properties file B
   * @returns 0 if the classifications are equal, -1 otherwise
   */
  function compareI18nClassifications(propertiesA, propertiesB) {
    const classificationRegex = /#[X-Y][A-Z]{3}/g;
    return propertiesA.match(classificationRegex).join('') === propertiesB.match(classificationRegex).join('') ? 0 : -1;
  }

  /**
   * Compares the number of classifications with the number of assignments in the i18n properties file
   * @param i18nProperties The content of the i18n properties file
   * @returns 0 if the number of classifications and assignments are equal, -1 otherwise
   */
  function compareI18ClassificationsWithAssignments(i18nProperties) {
    i18nProperties = '\n' + i18nProperties + '\n';
    const classificationRegex = /#[X-Y][A-Z]{3}/g;
    const numOfClassifications = i18nProperties.match(classificationRegex) ? i18nProperties.match(classificationRegex).length : 0;
    const assignmentRegex = /\n\S*=.+\n/g;
    const numOfAssignments = i18nProperties.match(assignmentRegex) ? i18nProperties.match(assignmentRegex).length : 0;
    return numOfClassifications === numOfAssignments ? 0 : -1;
  }
});
//# sourceMappingURL=properties.qunit-dbg.js.map

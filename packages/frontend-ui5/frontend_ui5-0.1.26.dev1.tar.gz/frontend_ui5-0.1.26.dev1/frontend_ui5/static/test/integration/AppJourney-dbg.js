"use strict";

sap.ui.define(["demo/spa/controller/SignUp.controller", "demo/spa/controller/utils/Cookies", "demo/spa/controller/utils/FetchAPIWrapper", "demo/spa/controller/utils/Misc", "demo/spa/controller/utils/MockConnector", "sap/base/Log", "sap/ui/test/Opa5", "sap/ui/test/opaQunit", "./pages/App.page"], function (__SignUp, __demo_spa_controller_utils_Cookies, __FetchAPIWrapper, __demo_spa_controller_utils_Misc, __MockConnector, Log, Opa5, opaTest, __OnTheAppPage) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const SignUp = _interopRequireDefault(__SignUp);
  const getCSRFCookie = __demo_spa_controller_utils_Cookies["getCSRFCookie"];
  const FetchAPIWrapper = _interopRequireDefault(__FetchAPIWrapper);
  const getResourceRoot = __demo_spa_controller_utils_Misc["getResourceRoot"];
  const MockConnector = _interopRequireDefault(__MockConnector);
  const OnTheAppPage = _interopRequireDefault(__OnTheAppPage); // Preparation
  const logger = Log.getLogger('AppJourney');
  const e2eTestResultPath = '/test-results';
  const isE2ETest = window.location.search.includes('e2eTest=true');
  const onTheAppPage = new OnTheAppPage();
  const fetchAPI = new FetchAPIWrapper('/ui5');
  logger.setLevel(Log.Level.INFO);
  let version = 'UNKNOWN';
  fetchVersion();
  setTestCookie('LANG', 'en');
  MockConnector.deferResponse = false;
  QUnit.module('ToolPage Basics');
  onTheAppPage.iStartMyUIComponent({
    componentConfig: {
      name: 'demo.spa'
    },
    hash: ''
  });
  opaTest('User Action Sheet Test', function () {
    onTheAppPage.iPressTheElement('idUserButton');
    onTheAppPage.iShouldSeeTheUserActionSheet();
    onTheAppPage.iPressTheElement('idHomeNavListItem');
    onTheAppPage.theUserActionSheetShouldNotExist();
  });
  QUnit.module('Authentication Basics');
  opaTest('Login Test', function () {
    if (!getCSRFCookie()) {
      setTestCookie('csrftoken', 'dummy');
    }
    Opa5.getHashChanger().setHash('sign-in');
    onTheAppPage.iShouldSeeTheDialogWithId('idSignInDialog', onTheAppPage.signInViewName);
    onTheAppPage.iShouldSeeAnDisabledElement('idSignInButton', onTheAppPage.signInViewName);
    onTheAppPage.iSetTheInputFieldToValue('idSignInUsernameInput', 'admin', onTheAppPage.signInViewName);
    onTheAppPage.iSetTheInputFieldToValue('idSignInPasswordInput', 'this-is-an-integration-test', onTheAppPage.signInViewName);
    onTheAppPage.iShouldSeeAnEnabledElement('idSignInButton', onTheAppPage.signInViewName);
  });
  opaTest('Sign Up Test - Failed Signup', function () {
    SignUp.setInitialSignUpData({
      username: 'test-user',
      email: 'tester@abc.de',
      password: 'this-is-an-integration-test',
      password_confirmation: 'this-is-an-integration-test',
      product_key: 'INVALID_KEY'
    });
    Opa5.getHashChanger().setHash('sign-up');
    onTheAppPage.iShouldSeeTheDialogWithId('idSignUpDialog', onTheAppPage.signUpViewName);
    onTheAppPage.iShouldSeeAnEnabledElement('idSignUpButton', onTheAppPage.signUpViewName);
    onTheAppPage.iPressTheElement('idSignUpButton', onTheAppPage.signUpViewName);
    // Simulate failed sign-up in case the mockConnector is used:
    if (!isE2ETest) {
      MockConnector.nextStatusCodes.push(400);
    }
    onTheAppPage.iShouldSeeAnErrorMessageBox();
    onTheAppPage.iCanDestroyTheErrorMessageBox();
  });
  opaTest('Sign Up Test - Successful Signup', function () {
    SignUp.setInitialSignUpData({
      username: 'test-user',
      email: 'tester@abc.de',
      password: 'this-is-an-integration-test',
      password_confirmation: 'this-is-an-integration-test',
      product_key: 'VALID_KEY'
    });
    Opa5.getHashChanger().setHash('sign-up');
    onTheAppPage.iShouldSeeTheDialogWithId('idSignUpDialog', onTheAppPage.signUpViewName);
    onTheAppPage.iShouldSeeAnEnabledElement('idSignUpButton', onTheAppPage.signUpViewName);
    onTheAppPage.iPressTheElement('idSignUpButton', onTheAppPage.signUpViewName);
    onTheAppPage.iShouldNotSeeAnErrorMessageBox();
  });
  opaTest('Sign Up Test - Failed Signup - Used Product Key twice', function () {
    SignUp.setInitialSignUpData({
      username: 'test-user-2',
      email: 'tester2@abc.de',
      password: 'this-is-an-integration-test',
      password_confirmation: 'this-is-an-integration-test',
      product_key: 'VALID_KEY'
    });
    setTimeout(() => Opa5.getHashChanger().setHash(''), 100);
    setTimeout(() => Opa5.getHashChanger().setHash('sign-up'), 250);
    onTheAppPage.iShouldSeeTheDialogWithId('idSignUpDialog', onTheAppPage.signUpViewName);
    onTheAppPage.iShouldSeeAnEnabledElement('idSignUpButton', onTheAppPage.signUpViewName);
    onTheAppPage.iPressTheElement('idSignUpButton', onTheAppPage.signUpViewName);
    // Simulate failed sign-up in case the mockConnector is used:
    if (!isE2ETest) {
      MockConnector.nextStatusCodes.push(400);
    }
    onTheAppPage.iShouldSeeAnErrorMessageBox();
    onTheAppPage.iCanDestroyTheErrorMessageBox();
  });
  QUnit.module('Finalize Test');
  opaTest('Tear Down UI Component', function () {
    onTheAppPage.iAssertTrueIsTrue();
    onTheAppPage.iTeardownMyUIComponent();
    onTheAppPage.iRestoreBodyStyles();
  });
  QUnit.done(function (details) {
    const result = {
      ...details,
      version: version
    };
    logger.info('Test results: ' + JSON.stringify(result));
    if (isE2ETest) {
      fetchAPI.call('post', e2eTestResultPath, {
        ...details,
        version: version
      }, true).catch(error => {
        logger.error(String(error));
      });
    }
  });

  /**
   * Set cookie for 30 seconds for testing purposes.
   * @param key key of cookie
   * @param value value of cookie, default "true"
   */
  function setTestCookie(key) {
    let value = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'true';
    const date = new Date();
    date.setTime(date.getTime() + 30000);
    const cookieToSet = key + '=' + value + '; expires=' + date.toUTCString() + '; path=/; SameSite=Strict;';
    Opa5.getWindow().document.cookie = cookieToSet;
  }

  /**
   * Fetches the version from the app.version.json file and sets it to the global variable.
   */
  function fetchVersion() {
    const path = isE2ETest ? getResourceRoot() + 'resources/app.version.json' : '/../resources/app.version.json';
    const fetchStatic = new FetchAPIWrapper('');
    fetchStatic.call('get', path).then(response => response.json()).then(data => {
      version = String(data.version);
      logger.info('Version: ' + data.version);
    }).catch(error => {
      logger.error('Error fetching version: ' + error); // todo remove
    });
  }
});
//# sourceMappingURL=AppJourney-dbg.js.map

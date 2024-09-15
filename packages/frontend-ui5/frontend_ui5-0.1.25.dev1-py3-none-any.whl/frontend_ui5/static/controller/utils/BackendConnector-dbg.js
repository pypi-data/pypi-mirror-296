"use strict";

sap.ui.define(["./FetchAPIWrapper"], function (__FetchAPIWrapper) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const FetchAPIWrapper = _interopRequireDefault(__FetchAPIWrapper);
  /**
   * Mock API to simulate backend fetches.
   * @namespace demo.spa.controller.utils
   */
  class BackendConnector {
    constructor() {
      let apiEndpoint = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '/ui5/api';
      let pathToREST = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'rest/';
      this.API = new FetchAPIWrapper(apiEndpoint);
      this.pathToREST = pathToREST;
    }
    create(entity) {
      return this.API.call('post', `/${this.pathToREST}${entity._type}/`, entity);
    }
    delete(entity) {
      return this.API.call('delete', `/${this.pathToREST}${entity._type}/${entity.id}/`);
    }
    get(entityType, id) {
      return this.API.call('get', `/${this.pathToREST}${entityType}/${id}/`);
    }
    getAll(entityType) {
      return this.API.call('get', `/${this.pathToREST}${entityType}`);
    }
    getUserData() {
      return this.API.call('get', '/user-data');
    }
    signIn(credentials) {
      return this.API.call('post', '/sign-in', credentials, true);
    }
    signOut() {
      return this.API.call('post', '/sign-out');
    }
    signUp(signUpForm) {
      return this.API.call('post', '/sign-up', signUpForm, true);
    }
    update(entity) {
      return this.API.call('patch', `/${this.pathToREST}${entity._type}/${entity.id}/`, entity);
    }
  }
  return BackendConnector;
});
//# sourceMappingURL=BackendConnector-dbg.js.map

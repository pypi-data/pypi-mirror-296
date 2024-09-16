"use strict";

sap.ui.define(["sap/base/Log", "./Cookies"], function (Log, ___Cookies) {
  "use strict";

  const getCSRFCookie = ___Cookies["getCSRFCookie"]; // types
  /**
   * @namespace demo.spa.controller.utils
   */
  class FetchAPIWrapper {
    CSRFToken = '';
    logger = (() => Log.getLogger('FetchAPIWrapper'))();

    /**
     * Create a fetch API wrapper for convenient calls to the api endpoint
     * on the given domain.
     * Domain is set to window.location.origin if not provided.
     * @param apiEndpoint The api endpoint to call.
     * @param domain The domain to call the api endpoint on.
     * Defaults to window.location.origin.
     */
    constructor(apiEndpoint) {
      let domain = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '';
      this.logger.setLevel(Log.Level.INFO);
      this.domain = domain ? domain : window.location.origin;
      this.apiEndpoint = apiEndpoint;
    }

    /**
     * Executes a fetch to the api endpoint and given path with the given method and data.
     * Serializes the data object to form data if serialize is true.
     * @param method Method to use for the fetch.
     * @param path Path to append to the api endpoint.
     * @param data Data to send with the fetch.
     * @param serialize If true, serializes the data object to form data.
     * @returns Promise that resolves to a Response
     * or rejects to an Error or a Response with a status code >= 400.
     */
    call(method, path) {
      let data = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
      let serialize = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : false;
      let stringifiedData = '';
      if (serialize && typeof data === 'object') {
        stringifiedData = this.serialize(data);
      } else if (serialize && typeof data === 'string') {
        this.logger.warning("Can't serialize data of type string!");
      } else {
        stringifiedData = typeof data === 'string' ? data : JSON.stringify(data);
      }
      if (['post', 'delete', 'patch', 'put'].includes(method)) {
        this.CSRFToken = getCSRFCookie();
        if (!this.CSRFToken) {
          this.logger.warning('No CSRF token found!');
        }
      }
      return new Promise((resolve, reject) => {
        this[method](path, stringifiedData, serialize).then(response => {
          if (response.ok) {
            resolve(response);
          } else {
            reject(response);
          }
        }).catch(error => {
          reject(error);
        });
      });
    }

    /**
     * Executes a delete request to the api endpoint with given path with the given data.
     */
    delete(path, data) {
      return fetch(this.domain + this.apiEndpoint + path, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
          'X-CSRFToken': this.CSRFToken
        },
        body: data
      });
    }

    /**
     * Executes a get request to the api endpoint with given path.
     */
    get(path) {
      return fetch(this.domain + this.apiEndpoint + path, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json'
        }
      });
    }

    /**
     * Executes a patch request to the api endpoint with given path with the given data.
     */
    patch(path, data) {
      return fetch(this.domain + this.apiEndpoint + path, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
          'X-CSRFToken': this.CSRFToken
        },
        body: data
      });
    }

    /**
     * Executes a post request to the api endpoint with given path with the given data.
     * Serializes the data object to form data if serialize is true.
     */
    post(path, data) {
      let serialize = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
      return fetch(this.domain + this.apiEndpoint + path, {
        method: 'POST',
        headers: {
          'Content-Type': serialize ? 'application/x-www-form-urlencoded' : 'application/json',
          Accept: 'application/json',
          'X-CSRFToken': this.CSRFToken
        },
        body: data
      });
    }

    /**
     * Executes a patch request to the api endpoint with given path with the given data.
     */
    put(path, data) {
      return fetch(this.domain + this.apiEndpoint + path, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
          'X-CSRFToken': this.CSRFToken
        },
        body: data
      });
    }

    /**
     * Serializes the given object to form data.
     * @param data The object to serialize.
     * @returns The serialized form data.
     */
    serialize(data) {
      return Object.keys(data).map(key => {
        return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
      }).join('&');
    }
  }
  return FetchAPIWrapper;
});
//# sourceMappingURL=FetchAPIWrapper-dbg.js.map

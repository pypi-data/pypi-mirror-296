"use strict";

sap.ui.define(["sap/base/Log"], function (Log) {
  "use strict";

  /** Deletes all cookies */
  function deleteAllCookies() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i];
      const equals = cookie.indexOf('=');
      const name = equals > -1 ? cookie.substr(0, equals) : cookie;
      document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Strict;';
    }
  }

  /**
   * Delete cookie by key
   * @param key key of cookie
   */
  function deleteCookie(key) {
    const date = new Date(0);
    document.cookie = key + '=; expires=' + date.toUTCString() + '; path=/; SameSite=Strict;';
  }

  /**
   * Convenience wrapper for getting CSRF cookie
   */
  function getCSRFCookie() {
    return getCookie('csrftoken');
  }

  /**
   * Get cookie by key
   * @param key key of cookie
   */
  function getCookie(key) {
    const value = '; ' + document.cookie;
    const cookies = value.split('; ' + key + '=');
    if (cookies.length == 2) {
      return cookies.pop().split(';').shift();
    }
    return '';
  }

  /**
   * Returns true if cookie consent is given, false otherwise
   * @returns true if cookie consent is given, false otherwise
   */
  function getCookieConsent() {
    return getCookie('COOKIE_CONSENT') === 'true' ? true : false;
  }

  /**
   * Set cookie with name, value and expiration time
   * @param key key of cookie
   * @param value value of cookie, default "true"
   * @param expiresIn expiration time in milliseconds (defaults to one year)
   * @returns true if cookie consent is given, false otherwise
   */
  function setCookie(key) {
    let value = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'true';
    let expiresIn = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 365 * 24 * 3600 * 1000;
    const date = new Date();
    date.setTime(date.getTime() + expiresIn);
    if (key === 'COOKIE_CONSENT') {
      document.cookie = key + '=' + value + '; expires=' + date.toUTCString() + '; path=/; SameSite=Strict;';
      return true;
    } else if (getCookie('COOKIE_CONSENT')) {
      document.cookie = key + '=' + value + '; expires=' + date.toUTCString() + '; path=/; SameSite=Strict;';
      return true;
    } else {
      logger.warning('Cookie consent not given, cookie not set');
      return false;
    }
  }

  /**
   * Convenience wrapper for setting cookie consent to true
   */
  function setCookieConsent() {
    setCookie('COOKIE_CONSENT');
  }

  /**
   * Convenience wrapper for setting dummy CSRF cookie
   * For testing purposes only
   */
  function setDummyCSRFCookie() {
    setCookie('csrftoken', 'dummy');
  }

  /**
   * Convenience Wrapper for deleting cookie consent and all other cookies
   */
  function unsetCookieConsent() {
    deleteAllCookies();
  }
  const logger = Log.getLogger('controller/utils/Cookies');
  var __exports = {
    __esModule: true
  };
  __exports.deleteAllCookies = deleteAllCookies;
  __exports.deleteCookie = deleteCookie;
  __exports.getCSRFCookie = getCSRFCookie;
  __exports.getCookie = getCookie;
  __exports.getCookieConsent = getCookieConsent;
  __exports.setCookie = setCookie;
  __exports.setCookieConsent = setCookieConsent;
  __exports.setDummyCSRFCookie = setDummyCSRFCookie;
  __exports.unsetCookieConsent = unsetCookieConsent;
  return __exports;
});
//# sourceMappingURL=Cookies-dbg.js.map

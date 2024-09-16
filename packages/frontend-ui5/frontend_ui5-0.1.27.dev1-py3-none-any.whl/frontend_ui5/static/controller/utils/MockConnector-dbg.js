"use strict";

sap.ui.define(["sap/base/Log", "./MockDataProvider", "./Random"], function (Log, __MockDataProvider, __Random) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const MockDataProvider = _interopRequireDefault(__MockDataProvider);
  const Random = _interopRequireDefault(__Random);
  /**
   * Mock API to simulate backend fetches.
   * @namespace demo.spa.controller.utils
   */
  class MockConnector {
    static deferResponse = false;
    /** Status codes for coming mock responses */
    static nextStatusCodes = (() => [])();

    /** Logger for the MockConnector */
    logger = (() => Log.getLogger('MockConnector'))();
    mockDataProvider = (() => new MockDataProvider())();
    random = (() => new Random(12345))();
    constructor() {
      this.logger.setLevel(Log.Level.INFO);
    }
    create(entity) {
      return this.createMockResponse(entity, true);
    }
    delete(entity) {
      return this.createMockResponse(entity);
    }
    get(entityType, id) {
      return this.createMockResponse({
        id: id,
        _type: entityType
      });
    }
    getAll(type) {
      return this.createMockResponse({
        id: '',
        _type: 'mock-list-' + type
      }); // todo make enhance type safety
    }
    getUserData() {
      return this.createMockResponse({
        id: '',
        _type: 'mock-data'
      });
    }
    signIn(credentials) {
      return this.createMockResponse({
        username: credentials.username,
        user_id: 'id-mock-user',
        password: credentials.password
      });
    }
    signOut() {
      return this.createMockResponse({
        id: '',
        _type: 'mock-data'
      });
    }
    signUp(signUpForm) {
      return this.createMockResponse({
        username: signUpForm.username,
        user_id: 'id-mock-user',
        password: signUpForm.password
      });
    }
    update(entity) {
      return this.createMockResponse(entity);
    }

    /**
     * Creates a mock response for the given entity.
     * @param entity The entity to create the response for.
     * @param assignId Whether to assign an id to the entity.
     * @returns A promise that resolves to a Response or rejects to an Error or a Response with a status code >= 400.
     */
    createMockResponse(entity, assignId) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const entityCopy = {
            ...entity
          };
          if (assignId) {
            entityCopy.id = String(this.random.randIntBetween(100000, 999999));
          }
          let statusCode = 200;
          if (MockConnector.nextStatusCodes.length > 0) {
            statusCode = MockConnector.nextStatusCodes.shift();
            this.logger.info(`MockConnector: next status code is ${statusCode}`);
          }
          if (statusCode >= 400) {
            reject(new Response(JSON.stringify(entityCopy), {
              status: statusCode
            }));
          } else if (statusCode >= 200) {
            if (entityCopy._type === 'mock-list-person') {
              resolve(toDRFResponse(this.mockDataProvider.generateRandomPersons(), statusCode));
            } else if (entityCopy._type === 'mock-list-appointment') {
              resolve(toDRFResponse(this.mockDataProvider.generateRandomAppointments(), statusCode));
            } else if (entityCopy._type === 'mock-list-slot') {
              resolve(toDRFResponse(this.mockDataProvider.generateRandomSlots(), statusCode));
            } else if (entity.username) {
              // request is a sign in or sign up
              const generatedUser = this.mockDataProvider.generateRandomPersons().find(person => person.key == entity.username);
              if (generatedUser) {
                const username = generatedUser.first_name + ' ' + generatedUser.last_name;
                if (entity.password.replaceAll(' ', '').toLowerCase() != username.replaceAll(' ', '').toLowerCase()) {
                  reject(new Response(JSON.stringify(entityCopy), {
                    status: 401
                  }));
                }
                if (entity.password) resolve(new Response(JSON.stringify({
                  username: username,
                  user_id: generatedUser.related_user
                }), {
                  status: statusCode
                }));
              } else {
                resolve(new Response(JSON.stringify(entityCopy), {
                  status: statusCode
                }));
              }
            }
            resolve(new Response(JSON.stringify(entityCopy), {
              status: statusCode
            }));
          } else if (statusCode === -1) {
            // will be treated as a connection error
            reject(new TypeError('NetworkError when attempting to fetch resource.'));
          } else if (statusCode === -2) {
            // will be treated as an unknown error
            reject(new Error('Test Error from MockConnector'));
          }
        }, MockConnector.deferResponse ? this.random.random() * 1500 : 0);
      });
    }
  }

  /**
   * Convenience function to convert an array of CustomModelEntityBase to
   * a mock Django REST Framework (DRF) response.
   */
  function toDRFResponse(data, statusCode) {
    return new Response(JSON.stringify({
      count: 0,
      next: null,
      previous: null,
      results: data
    }), {
      status: statusCode
    });
  }
  return MockConnector;
});
//# sourceMappingURL=MockConnector-dbg.js.map

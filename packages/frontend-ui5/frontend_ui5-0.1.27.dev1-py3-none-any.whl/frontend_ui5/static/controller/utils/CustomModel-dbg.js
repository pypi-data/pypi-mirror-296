"use strict";

sap.ui.define(["sap/base/Log", "sap/base/assert", "sap/ui/model/json/JSONModel", "./BackendConnector", "./Formatters", "./Misc", "./MockConnector"], function (Log, assert, JSONModel, __BackendConnector, ___Formatters, ___Misc, __MockConnector) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const BackendConnector = _interopRequireDefault(__BackendConnector);
  const dateTimeReviver = ___Formatters["dateTimeReviver"];
  const equals = ___Misc["equals"];
  const MockConnector = _interopRequireDefault(__MockConnector);
  /**
   * @namespace demo.spa.controller.utils
   */
  const CustomModel = JSONModel.extend("demo.spa.controller.utils.CustomModel", {
    /**
     * Constructor for the CustomModel - a model that is basically
     * a JSONModel with a backend connection
     * @param initialData JS object to for initializing the JSONModel
     */
    constructor: function _constructor(initialData) {
      JSONModel.prototype.constructor.call(this, initialData, true);
      this.initialData = {};
      /** Logger for the CustomModel */
      this.logger = Log.getLogger(CustomModel.prototype.getMetadata().getName());
      this.id = CustomModel.modelCounter;
      CustomModel.modelCounter++;
      this.setUpConnector();
      this.initialData = {
        ...initialData
      };
    },
    reset: function _reset() {
      this.setData({
        ...this.initialData
      });
      this.updateBindings(true);
    },
    setUpConnector: function _setUpConnector() {
      const params = new URLSearchParams(window.location.search);
      const useMockConnector = params.get('useMockConnector') == 'true';
      if (useMockConnector) {
        this.connector = new MockConnector();
      } else {
        this.connector = new BackendConnector();
      }
    },
    attachModelChangedHandler: function _attachModelChangedHandler(f) {
      this.attachEvent(`customModel${this.id}changed`, f);
    },
    attachModelChangedHandlerOnce: function _attachModelChangedHandlerOnce(f) {
      this.attachEventOnce(`customModel${this.id}changed`, f);
    },
    /**
     * Creates the given entity on the backend and adds it to the model if successful.
     * @param entity The entity to create.
     * @param onFinish Callback to execute after the creation is finished.
     * The callback is executed regardless of whether the creation was successful.
     */
    create: function _create(entity) {
      let onFinish = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : () => null;
      this.checkEntity(entity);
      this.connector.create(entity).then(result => {
        if (result instanceof Response && result.ok) {
          result.text().then(jsonString => {
            const toCreate = JSON.parse(jsonString, dateTimeReviver);
            this._create(toCreate);
            onFinish();
            this.fireModelChangedEvent(entity._type);
          }).catch(error => {
            this._failureMessageHandler.bind(this)(error);
            onFinish();
          });
        } else {
          this._failureMessageHandler.bind(this)(result);
          onFinish();
        }
      }).catch(error => {
        this._failureMessageHandler.bind(this)(error);
        onFinish();
      });
    },
    /**
     * Requests deletion from the backend and deletes the entity from the model if successful.
     * @param entity The entity to delete.
     * @param onFinish A callback to execute after the deletion is finished.
     * The callback is executed regardless of whether the deletion was successful.
     */
    delete: function _delete(entity) {
      let onFinish = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : () => null;
      this.checkEntity(entity);
      this.connector.delete(entity).then(result => {
        if (result instanceof Response && result.ok) {
          this._delete(entity);
          this.fireModelChangedEvent(entity._type);
        } else {
          this._failureMessageHandler.bind(this)(result);
        }
        onFinish();
      }).catch(error => {
        this._failureMessageHandler.bind(this)(error);
        onFinish();
      });
    },
    /**
     * Fetches the user data for the given entity types and updates the model.
     * @param entityTypes The entity types to fetch
     */
    fetch: function _fetch(entityTypes) {
      let onFinish = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : () => null;
      for (const entityType of entityTypes) {
        this.connector.getAll(entityType).then(response => {
          if (response instanceof Response) {
            return response.text();
          } else {
            throw response;
          }
        }).then(text => {
          const response = JSON.parse(text, dateTimeReviver);
          this.setProperty(`/${entityType}_list`, response.results);
          this.logger.debug(`Fetched ${entityType}_list data: ${response.results.length} entries`);
          this.updateBindings(true);
          this.fireModelChangedEvent(entityType);
        }).catch(error => {
          this._failureMessageHandler.bind(this)(error);
          onFinish();
        });
      }
    },
    fireModelChangedEvent: function _fireModelChangedEvent(entityName) {
      this.fireEvent(`customModel${this.id}changed`, {
        entityName: entityName
      });
    },
    /**
     * Returns a copy if the entity with the given id from the model if it exists.
     * Else returns null.
     */
    get: function _get(entityType, id) {
      const entity = this._get({
        id: id,
        _type: entityType
      });
      return entity ? Object.assign({}, entity) : null;
    },
    /**
     * Sets a custom message handler for displaying error messages that occur
     * during the communication with the backend to the user.
     */
    setFailureMessageHandler: function _setFailureMessageHandler(failureMessageHandler) {
      this._failureMessageHandler = failureMessageHandler;
    },
    /**
     * Updates the given entity on the backend
     * and updates the entity in the model if successful.
     */
    update: function _update(entity) {
      let onFinish = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : () => null;
      this.checkEntity(entity);
      const currentEntity = this.get(entity._type, entity.id);
      if (equals(entity, currentEntity)) {
        this.logger.debug(`${JSON.stringify(entity)} equals ${JSON.stringify(this._get(entity))}`);
        onFinish();
        return;
      }
      this.connector.update(entity).then(result => {
        if (result instanceof Response && result.ok) {
          result.text().then(jsonString => {
            const toUpdate = JSON.parse(jsonString, dateTimeReviver);
            assert(equals(toUpdate, entity), "The updated entity doesn't match the response: " + jsonString + ' \n\n' + JSON.stringify(entity));
            this._update(toUpdate);
            this.fireModelChangedEvent(entity._type);
            onFinish();
          }).catch(error => {
            this._failureMessageHandler.bind(this)(error);
            onFinish();
          });
        } else {
          this._failureMessageHandler.bind(this)(result);
          onFinish();
        }
      }).catch(error => {
        this._failureMessageHandler.bind(this)(error);
        onFinish();
      });
    },
    /**
     * Adds the entity to the suitable collection in the model.
     */
    _create: function _create2(entity) {
      const collectionKey = `${entity._type}_list`;
      const entities = this.getProperty('/' + collectionKey);
      this.setProperty('/' + collectionKey, [...entities, entity]);
    },
    /**
     * Deletes the entity that has the same id as the given entity from the model.
     */
    _delete: function _delete2(entity) {
      const collectionKey = `${entity._type}_list`;
      const filtered = this.getProperty('/' + collectionKey).filter(item => item.id !== entity.id);
      this.setProperty('/' + collectionKey, filtered);
    },
    /**
     * Handles failures that occur during the communication with the backend. You can
     * override this method to customize the error handling by using the method setMessageHandler.
     */
    _failureMessageHandler: function _failureMessageHandler(informationCarrier) {
      this.logger.error(String(informationCarrier));
    },
    /**
     * Returns entity from model that has same id and type as the given entity.
     */
    _get: function _get2(entity) {
      const collectionKey = `${entity._type}_list`;
      const customEntity = this.getProperty('/' + collectionKey).find(item => item.id === entity.id);
      return customEntity || null;
    },
    /**
     * Updates the entity in the model that has the same id and type as the given entity
     * with the values of the given entity.
     */
    _update: function _update2(entity) {
      Object.assign(this._get(entity), entity);
      this.updateBindings(true);
    },
    /**
     * Checks if the given entity is processable by the model.
     * Only for debugging purpose - logs failed assertions.
     * @param entity The entity to check.
     */
    checkEntity: function _checkEntity(entity) {
      const collectionKey = `${entity._type}_list`;
      assert(Boolean(entity._type), `Entity type not set: ${JSON.stringify(entity)}`);
      assert(Boolean(this.getProperty('/' + collectionKey)), `Collection for ${entity._type} not found in model.` + ' ### ' + JSON.stringify(this.getData()));
    }
  });
  CustomModel.modelCounter = 0;
  return CustomModel;
});
//# sourceMappingURL=CustomModel-dbg.js.map

"use strict";

sap.ui.define(["sap/base/Log", "sap/m/MessageBox", "sap/m/MessageToast", "./BaseController", "./utils/Comparators", "./utils/Formatters"], function (Log, MessageBox, MessageToast, __BaseController, ___utils_Comparators, ___utils_Formatters) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const BaseController = _interopRequireDefault(__BaseController);
  const comparePersons = ___utils_Comparators["comparePersons"];
  const getEmailAddressErrorState = ___utils_Formatters["getEmailAddressErrorState"];
  const isValidEmailAddress = ___utils_Formatters["isValidEmailAddress"];
  const trimValuesShallow = ___utils_Formatters["trimValuesShallow"];
  /**
   * @namespace demo.spa.controller
   */
  const Team = BaseController.extend("demo.spa.controller.Team", {
    constructor: function constructor() {
      BaseController.prototype.constructor.apply(this, arguments);
      this.comparePersons = comparePersons;
      /** Formatter for the email field */
      this.getEmailAddressErrorState = getEmailAddressErrorState;
      /** Logger for the team controller. */
      this.logger = Log.getLogger(Team.getMetadata().getName());
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    /**
     * Deletes the person item from the member list and the corresponding entity from the model.
     */
    deletePerson: function _deletePerson(person) {
      this.teamMemberDialog.setBusy(true);
      const teamMembersBefore = this.getUserDataModel().getProperty('/person_list').length;
      const onFinish = () => {
        this.teamMemberDialog.setBusy(false);
        this.teamMemberDialog.close();
        if (this.getUserDataModel().getProperty('/person_list').length !== teamMembersBefore) {
          this.getUserDataModel().fetch(['person', 'slot', 'appointment']);
        }
      };
      this.getUserDataModel().delete(person, onFinish);
    },
    /**
     * Returns the access link for the given person.
     * The access link is the URL to the access page with the user key of the given person.
     */
    getAccessLink: function _getAccessLink(person) {
      try {
        const origin = window.location.origin;
        const hash = this.getRouter().getURL('ACCESS FULLSCREEN', {
          userKey: person.key
        });
        const search = window.location.search;
        const pathname = window.location.pathname;
        return `${origin}${pathname}${search}#${hash}`;
      } catch (error) {
        this.logger.debug(String(error)); // just applies to yet-to-create persons, so no need to log
        return '';
      }
    },
    /** Called when the user clicks the add member button. */onAddPersonPress: function _onAddPersonPress() {
      this.setPersonFormData({
        _type: 'person',
        id: null,
        first_name: '',
        last_name: '',
        email: ''
      });
      this.openTeamMemberDialog();
    },
    onDeletePersonPress: function _onDeletePersonPress() {
      const personId = this.getFrontendModel().getProperty('/personForm/id');
      const person = this.getUserDataModel().get('person', personId);
      if (person.related_user === django.user_id) {
        MessageToast.show('Sie können sich nicht selbst löschen.'); // todo i18n
        return;
      }
      const fullName = person.first_name + ' ' + person.last_name;
      this.createConfirmation('team.txtConfirmDeletion', [fullName], () => this.deletePerson(person));
    },
    /** Called when the user clicks the add member button. */onDialogCreate: function _onDialogCreate() {
      this.teamMemberDialog.setBusy(true);
      const personToCreate = this.getPersonFormData();
      if (!this.checkPersonFormInput(personToCreate.first_name, personToCreate.last_name, personToCreate.email)) {
        this.onDialogClose();
        return;
      } else {
        this.getUserDataModel().create(personToCreate, () => this.onDialogClose());
      }
    },
    /** Called when the user clicks the save changes of member entry button. */onDialogSave: function _onDialogSave() {
      const personToUpdate = this.getPersonFormData();
      this.teamMemberDialog.setBusy(true);
      if (!this.checkPersonFormInput(personToUpdate.first_name, personToUpdate.last_name, personToUpdate.email)) {
        this.onDialogClose();
        return;
      } else {
        this.getUserDataModel().update(personToUpdate, () => this.onDialogClose());
      }
    },
    /** Called when the user clicks on a list item in the member list. */onPersonEditPress: function _onPersonEditPress(event) {
      const selectedPerson = event.getSource().getCustomData()[0].getValue();
      this.setPersonFormData(selectedPerson);
      this.openTeamMemberDialog();
    },
    onPersonListItemPress: function _onPersonListItemPress(event) {
      const selectedPerson = event.getSource().getCustomData()[0].getValue();
      if (selectedPerson.related_user != django.user_id) {
        this.setPersonFormData(selectedPerson);
        this.openCollaborationDialog();
      }
    },
    /**
     * Checks if the data of the given person meets the requirements. Returns true if so, false otherwise.
     */
    checkPersonFormInput: function _checkPersonFormInput(firstName, lastName, emailAddress) {
      const emailIsValid = isValidEmailAddress(emailAddress) || emailAddress === '';
      const nameIsNotEmpty = (firstName + lastName).trim() !== '';
      return emailIsValid && nameIsNotEmpty;
    },
    /** Creates a confirmation dialog. Performs onConfirm if the user confirms. */createConfirmation: function _createConfirmation(i18nKey, placeholder, onConfirm) {
      void this.getI18nBundle().then(bundle => {
        const confirmationText = bundle.getText(i18nKey, placeholder);
        MessageBox.confirm(confirmationText, {
          actions: [MessageBox.Action.YES, MessageBox.Action.NO],
          emphasizedAction: MessageBox.Action.YES,
          onClose: action => {
            if (action == MessageBox.Action.YES) {
              onConfirm();
            }
          }
        });
      });
    },
    /** Creates and returns a person based on the data in the person form. */getPersonFormData: function _getPersonFormData() {
      const person = this.getFrontendModel().getProperty('/personForm');
      return trimValuesShallow({
        ...person
      });
    },
    /** Closes the dialog and removes the busy indicator. */onDialogClose: function _onDialogClose() {
      if (this.teamCollaborationDialog) {
        this.teamCollaborationDialog.setBusy(false);
        this.teamCollaborationDialog.close();
      }
      if (this.teamMemberDialog) {
        this.teamMemberDialog.setBusy(false);
        this.teamMemberDialog.close();
      }
    },
    openCollaborationDialog: function _openCollaborationDialog() {
      if (!this.teamCollaborationDialog) {
        this.loadFragment({
          name: 'demo.spa.view.TeamCollaborationDialog'
        }).then(dialog => {
          this.teamCollaborationDialog = dialog;
          // this.teamMemberDialog.attachAfterOpen(() => ()); // todo set focus
          this.teamCollaborationDialog.open();
        }).catch(error => {
          this.logger.error(String(error));
        });
      } else {
        this.teamCollaborationDialog.open();
      }
    },
    /**
     * Creates a dialog to add or change team members in case it does not exist yet.
     * Opens the dialog in any case.
     * The dialog is a change dialog if the property frontend>personForm/id is set
     * to a value other than null, undefined or an empty string.
     * Otherwise the dialog is an add member dialog.
     */
    openTeamMemberDialog: function _openTeamMemberDialog() {
      if (!this.teamMemberDialog) {
        this.loadFragment({
          name: 'demo.spa.view.TeamDialog'
        }).then(dialog => {
          this.teamMemberDialog = dialog;
          this.teamMemberDialog.attachAfterOpen(() => this.setTeamMemberDialogFocus());
          this.teamMemberDialog.open();
        }).catch(error => {
          this.logger.error(String(error));
        });
      } else {
        this.teamMemberDialog.open();
      }
    },
    /** Sets the data of the person form to the data of the given person. */setPersonFormData: function _setPersonFormData(person) {
      this.getFrontendModel().setProperty('/personForm', {
        ...person
      });
    },
    setTeamMemberDialogFocus: function _setTeamMemberDialogFocus() {
      const firstNameInput = this.byId('idFirstNameInput');
      firstNameInput.focus();
    }
  });
  return Team;
});
//# sourceMappingURL=Team-dbg.controller.js.map

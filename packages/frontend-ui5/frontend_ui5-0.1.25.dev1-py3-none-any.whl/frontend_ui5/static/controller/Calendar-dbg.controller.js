"use strict";

sap.ui.define(["canvas-confetti", "sap/base/assert", "sap/m/library", "sap/m/MessageToast", "sap/ui/Device", "./BaseController", "./utils/Comparators", "./utils/Cookies", "./utils/Formatters", "./utils/Time"], function (__confetti, assert, sap_m_library, MessageToast, Device, __BaseController, ___utils_Comparators, ___utils_Cookies, ___utils_Formatters, ___utils_Time) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const confetti = _interopRequireDefault(__confetti);
  const getLocale = sap_m_library["getLocale"];
  const getLocaleData = sap_m_library["getLocaleData"];
  const BaseController = _interopRequireDefault(__BaseController);
  const comparePersons = ___utils_Comparators["comparePersons"];
  const getCookie = ___utils_Cookies["getCookie"];
  const getCSRFCookie = ___utils_Cookies["getCSRFCookie"];
  const setCookie = ___utils_Cookies["setCookie"];
  const adjustDate = ___utils_Formatters["adjustDate"];
  const dateFitsInSlots = ___utils_Time["dateFitsInSlots"];
  const dateToNextMonday = ___utils_Time["dateToNextMonday"];
  const dateToPreviousMonday = ___utils_Time["dateToPreviousMonday"];
  const dateToPreviousSunday = ___utils_Time["dateToPreviousSunday"];
  const findBetterStartDate = ___utils_Time["findBetterStartDate"];
  const hasConflictingAppointments = ___utils_Time["hasConflictingAppointments"];
  /**
   * @namespace demo.spa.controller
   */
  const Calendar = BaseController.extend("demo.spa.controller.Calendar", {
    constructor: function constructor() {
      BaseController.prototype.constructor.apply(this, arguments);
      this.comparePersons = comparePersons;
      this.appointmentTypeGreen = 'Type08';
      this.appointmentTypeOrange = 'Type01';
      this.appointmentTypeRed = 'Type02';
      this.lastTappedEndDate = new Date(new Date().toISOString().split('T')[0] + 'T11:00:00Z');
      this.lastTappedStartDate = new Date(new Date().toISOString().split('T')[0] + 'T10:00:00Z');
      this.magicButtonTimeout = 7500;
      this.mousePosition = {
        x: 0,
        y: 0
      };
      this.timeoutCount = 0;
    },
    _: function _() {
      this.onInit(); // just a bookmark
    },
    formatAppointmentText: async function _formatAppointmentText(startDate, endDate, participants) {
      const timeStr = this.formatDatePair(startDate, endDate);
      const participantsAbbr = await this.getBundleText('calendar.participantsAbbr');
      return timeStr + `\n(${participants.length} ${participantsAbbr})`;
    },
    formatAppointmentType: function _formatAppointmentType(appointment, allSlots, allAppointments) {
      let color = this.appointmentTypeGreen;
      if (!dateFitsInSlots(appointment, allSlots)) {
        color = this.appointmentTypeOrange;
      }
      if (hasConflictingAppointments(appointment, allAppointments)) {
        color = this.appointmentTypeRed;
      }
      return color;
    },
    /**
     * Formats pair of dates to a string of the format 'HH:mm - HH:mm'
     */
    formatDatePair: function _formatDatePair(startDate, endDate) {
      const formatter = date => date.toLocaleTimeString('de').slice(0, 5);
      if (endDate.getTime() - startDate.getTime() <= 3600000) {
        return `${formatter(startDate)} - ${formatter(endDate)}`;
      }
      return `${formatter(startDate)} -\n${formatter(endDate)}`;
    },
    /**
     * Formatter for checkbox state. Returns true if
     * the person's id is in the participants list.
     * @param personId The id of the person to check.
     */
    getPersonSelected: function _getPersonSelected(personId) {
      if (this.getFrontendModel().getProperty('/appointmentForm/participants').includes(personId)) {
        return true;
      }
      return false;
    },
    getSlotType: function _getSlotType(is_preferred) {
      return is_preferred ? 'Type08' : 'Type09';
    },
    /**
     * Converts a list of person ids to a string of person names.
     */
    idsToPersonNames: function _idsToPersonNames(ids) {
      if (!Array.isArray(ids)) {
        ids = [ids];
      }
      const persons = this.getUserDataModel().getProperty('/person_list');
      const filtered = persons.filter(person => ids.includes(person.id));
      filtered.sort(comparePersons);
      let resultStr = filtered.map(person => person.first_name + ' ' + person.last_name).join(', ');
      resultStr = resultStr.replaceAll(' ,', ',').replaceAll('  ', ' ').trim();
      return resultStr;
    },
    onAppointmentImprovePress: function _onAppointmentImprovePress() {
      if (this.getFrontendModel().getProperty('/improveAppointmentPressed')) {
        MessageToast.show('Tippe für einen Verbesserungsvorschlag auf einen Termin'); // todo i18n
        this.setTimerForImproveAppointment();
      }
    },
    onCalendarItemChange: function _onCalendarItemChange(event) {
      const selectedItemId = event.getParameter('appointment').getKey();
      const _type = this.type === 'appointments' ? 'appointment' : 'slot';
      const entry = this.getUserDataModel().get(_type, selectedItemId);
      entry.start_date = event.getParameter('startDate');
      entry.end_date = event.getParameter('endDate');
      if (this.type === 'availability' && !this.validateSlot(entry)) {
        void this.getBundleText('calendar.slotOverlap').then(text => MessageToast.show(text));
        return;
      }
      this.getUserDataModel().update(entry);
    },
    onCalendarItemCreate: function _onCalendarItemCreate(event) {
      if (this.type === 'availability') {
        this.handleCreateSlot(event);
      } else {
        this.handleCreateAppointment(event);
      }
    },
    onCalendarItemCreateButtonPress: function _onCalendarItemCreateButtonPress() {
      if (this.type === 'availability') {
        this.handleCreateBtnSlotPress();
      } else {
        this.handleCreateBtnAppointmentPress();
      }
    },
    onCalendarItemSelect: function _onCalendarItemSelect(event) {
      if (this.type === 'availability') {
        this.handleSelectSlot(event);
      } else {
        this.handleSelectAppointment(event);
      }
    },
    onCancelDialog: function _onCancelDialog() {
      this.calendarItemDialog.close();
    },
    onCellPress: function _onCellPress(event) {
      const startDate = adjustDate(event.getParameter('startDate'));
      const endDate = adjustDate(event.getParameter('endDate'));
      this.lastTappedStartDate = startDate;
      this.lastTappedEndDate = endDate;
    },
    onChoosePersonDialogOk: function _onChoosePersonDialogOk() {
      this.personDialog.destroy();
      this.personDialog = null;
    },
    onDeleteDialog: function _onDeleteDialog() {
      this.calendarItemDialog.setBusy(true);
      const pathToId = this.type === 'appointments' ? '/appointmentForm/id' : '/availabilityForm/id';
      const _type = this.type === 'appointments' ? 'appointment' : 'slot';
      const toDelete = {
        _type: _type,
        id: this.getFrontendModel().getProperty(pathToId)
      };
      assert(Boolean(toDelete.id), 'No id to delete found');
      this.getUserDataModel().delete(toDelete, () => {
        this.calendarItemDialog.setBusy(false);
        this.calendarItemDialog.close();
        this.getFrontendModel().setProperty(pathToId, '');
      });
    },
    onFullDayToggleBtnPress: function _onFullDayToggleBtnPress() {
      setCookie('CALENDAR_SHOW_24_HOURS', String(this.getFrontendModel().getProperty('/show24hCalendar')));
    },
    onInit: function _onInit() {
      BaseController.prototype.onInit.call(this);
      this.type = this.getView().getId().includes('availability') ? 'availability' : 'appointments';
      this.calendar = this.byId('idCalendar');
      this.attachRouteMatchedEvent();
      this.getUserDataModel().attachModelChangedHandler(() => this.applyFilter());
      this.adjustViewForSmallScreens();
      this.initCalendarSettings();
      this.setCalenderViewChangeHandlers();
      this.initMouseObserver();
    },
    onPersonSelectionChange: function _onPersonSelectionChange(event) {
      const selectedItems = event.getSource().getSelectedItems();
      const selectedPersons = selectedItems.map(item => {
        return item.getCustomData()[0].getValue();
      });
      this.getFrontendModel().setProperty('/appointmentForm/participants', selectedPersons);
    },
    onPreferredPress: function _onPreferredPress(event) {
      const key = event.getSource().getKey();
      if (key == 'yes') {
        this.getFrontendModel().setProperty('/availabilityForm/is_preferred', true);
      } else {
        this.getFrontendModel().setProperty('/availabilityForm/is_preferred', false);
      }
    },
    onRefreshPress: function _onRefreshPress() {
      this.getUserDataModel().fetch(['appointment', 'person', 'slot']);
    },
    onSaveBtnPress: function _onSaveBtnPress() {
      this.calendarItemDialog.setBusy(true);
      const finalize = () => {
        this.calendarItemDialog.setBusy(false);
        this.calendarItemDialog.close();
      };
      let modelEntry;
      if (this.type === 'appointments') {
        modelEntry = this.formDataToAppointment();
        if (!modelEntry.participants.length) {
          void this.getBundleText('calendar.noParticipants').then(text => MessageToast.show(text));
          finalize();
          return;
        }
        const suggestions = this.getFrontendModel().getProperty('/appointmentTitleSuggestions');
        if (!suggestions.includes(modelEntry.title)) {
          suggestions.push(modelEntry.title);
        }
      } else {
        modelEntry = this.formDataToSlot();
        if (!this.validateSlot(modelEntry)) {
          void this.getBundleText('calendar.slotOverlap').then(text => MessageToast.show(text));
          finalize();
          return;
        }
      }
      if (modelEntry.id) {
        this.getUserDataModel().update(modelEntry, () => finalize());
      } else {
        this.getUserDataModel().create(modelEntry, () => finalize());
      }
    },
    onSwitchToAppointmentsPress: function _onSwitchToAppointmentsPress() {
      const selectedPerson = this.getFrontendModel().getProperty('/lastChosenPerson');
      void this.getRouter().getHashChanger().setHash('appointments/' + selectedPerson);
    },
    onSwitchToAvailabilityPress: function _onSwitchToAvailabilityPress() {
      const selectedPerson = this.getFrontendModel().getProperty('/lastChosenPerson');
      void this.getRouter().getHashChanger().setHash('availability/' + selectedPerson);
    },
    /**
     * Opens the Appointment dialog.
     * Creates the dialog if it does not exist yet.
     */
    openCalendarItemDialog: function _openCalendarItemDialog() {
      if (!getCSRFCookie()) {
        void this.noCSRFTokenMessageBox();
        return;
      } else if (this.calendarItemDialog) {
        this.calendarItemDialog.open();
      } else {
        const fragmentPath = this.type === 'appointments' ? 'demo.spa.view.AppointmentDialog' : 'demo.spa.view.AvailabilityDialog';
        this.loadFragment({
          name: fragmentPath
        }).then(dialog => {
          this.calendarItemDialog = dialog;
          this.calendarItemDialog.open();
          this.calendarItemDialog.attachAfterOpen(() => {
            this.setAppointmentDialogFocus();
          });
        }).catch(error => {
          this.logger.error(String(error));
        });
      }
    },
    openPersonDialog: function _openPersonDialog() {
      if (this.personDialog) {
        this.personDialog.open();
      } else {
        this.loadFragment({
          name: 'demo.spa.view.ChoosePersonDialog'
        }).then(dialog => {
          this.personDialog = dialog;
          this.personDialog.open();
        }).catch(error => {
          this.logger.error(String(error));
        });
      }
    },
    /**
     * Validates the AppointmentForm.
     * @returns True if the form is valid, false otherwise.
     */
    validateCalendarItemForm: function _validateCalendarItemForm(date, startTime, endTime, participants) {
      const startTimeTimestamp = new Date(date + 'T' + startTime + 'Z').getTime();
      const endTimeTimestamp = new Date(date + 'T' + endTime + 'Z').getTime();
      if (participants && participants.length === 0) {
        MessageToast.show('Wähle mindestens einen Teilnehmer aus.'); // todo i18n
        return false;
      }
      if (isNaN(startTimeTimestamp) || isNaN(endTimeTimestamp)) {
        return false;
      }
      return true;
    },
    /**
     * Adjusts the start date of the calendar to the first day of the week if the
     * view is a WeekView or WorkWeekView.
     */
    adjustCalendarStartDay: function _adjustCalendarStartDay() {
      const dayOffset = this.getCalendarViewOffset(this.getCalendarViewName());
      const currentStartDay = this.calendar.getStartDate();
      const firstDayOfWeek = this.calendar.getFirstDayOfWeek();
      if (dayOffset == 5) {
        if (firstDayOfWeek == 0 && currentStartDay.getDay() == 0) {
          this.calendar.setStartDate(dateToNextMonday(currentStartDay));
        } else {
          this.calendar.setStartDate(dateToPreviousMonday(currentStartDay));
        }
      } else if (dayOffset == 7) {
        if (firstDayOfWeek == 0) {
          this.calendar.setStartDate(dateToPreviousSunday(currentStartDay));
        } else {
          this.calendar.setStartDate(dateToPreviousMonday(currentStartDay));
        }
      }
      setCookie('CALENDAR_START_DATE', this.calendar.getStartDate().toISOString());
    },
    /**
     * Adjusts the view for small screens. Shows the day view since it is
     * the view that fits best on small screens.
     */
    adjustViewForSmallScreens: function _adjustViewForSmallScreens() {
      if (Device.resize.width <= 900) {
        const dayView = this.byId('idDayView');
        this.calendar.setSelectedView(dayView);
      } else if (Device.resize.width <= 1200) {
        const workWeekView = this.byId('idWorkWeekView');
        this.calendar.setSelectedView(workWeekView);
      }
    },
    applyFilter: function _applyFilter() {
      let includeAll = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;
      if (this.type === 'appointments') {
        this.filterAppointments(includeAll);
      } else {
        this.filterSlots();
      }
    },
    attachRouteMatchedEvent: function _attachRouteMatchedEvent() {
      this.getRouter().attachRouteMatched(event => {
        const routeName = event.getParameter('name');
        if (['APPOINTMENTS INDIVIDUAL', 'AVAILABILITY INDIVIDUAL'].includes(routeName)) {
          this.initCalendarSettings();
          const personId = event.getParameter('arguments').personId;
          this.getFrontendModel().setProperty('/lastChosenPerson', personId);
          if (!this.idsToPersonNames(personId)) {
            // this is a workaround for the problem that you don't know
            // if a personId is invalid or the model is not fully loaded
            setTimeout(() => {
              if (!this.idsToPersonNames(personId)) {
                const viewNameToNavigateTo = this.type === 'appointments' ? 'APPOINTMENTS' : 'AVAILABILITY';
                this.getRouter().navTo(viewNameToNavigateTo);
                this.getRouter().fireEvent('navigateBackToValidRoute');
              } else {
                this.getFrontendModel().updateBindings(true);
              }
            }, 750);
            this.applyFilter();
          } else {
            this.applyFilter();
          }
          if (routeName.startsWith('APPOINTMENTS')) {
            this.getFrontendModel().setProperty('/expandAppointmentNavListItem', true);
            this.getFrontendModel().setProperty('/expandAvailabilityNavListItem', false);
            this.getFrontendModel().setProperty('/selectedCalendarType', 'appointments');
          } else {
            this.getFrontendModel().setProperty('/expandAppointmentNavListItem', false);
            this.getFrontendModel().setProperty('/expandAvailabilityNavListItem', true);
            this.getFrontendModel().setProperty('/selectedCalendarType', 'availability');
          }
        } else if (['APPOINTMENTS', 'AVAILABILITY'].includes(routeName)) {
          this.initCalendarSettings();
          this.getFrontendModel().setProperty('/lastChosenPerson', null);
          this.applyFilter();
        }
      });
    },
    deactivateImproveAppointment: function _deactivateImproveAppointment() {
      this.timeoutCount--;
      if (this.timeoutCount <= 0) {
        this.getFrontendModel().setProperty('/improveAppointmentPressed', false);
        this.timeoutCount = 0;
      }
    },
    filterAppointments: function _filterAppointments(includeAll) {
      let appointments = [...this.getUserDataModel().getProperty('/appointment_list')];
      if (includeAll) {
        this.getFrontendModel().setProperty('/filteredAppointments', appointments);
        return;
      } else {
        const lastChosenPersonId = this.getFrontendModel().getProperty('/lastChosenPerson');
        const chosenUserName = this.idsToPersonNames(lastChosenPersonId);
        if (chosenUserName) {
          appointments = appointments.filter(appointment => appointment.participants.includes(lastChosenPersonId));
          this.getFrontendModel().setProperty('/filteredAppointments', appointments);
        } else {
          this.getFrontendModel().setProperty('/filteredAppointments', appointments);
        }
      }
    },
    filterSlots: function _filterSlots() {
      let slots = [...this.getUserDataModel().getProperty('/slot_list')];
      const lastChosenPersonId = this.getFrontendModel().getProperty('/lastChosenPerson');
      const chosenUserName = this.idsToPersonNames(lastChosenPersonId);
      if (chosenUserName) {
        slots = slots.filter(slot => slot.person == lastChosenPersonId);
        this.getFrontendModel().setProperty('/filteredSlots', slots);
      }
    },
    findBetterStartDate: function _findBetterStartDate(appointment) {
      const appointments = this.getUserDataModel().getProperty('/appointment_list');
      const slots = this.getUserDataModel().getProperty('/slot_list');
      const earliestDate = this.calendar.getStartDate(); // todo this is not accurate
      const dayOffset = this.getCalendarViewOffset(this.getCalendarViewName());
      const latestDate = new Date(earliestDate.getTime() + dayOffset * 24 * 3600 * 1000);
      return findBetterStartDate(appointment, appointments, slots, earliestDate, latestDate);
    },
    formDataToAppointment: function _formDataToAppointment() {
      const formData = this.getFrontendModel().getProperty('/appointmentForm');
      const datePicker = this.byId('idDateInput');
      const date = adjustDate(datePicker.getDateValue());
      const dateString = date.toISOString().split('T')[0];
      const startDate = adjustDate(new Date(dateString + 'T' + formData.startTime + 'Z'), 'add');
      const endDate = adjustDate(new Date(dateString + 'T' + formData.endTime + 'Z'), 'add');
      if (startDate.getTime() >= endDate.getTime()) {
        endDate.setDate(endDate.getDate() + 1);
      }
      return {
        _type: 'appointment',
        id: formData.id,
        title: formData.title,
        participants: formData.participants,
        start_date: startDate,
        end_date: endDate
      };
    },
    formDataToSlot: function _formDataToSlot() {
      const formData = this.getFrontendModel().getProperty('/availabilityForm');
      const datePicker = this.byId('idDateInput');
      const date = adjustDate(datePicker.getDateValue());
      const dateString = date.toISOString().split('T')[0];
      const startDate = adjustDate(new Date(dateString + 'T' + formData.startTime + 'Z'), 'add');
      const endDate = adjustDate(new Date(dateString + 'T' + formData.endTime + 'Z'), 'add');
      if (startDate.getTime() >= endDate.getTime()) {
        endDate.setDate(endDate.getDate() + 1);
      }
      return {
        _type: 'slot',
        id: formData.id,
        person: formData.person,
        start_date: startDate,
        end_date: endDate,
        is_preferred: formData.is_preferred
      };
    },
    getCalendarViewName: function _getCalendarViewName() {
      return this.byId(this.calendar.getSelectedView()).getKey();
    },
    /**
     * Returns the number of days the calendar view is showing.
     */
    getCalendarViewOffset: function _getCalendarViewOffset(viewName) {
      switch (viewName) {
        case 'WeekView':
          return 7;
        case 'WorkWeekView':
          return 5;
        case 'DayView':
          return 1;
        default:
          new Error('Unknown calendar view: ' + viewName);
      }
    },
    handleCreateAppointment: function _handleCreateAppointment(event) {
      const startDate = adjustDate(event.getParameter('startDate'));
      const endDate = adjustDate(event.getParameter('endDate'));
      const formData = this.getFrontendModel().getProperty('/appointmentForm');
      const lastChosenPerson = this.getFrontendModel().getProperty('/lastChosenPerson');
      formData.participants = lastChosenPerson ? [lastChosenPerson] : [];
      formData.id = null;
      formData.title = '';
      formData.date = startDate.toISOString().substring(0, 10);
      formData.startTime = startDate.toISOString().substring(11, 16);
      formData.endTime = endDate.toISOString().substring(11, 16);
      this.getFrontendModel().setProperty('/appointmentForm', formData);
      this.openCalendarItemDialog();
    },
    handleCreateBtnAppointmentPress: function _handleCreateBtnAppointmentPress() {
      const formData = this.getFrontendModel().getProperty('/appointmentForm');
      const lastChosenPerson = this.getFrontendModel().getProperty('/lastChosenPerson');
      formData.id = null;
      formData.title = '';
      formData.date = this.lastTappedStartDate.toISOString().substring(0, 10);
      formData.startTime = this.lastTappedStartDate.toISOString().substring(11, 16);
      formData.endTime = this.lastTappedEndDate.toISOString().substring(11, 16);
      formData.participants = lastChosenPerson ? [lastChosenPerson] : [];
      this.getFrontendModel().setProperty('/appointmentForm', formData);
      this.openCalendarItemDialog();
    },
    handleCreateBtnSlotPress: function _handleCreateBtnSlotPress() {
      const formData = this.getFrontendModel().getProperty('/availabilityForm');
      const lastChosenPerson = this.getFrontendModel().getProperty('/lastChosenPerson');
      formData.id = null;
      formData.date = this.lastTappedStartDate.toISOString().substring(0, 10);
      formData.startTime = this.lastTappedStartDate.toISOString().substring(11, 16);
      formData.endTime = this.lastTappedEndDate.toISOString().substring(11, 16);
      formData.person = lastChosenPerson;
      this.getFrontendModel().setProperty('/availabilityForm', formData);
      this.openCalendarItemDialog();
    },
    handleCreateSlot: function _handleCreateSlot(event) {
      const startDate = event.getParameter('startDate');
      const endDate = event.getParameter('endDate');
      const person = this.getFrontendModel().getProperty('/lastChosenPerson');
      const slot = {
        _type: 'slot',
        id: null,
        person: person,
        start_date: startDate,
        end_date: endDate,
        is_preferred: true
      };
      this.getUserDataModel().create(slot);
    },
    handleSelectAppointment: function _handleSelectAppointment(event) {
      const calendarAppointment = event.getParameter('appointment');
      if (calendarAppointment) {
        if (this.getFrontendModel().getProperty('/improveAppointmentPressed')) {
          this.improveAppointment(calendarAppointment);
          this.setTimerForImproveAppointment();
          return;
        }
        const startDate = adjustDate(calendarAppointment.getStartDate());
        const endDate = adjustDate(calendarAppointment.getEndDate());
        const formData = this.getFrontendModel().getProperty('/appointmentForm');
        const appointmentId = calendarAppointment.getKey();
        const appointment = this.getUserDataModel().get('appointment', appointmentId);
        assert(Boolean(appointment), 'Appointment not found');
        formData.participants = appointment.participants;
        formData.id = appointmentId;
        formData.title = calendarAppointment.getTitle();
        formData.date = startDate.toISOString().substring(0, 10);
        formData.startTime = startDate.toISOString().substring(11, 16);
        formData.endTime = endDate.toISOString().substring(11, 16);
        this.getFrontendModel().setProperty('/appointmentForm', formData);
        this.openCalendarItemDialog();
      }
    },
    handleSelectSlot: function _handleSelectSlot(event) {
      const calendarAppointment = event.getParameter('appointment');
      if (calendarAppointment) {
        const startDate = adjustDate(calendarAppointment.getStartDate());
        const endDate = adjustDate(calendarAppointment.getEndDate());
        const formData = this.getFrontendModel().getProperty('/availabilityForm');
        const entryId = calendarAppointment.getKey();
        const slot = this.getUserDataModel().get('slot', entryId);
        assert(Boolean(slot), 'Slot not found');
        formData.person = slot.person;
        formData.id = entryId;
        formData.date = startDate.toISOString().substring(0, 10);
        formData.startTime = startDate.toISOString().substring(11, 16);
        formData.endTime = endDate.toISOString().substring(11, 16);
        formData.is_preferred = slot.is_preferred;
        this.getFrontendModel().setProperty('/availabilityForm', formData);
        this.openCalendarItemDialog();
      }
    },
    improveAppointment: function _improveAppointment(calendarAppointment) {
      const appointment = this.getUserDataModel().get('appointment', calendarAppointment.getKey());
      const startDate = this.findBetterStartDate(appointment);
      if (!startDate) {
        MessageToast.show('Es wurde kein besserer Termin gefunden.'); // todo i18n
        return;
      } else {
        this.moveAppointmentToBetterStartDate(appointment, startDate);
      }
    },
    initCalendarSettings: function _initCalendarSettings() {
      const calendarWeekView = this.byId('idWeekView');
      calendarWeekView.setFirstDayOfWeek(getLocaleData().getFirstDayOfWeek());
      this.calendar.setFirstDayOfWeek(getLocaleData().getFirstDayOfWeek());
      const calendarView = getCookie('CALENDAR_VIEW');
      if (calendarView) {
        this.calendar.getViews().forEach(view => {
          if (view.getKey() === calendarView) {
            this.calendar.setSelectedView(view);
          }
        });
      }
      const show24hCalendar = getCookie('CALENDAR_SHOW_24_HOURS');
      if (show24hCalendar) {
        this.getFrontendModel().setProperty('/show24hCalendar', show24hCalendar === 'true');
      }
      const calendarStartDate = getCookie('CALENDAR_START_DATE');
      if (calendarStartDate) {
        this.calendar.setStartDate(new Date(calendarStartDate));
      }
      this.getFrontendModel().setProperty('/selectedCalendarType', this.type);
    },
    initMouseObserver: function _initMouseObserver() {
      document.addEventListener('mousemove', event => {
        this.mousePosition.x = event.clientX / window.innerWidth;
        this.mousePosition.y = event.clientY / window.innerHeight;
      });
    },
    moveAppointmentToBetterStartDate: function _moveAppointmentToBetterStartDate(appointment, startDate) {
      const currentMousePosition = {
        ...this.mousePosition
      };
      const endDate = new Date(startDate.getTime() + (appointment.end_date.getTime() - appointment.start_date.getTime()));
      appointment.start_date = startDate;
      appointment.end_date = endDate;
      const locale = getLocale().getLanguage();
      const onFinish = () => {
        const formattedDate = appointment.start_date.toLocaleString(locale, {
          weekday: 'long',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        });
        void confetti({
          particleCount: 20,
          spread: 360,
          ticks: 15,
          origin: currentMousePosition
        });
        MessageToast.show(`Termin nach ${formattedDate} verschoben`); // todo i18n
      };
      this.getUserDataModel().update(appointment, () => onFinish());
    },
    setAppointmentDialogFocus: function _setAppointmentDialogFocus() {
      const subjectInput = this.byId('idSubjectInput');
      if (subjectInput) {
        subjectInput.focus();
      }
    },
    setCalenderViewChangeHandlers: function _setCalenderViewChangeHandlers() {
      this.calendar.attachViewChange(() => {
        this.adjustCalendarStartDay();
        if (this.calendar.getSelectedView()) {
          setCookie('CALENDAR_VIEW', this.getCalendarViewName());
        }
      });
      this.calendar.attachStartDateChange(() => {
        setCookie('CALENDAR_START_DATE', this.calendar.getStartDate().toISOString());
      });
    },
    setTimerForImproveAppointment: function _setTimerForImproveAppointment() {
      this.timeoutCount++;
      setTimeout(() => {
        this.deactivateImproveAppointment();
      }, this.magicButtonTimeout);
    },
    /**
     * Checks if a slot is overlapping with another slot.
     * @param slot The slot to check.
     * @returns True if the slot is not overlapping with another slot, false otherwise.
     */
    validateSlot: function _validateSlot(slot) {
      let slots = this.getUserDataModel().getProperty('/slot_list');
      slots = slots.filter(s => s.id !== slot.id && s.person === slot.person);
      for (const s of slots) {
        if (slot.start_date >= s.start_date && slot.start_date < s.end_date || slot.end_date > s.start_date && slot.end_date <= s.end_date || slot.start_date <= s.start_date && slot.end_date >= s.end_date) {
          return false;
        }
      }
      return true;
    }
  });
  return Calendar;
});
//# sourceMappingURL=Calendar-dbg.controller.js.map

"use strict";

sap.ui.define(["demo/spa/controller/utils/Time"], function (__demo_spa_controller_utils_Time) {
  "use strict";

  const dateFitsInAllSlots = __demo_spa_controller_utils_Time["dateFitsInAllSlots"];
  QUnit.module('Time Utils');
  QUnit.test('The date fitter works.', function (assert) {
    for (const date of dates) {
      assert.ok(dateFitsInAllSlots(date, slots) === date.fits, `${date.start_date.toLocaleTimeString()} to ${date.end_date.toLocaleTimeString()} was marked correctly.`);
    }
  });

  /** @type {{start_date: Date, end_date: Date}[]} */
  const slots = [{
    start_date: date('00:00'),
    end_date: date('00:55')
  }, {
    start_date: date('00:10'),
    end_date: date('00:40')
  }, {
    start_date: date('00:30'),
    end_date: date('00:50')
  }];

  /** @type {{start_date: Date, end_date: Date, fits: boolean}[]} */
  const dates = [{
    start_date: date('00:00'),
    end_date: date('00:15'),
    fits: false
  }, {
    start_date: date('00:10'),
    end_date: date('00:20'),
    fits: false
  }, {
    start_date: date('00:35'),
    end_date: date('00:40'),
    fits: true
  }, {
    start_date: date('00:40'),
    end_date: date('00:45'),
    fits: false
  }];

  /**
   * Little convenience function to create a date object
   */
  function date(timeStr) {
    return new Date(`1970-01-01T${timeStr}:00Z`);
  }
});
//# sourceMappingURL=Time.qunit-dbg.js.map

"use strict";

sap.ui.define([], function () {
  "use strict";

  /**
   * Random number generator.
   * Used instead of Math.random() to ensure that the same seed
   * always generates the same sequence of random numbers.
   */
  class Random {
    /**
     * Constructor for the Random class.
     * Every instance will generate the same sequence of random numbers
     * given the same seed.
     * @param seed The seed for the random number generator.
     */
    constructor(seed) {
      this.seed = seed >= 0 ? seed % 2147483647 : 0;
      if (this.seed === 0) {
        this.seed = 1;
      }
    }

    /**
     * Genrate a random number between 0 and 1.
     */
    random() {
      this.seed = this.seed * 16807 % 2147483647;
      return (this.seed - 1) / 2147483646;
    }

    /**
     * Generate a random number in the given range
     * including the min and max values.
     */
    randIntBetween(min, max) {
      return Math.floor(this.random() * (max - min + 1) + min);
    }

    /**
     * Generate a random choice from the given array.
     */
    randomChoice(choices) {
      return choices[this.randIntBetween(0, choices.length - 1)];
    }
  }
  return Random;
});
//# sourceMappingURL=Random-dbg.js.map

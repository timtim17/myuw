<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">U-Pass Membership</h2>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your Husky card balance right now. In the meantime, if
      you want to add funds, try the
      <a href="https://transportation.uw.edu">UW Transportation</a> page.
    </template>
    <template #card-body>
      <uw-card-status>
        <template #status-label>Status</template>
        <template #status-value>
          {{ isCurrent ? 'Current' : 'Not current' }}
        </template>
      </uw-card-status>

      <div v-if="isCurrent" id="upass-notices">
        <p v-if="displayActivation" class="myuw-text-md">
          Finalize activation by tapping your card on a reader.
        </p>
        <div v-if="!employee && inSummer && (pce || seattle)">
          <h3 class="h6 text-dark-beige myuw-font-encode-sans">
            Summer U-PASS Use
          </h3>
          <p class="myuw-text-md">
            Your U-PASS does not work during summer quarter unless you are
            registered for a class or are a
            <a
              v-out="'Temporary Employee U-PASS'"
              href="https://transportation.uw.edu/getting-here/transit/u-pass"
            >
              temporary employee
            </a>.
          </p>
        </div>
        <a v-out="'U-Pass'" :href="getUrl" class="myuw-text-md">
            U-PASS not working?
        </a>
      </div>
      <div v-else id="upass-not-current">
        <div v-if="!employee" id="upass-notices-for-students">
          <div v-if="seattle">
            <p>
              If you are registered for a quarter, your U-PASS will work one week
              before the quarter starts.
            </p>
            <div v-if="inSummer">
              <h3 class="h6 text-dark-beige myuw-font-encode-sans">
                Summer U-PASS Use
              </h3>
              <p>
                Your U-PASS does not work during summer quarter unless you are registered
                for a class or are a
                <a
                  v-out="'Temporary Employee U-PASS'"
                  href="https://transportation.uw.edu/getting-here/transit/u-pass"
                >
                  temporary employee
                </a>.
              </p>
            </div>
          </div>
          <div v-else id="upass-notices-for-non-sea-studs">
            <p v-if="bothell || tacoma">
              If you
              <a v-out="'Purchase U-PASS'" :href="getPurchaseUrl">
                purchase
              </a>
              a U-PASS for a quarter, your U-PASS will work one week before the quarter starts.
            </p>
          </div>
        </div>
        <ul class="list-unstyled myuw-text-md mb-1">
          <li class="mb-1">
            <a v-out="'What is U-PASS'" :href="getWhatIsUrl">
              What is the U-PASS?
            </a>
          </li>
          <li v-if="pce" class="mb-1">
            <a
              v-out="'Continuum College Student Purchase U-PASS'"
              href="https://transportation.uw.edu/getting-here/transit/u-pass"
            >
              Purchasing a U-PASS
            </a>
          </li>
        </ul>
      </div>
    </template>
  </uw-card>
</template>
<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import CardStatus from '../_templates/card-status.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
  },
  computed: {
    ...mapGetters('upass', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      employee: (state) => state.user.affiliations.all_employee,
      student: (state) => state.user.affiliations.student,
      tacoma: (state) => state.user.affiliations.tacoma,
      bothell: (state) => state.user.affiliations.bothell,
      seattle: (state) => state.user.affiliations.seattle,
      pce: (state) => state.user.affiliations.pce,
      displayActivation: (state) => state.upass.value.display_activation,
      inSummer: (state) => state.upass.value.in_summer,
      isCurrent: (state) => state.upass.value.is_current,
    }),
    showCard() {
      return this.employee || this.student;
    },
    showError() {
      return this.statusCode !== 404;
    },
    getUrl() {
      return this.employee
        ? 'https://transportation.uw.edu/getting-here/transit/u-pass'
        : this.bothell
        ? 'https://www.uwb.edu/facility/commuter-services/upass'
        : this.tacoma
        ? 'https://www.tacoma.uw.edu/getting-campus/u-pass-orca'
        : 'https://transportation.uw.edu/getting-here/transit/u-pass';
    },
    getPurchaseUrl() {
      return this.bothell
        ? 'https://www.uwb.edu/facility/commuter-services/upass'
        : 'https://www.tacoma.uw.edu/getting-campus/students-purchasing-u-pass';
    },
    getWhatIsUrl() {
      return this.employee
        ? 'https://transportation.uw.edu/getting-here/transit/u-pass'
        : this.tacoma
        ? 'https://www.tacoma.uw.edu/getting-campus/what-u-pass'
        : this.bothell
        ? 'https://www.uwb.edu/facility/commuter-services/upass'
        : 'https://transportation.uw.edu/getting-here/transit/u-pass';
    },
  },
  created() {
    if (this.employee || this.student) this.fetch();
  },
  methods: {
    ...mapActions('upass', ['fetch']),
  },
};
</script>

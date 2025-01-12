<template>
  <div v-if="showCard">
    <div class="w-100 myuw-border-top border-c7" />
    <uw-card :loaded="isReady"
             :errored="isErrored"
             :errored-show="showError"
    >
      <template #card-heading>
        <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          UW Medicine Account
        </h2>
        <img :src="staticUrl+'images/UWMedicine_Logo_RGB@2x.png'"
             width="100px"
             alt=""
             class="position-absolute"
        >
      </template>
      <template #card-error>
        An error occurred and MyUW cannot load your information right now.
        In the meantime, try the
        <a href="https://services.uwmedicine.org/passwordportal/login.htm"
        >UW Medicine Account</a> page.
      </template>
      <template #card-body>
        <p>
          This password is for UW Medicine applications
          like Epic, ORCA, MINDscape, AMC network, etc.
        </p>
        <div v-if="medPwExpired">
          <div class="alert alert-danger" role="alert">
            <p>
              Password expired on {{ toFriendlyDate(expiresMed) }}.
              <a v-out="'Change UW Medicine password'"
                 :href="passwordChange"
              >
                <br>Change your password to regain access.
              </a>
            </p>
          </div>
        </div>
        <div v-else>
          <uw-card-status>
            <template #status-label>
              Password expiration
            </template>
            <template #status-value>
              <div :class="expires30Days ? 'text-danger' : ''">
                {{ toFriendlyDate(expiresMed) }}
              </div>
            </template>
            <template #status-content>
              <div class="text-end">
                in {{ daysBeforeExpires }} days*
              </div>
            </template>
          </uw-card-status>
          <p class="text-muted myuw-text-md">
            *Expiration date gets updated nightly.
          </p>
          <a :href="passwordChange">
            Change UW Medicine password
          </a>
        </div>
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import CardStatus from '../_templates/card-status.vue';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
  },
  data: function() {
    return {
      passwordChange: 'https://services.uwmedicine.org/passwordportal/login.htm',
    };
  },
  computed: {
    ...mapState({
      password: (state) => state.profile.value.password,
      staticUrl: (state) => state.staticUrl,
    }),
    ...mapGetters('profile', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    showError() {
      return this.statusCode !== 404;
    },
    hasActiveMedPw() {
      return this.password.has_active_med_pw;
    },
    medPwExpired() {
      return this.password.med_pw_expired;
    },
    expiresMed() {
      return this.password.expires_med;
    },
    daysBeforeExpires() {
      return this.password.days_before_med_pw_expires;
    },
    showCard() {
      return !this.isReady || Boolean(this.password) && this.hasActiveMedPw;
    },
    expires30Days() {
      return this.daysBeforeExpires <= 30;
    },
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('profile', {
      fetch: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped>
img {
  top: 1rem;
  right: 1rem;
}
</style>

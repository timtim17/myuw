<template>
  <uw-card
    v-if="student && (!isReady || hasRegisterNotices)"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
    </template>

    <template #card-body>
      <div v-for="notice in notices" :key="notice.id_hash" class="mb-3">
        <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          Review Critical Summer Registration Info
        </h2>
        <div class="myuw-text-md" v-html="notice.notice_body" />
      </div>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Consider Early Fall Start
      </h2>
      <div class="myuw-text-md mb-2">
        Early Fall Start is a single 5-credit intensive course held
        over four weeks before autumn quarter begins. Benefit from a small
        class size, an early introduction to college life, and a lighter
        course load during autumn quarter. The language courses may be
        particularly helpful to international students!
        <a href="http://www.outreach.washington.edu/efs/">Learn more about Early Fall Start and register</a>.
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      notices: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_summerreg'),
        );
      },
      student: (state) => state.user.affiliations.student,
    }),
    ...mapGetters('notices', [
      'hasRegisterNotices',
      'isReady',
      'isErrored',
      'statusCode',
    ]),
    showError() {
      return this.statusCode !== 404;
    },
  },
  created() {
    if (this.student) this.fetch();
  },
  methods: {
    ...mapActions('notices', ['fetch']),
  },
};
</script>

<template>
  <div v-if="isReady">
    <uw-tabs
      pills
      justified
      small
      nav-class="bg-white rounded"
      nav-wrapper-class="mb-2 border rounded p-0 w-75 mx-auto"
    >
      <uw-tab title="All" title-item-class="myuw-text-md">
        <uw-calendar-cards :events="allEvents" />
      </uw-tab>
      <uw-tab title-item-class="myuw-text-md">
        <template #title>
          <font-awesome-icon
            :icon="faCircle"
            class="align-baseline text-mid-beige myuw-text-tiny"
          />
          Breaks
        </template>
        <uw-calendar-cards :events="breakEvents" />
      </uw-tab>
    </uw-tabs>
  </div>
</template>

<script>
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import CalendarCards from './calendar-cards.vue';
import Tabs from '../_templates/tabs/tabs.vue';
import Tab from '../_templates/tabs/tab.vue';

export default {
  components: {
    'uw-calendar-cards': CalendarCards,
    'uw-tabs': Tabs,
    'uw-tab': Tab,
  },
  data() {
    return {
      faCircle,
      urlExtra: '',
    };
  },
  computed: {
    ...mapState('academic_events', {
      eventsByTerms: (state) => state.value,
    }),
    ...mapGetters('academic_events', {
      isReadyTagged: 'isReadyTagged',
    }),
    isReady() {
      return this.isReadyTagged(this.urlExtra);
    },
    allEvents() {
      return this.eventsByTerms[this.urlExtra].filter((e) => e.myuw_categories.all);
    },
    breakEvents() {
      return this.eventsByTerms[this.urlExtra].filter((e) => e.myuw_categories.breaks);
    },
  },
  created() {
    this.fetch(this.urlExtra);
  },
  methods: {
    ...mapActions('academic_events', ['fetch']),
  },
};
</script>

<style lang="scss" scoped>
::v-deep .nav-link.active {
  background-color:#4d307f !important;
}
</style>
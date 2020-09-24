import {shallowMount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import Outage from '../components/cards/outage.vue';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

describe('Outage card', () => {

  it('non404Error checking', () => {
    let store = new Vuex.Store({
        state: {
          user: {
            affiliations: {
            student: true,
            instructor: false,
            employee: false,
            }
          }
        },
        getters: {
          'courses/statusCode': () => 200,
          'notices/statusCode': () => 200,
          // 'profile/statusCode': () => 200,
        },
    });
    const wrapper = shallowMount(Outage, {store, localVue});
    expect(wrapper.vm.non404Error(200)).toBeFalsy();
    expect(wrapper.vm.non404Error(404)).toBeFalsy();
    expect(wrapper.vm.non404Error(543)).toBeTruthy();
    expect(wrapper.vm.non404Error(400)).toBeTruthy();
  });

  describe('showOutageCard for Student', () => {
    const state = {
      user: {
        affiliations: {
          student: true,
          instructor: false,
          employee: false,
        }
      }
    };

    it('showOutageCard for Student - Successful calls', () => {
      let getters = {
        'courses/statusCode': () => 200,
        'notices/statusCode': () => 200,
        // 'profile/statusCode': () => 200,
      };
      let store = new Vuex.Store({
        getters,
        state,
      });

      const wrapper = shallowMount(Outage, {store, localVue});
      expect(wrapper.vm.showOutageCard).toBeFalsy();
    });

    it('showOutageCard for Student - 404 Error', () => {
      let getters = {
        'courses/statusCode': () => 404,
        'notices/statusCode': () => 200,
        // 'profile/statusCode': () => 200,
      };
      let store = new Vuex.Store({
        getters,
        state,
      });
  
      const wrapper = shallowMount(Outage, {store, localVue});
      expect(wrapper.vm.showOutageCard).toBeFalsy();
    });

    it('showOutageCard for Student - 543 Error', () => {
      let getters = {
        'courses/statusCode': () => 543,
        'notices/statusCode': () => 200,
        // 'profile/statusCode': () => 200,
      };
      let store = new Vuex.Store({
        getters,
        state,
      });
    
      const wrapper = shallowMount(Outage, {store, localVue});
      expect(wrapper.vm.showOutageCard).toBeTruthy();
    });
  });
  // TODO: Add tests for the instructor and employee status'
  // This currently only tests for the case of a student.

});
import axios from 'axios';
import moment from 'moment';
import {shallowMount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import hfs from '../store/hfs';
import library from '../store/library';
import Summaries from '../components/index/summaries.vue';

import mockNotices from './mock_data/notices.json';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

jest.mock('axios');
jest.mock('moment');

describe('Summaries', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        hfs,
        library,
      },
      state: {},
    });
  });

  it('ucfirst', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
    const wrapper = shallowMount(Summaries, {store, localVue});
    expect(wrapper.vm.ucfirst('test')).toEqual('Test');
    expect(wrapper.vm.ucfirst('test string')).toEqual('Test string');
  });

  it('toFromNowDate', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
    moment.mockImplementation((s) => {
      return {
        fromNow: jest.fn().mockReturnValueOnce(s),
      };
    });
    const wrapper = shallowMount(Summaries, {store, localVue});
    expect(wrapper.vm.toFromNowDate('test')).toEqual('test');
    expect(moment).toHaveBeenCalledTimes(1);
  });

  it('getWeeksApart', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
    const wrapper = shallowMount(Summaries, {store, localVue});
    moment.mockImplementation(jest.requireActual('moment'));

    // The week starts on Sundays
    // Winter quarter starts on Tuesday
    let d1 = new Date(2017, 0, 3);
    let d2 = null;
    for (let i = 25; i <= 31; i++) {
      d2 = new Date(2016, 11, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(0);
    }

    for (let i = 1; i <= 7; i++) {
      d2 = new Date(2017, 0, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(1);
    }

    for (let i = 8; i <= 14; i++) {
      d2 = new Date(2017, 0, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(2);
    }

    for (let i = 12; i <= 18; i++) {
      d2 = new Date(2017, 2, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(11);
    }

    d2 = new Date(2017, 2, 21);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(12);

    // Spring quarter starts on Monday
    d1 = new Date(2017, 2, 27);
    d2 = new Date(2017, 2, 22);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(0);

    d2 = new Date(2017, 2, 26);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(1);

    d1 = new Date(2017, 2, 27);
    d2 = new Date(2017, 3, 1);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(1);

    // Aut quarter starts on Wedesnday
    d1 = new Date(2017, 8, 27);
    d2 = new Date(2017, 8, 23);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(0);

    for (let i = 24; i <= 30; i++) {
      d2 = new Date(2017, 8, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(1);
    }
    for (let i = 10; i <= 23; i++) {
      d2 = new Date(2017, 8, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(0);
    }
  });
});

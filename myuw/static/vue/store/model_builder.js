import axios from 'axios';

const statusOptions = ['READY', 'FETCHING', 'ERROR'];

// Some helper functions
const doNothing = (response) => response;
const extractData = (response) => response.data;
const setTermAndExtractData = (response, urlExtra) => {
  let proccessValue = {};
  proccessValue[urlExtra] = response.data;
  return proccessValue;
}

const fetchBuilder = (url, postProcess, type) => {
  return ({commit, getters}, urlExtra = '') => {
    if (!getters.isReady && !getters.isFetching) {
      commit('setStatus', {[urlExtra]: {type: statusOptions[1]}});
      axios.get(url + urlExtra, {
        responseType: type,
      }).then((response) => {
        return {
          data: postProcess(response, urlExtra),
          statusCode: response.status
        };
      }).then(({data, statusCode}) => {
        commit('setValue', data);
        commit(
          'setStatus',
          {[urlExtra]: {type: statusOptions[0], code: statusCode}}
        );
      }).catch((error)=>{
        if (process.env.NODE_ENV === "development") {
          console.log(error);
        };
        commit(
          'setStatus', 
          {
            [urlExtra]: {
              type: statusOptions[2], code: error.response.status,
            }
          }
        );
      });
    }
  };
};

const buildWith = (
    {
      customState={
        value: [],
        status: {},
      },
      customGetters={},
      customMutations={},
      customActions={},
    } = {}) => {
  const state = () => ({
    ...customState
  });

  const getters = {
    // Default getters when no urlExtra is used
    isReady(state) {
      return (
        state.status[''] !== undefined &&
        state.status[''].type == statusOptions[0]
      );
    },
    isFetching(state) {
      return (
        state.status[''] !== undefined &&
        state.status[''].type == statusOptions[1]
      );
    },
    isErrored(state) {
      return (
        state.status[''] !== undefined &&
        state.status[''].type == statusOptions[2]
      );
    },
    statusCode(state) {
      return state.status[''] !== undefined ? -1 : state.status.code;
    },
    // Function type getters when urlExtra is used
    isReadyTagged: (state) => (urlExtra) => (
      state.status[urlExtra] !== undefined &&
      state.status[urlExtra].type == statusOptions[0]
    ),
    isFetchingTagged: (state) => (urlExtra) => (
      state.status[urlExtra] !== undefined &&
      state.status[urlExtra].type == statusOptions[1]
    ),
    isErroredTagged: (state) => (urlExtra) => (
      state.status[urlExtra] !== undefined &&
      state.status[urlExtra].type == statusOptions[2]
    ),
    statusCodeTagged: (state) => (urlExtra) => (
      state.status[urlExtra] !== undefined ? -1 : state.status.code
    ),
    ...customGetters,
  };

  const mutations = {
    setValue(state, data) {
      state.value = data;
    },
    setStatus(state, status) {
      state.status = status;
    },
    ...customMutations,
  };

  return {
    namespaced: true,
    state,
    getters,
    actions: customActions,
    mutations,
  };
};


export {
  statusOptions,
  // Helper Functions
  doNothing,
  extractData,
  setTermAndExtractData,
  // Builders
  buildWith,
  fetchBuilder,
};

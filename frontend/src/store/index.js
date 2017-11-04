import Vue from 'vue'
import Vuex from 'vuex'
import actions from './actions'
import mutations from './mutations'
import getters from './getters'
// import modules
// import rut from './rut'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    user: null,
    nexturl: ''
  },
  actions,
  mutations,
  getters,

  modules: {}
})

export default store

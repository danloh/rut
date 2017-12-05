import Vue from 'vue'
import Vuex from 'vuex'
import actions from './actions'
import mutations from './mutations'
import getters from './getters'
import rut from './modules/rut'
import item from './modules/item'
import clip from './modules/clip'
import demand from './modules/demand'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {  // only for auth user
    currentUser: null,
    currentUserID: '',
    authed: false,
    token: '',
    nexturl: ''
  },
  actions,
  mutations,
  getters,
  modules: {
    rut,
    item,
    clip,
    demand
  }
})

export default store

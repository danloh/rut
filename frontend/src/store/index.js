import Vue from 'vue'
import Vuex from 'vuex'
import actions from './actions'
import mutations from './mutations'
import getters from './getters'
import rut from './modules/rut'
import item from './modules/item'
import clip from './modules/clip'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    user: null,
    token: '',
    nexturl: ''
  },
  actions,
  mutations,
  getters,
  modules: {
    rut,
    item,
    clip
  }
})

export default store

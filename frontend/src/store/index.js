import Vue from 'vue'
import Vuex from 'vuex'
import { getToken, setToken, removeToken, getID, setID, removeID } from '@/util/auth'
import getters from './getters'
import rut from './modules/rut'
import item from './modules/item'
import clip from './modules/clip'
import demand from './modules/demand'

Vue.use(Vuex)

// for auth user
const state = {
  currentUserID: Number(getID()),
  authed: Boolean(getID()) && Boolean(getToken()),
  token: getToken(),
  currentUser: null,
  nexturl: ''
}
const mutations = {
  SET_USER (state, userid) {
    state.currentUserID = userid
    state.authed = Boolean(userid)
    setID(userid)
  },
  SET_TOKEN (state, token) {
    state.token = token
    setToken(token)
  },
  SET_INFO (state, userobj) {
    state.currentUser = userobj
  },
  DEL_TOKEN (state) {
    state.token = ''
    state.currentUserID = ''
    state.currentUser = null
    state.authed = false
    removeToken()
    removeID()
  },
  MOD_NEXT (state, nexturl) {
    state.nexturl = nexturl
  }
}
import { fetchCurrentUser, confirm, reset } from '@/api/api'
const actions = {
  getCurrentUser: ({ commit, state }) => {
    return new Promise((resolve, reject) => {
      fetchCurrentUser()
      .then(resp => {
        commit('SET_INFO', resp.data)
        resolve(resp)
      }).catch(error => {
        reject(error)
      })
    })
  },
  confirmEmail: (context, token) => {
    return new Promise((resolve, reject) => {
      confirm(token).then(resp => {
        resolve(resp)
      }).catch(error => {
        reject(error)
      })
    })
  },
  resetPsw: (context, params) => {
    return new Promise((resolve, reject) => {
      reset(params['token'], params['data']).then(resp => {
        resolve(resp)
      }).catch(error => {
        reject(error)
      })
    })
  }
}
// store instance
const store = new Vuex.Store({
  state,
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

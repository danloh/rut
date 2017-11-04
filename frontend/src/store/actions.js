// root action

import {
  authUser
} from '../api/api'

export default {
  VERIFY ({ commit, state }) {
    authUser({ ref: 'verify' }).then((resp) => {
      if (state.user == null || state.user.userid !== resp.data.userid) {
        authUser().then((resp) => {
          commit('MOD_USER', resp.data)
          return true
        }, (resp) => {
          return false
        })
      }
    }, (resp) => {
      commit('MOD_USER', null)
      return false
    })
  }
}

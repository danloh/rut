// root action

import {
  authUser
} from '../api/api'

export default {
  VERIFY: ({ commit, state }) => {
    return authUser({ ref: 'verify' }).then((resp) => {
      if (state.user == null || state.user.id !== resp.data.id) {
        return authUser().then((resp) => {
          commit('MOD_USER', resp.data)
          return true
        }, (resp) => {
          return false
        })
      }
      return true
    }, (resp) => {
      commit('MOD_USER', null)
      return false
    })
  }
}

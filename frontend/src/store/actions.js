// // root action
// import axios from '../main'
import { fetchCurrentUser } from '@/api/api'

export default {
  getCurrentUser: ({ commit, state }) => {
    return new Promise((resolve, reject) => {
      fetchCurrentUser()
      .then(resp => {
        commit('MOD_USER', resp.data)
        resolve(resp)
      }).catch(error => {
        reject(error)
      })
    })
  }
}

// axios('api/user', { ref: 'verify' })
// .then((resp) => {
//   if (state.user == null || state.user.id !== resp.data.id) {
//     return axios('api/user').then((resp) => {
//       commit('MOD_USER', resp.data)
//       return true
//     }, (resp) => {
//       return false
//     })
//   }
//   return true
// }, (resp) => {
//   commit('MOD_USER', null)
//   return false
// })

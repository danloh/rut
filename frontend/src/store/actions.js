// // root action
// import axios from '../main'

// export default {
//   VERIFY: ({ commit, state }) => {
//     return axios('api/user', { ref: 'verify' })
//     .then((resp) => {
//       if (state.user == null || state.user.id !== resp.data.id) {
//         return axios('api/user').then((resp) => {
//           commit('MOD_USER', resp.data)
//           return true
//         }, (resp) => {
//           return false
//         })
//       }
//       return true
//     }, (resp) => {
//       commit('MOD_USER', null)
//       return false
//     })
//   }
// }

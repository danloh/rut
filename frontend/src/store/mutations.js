// import Vue from 'vue'

export default {
  MOD_USER (state, userobj) {
    state.currentUser = userobj
    state.authed = Object.keys(userobj).length !== 0
    state.currentUserID = userobj.id
    localStorage.userid = userobj.id
  },
  SET_TOKEN (state, token) {
    state.token = token
    localStorage.token = token
  },
  SET_USER (state, id) {
    state.currentUserID = id
  },

  DEL_TOKEN (state) {
    state.token = ''
    state.currentUserID = ''
    state.currentUser = null
    state.authed = false
    localStorage.token = ''
    localStorage.userid = ''
  },
  MOD_NEXT (state, nexturl) {
    state.nexturl = nexturl
  }
}

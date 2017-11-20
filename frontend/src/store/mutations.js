// import Vue from 'vue'

export default {
  MOD_USER (state, userobj) {
    state.user = userobj
    localStorage.user = userobj.id
  },

  SET_TOKEN (state, token) {
    state.token = token
    localStorage.token = token
  },

  DEL_TOKEN (state) {
    state.token = ''
    localStorage.token = ''
  },

  MOD_NEXT (state, nexturl) {
    state.nexturl = nexturl
  }
}

// import Vue from 'vue'

export default {
  MOD_USER (state, userobj) {
    state.user = userobj
  },

  SET_TOKEN (state, token) {
    state.token = token
    localStorage.token = token
  },

  MOD_NEXT (state, nexturl) {
    state.nexturl = nexturl
  }
}

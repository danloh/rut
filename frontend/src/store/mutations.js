// import Vue from 'vue'

export default {
  MOD_USER: (state, userobj) => {
    state.user = userobj
  },

  MOD_NEXT: (state, nexturl) => {
    state.nexturl = nexturl
  }
}

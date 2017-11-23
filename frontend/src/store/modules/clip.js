// initial state
const state = {
  clipz: {
    list: {
      clips: [],
      prev: null,
      more: null,
      total: 0
    },  // get from api
    page: 0
  }
}

// getters
const getters = {
  cliplist: state => state.clipz.list
}

// actions
const actions = {
}

// mutations
const mutations = {
  SET_CLIPS (state, data) {
    state.clipz.list = data
    state.clipz.page = 1
  },
  ADD_CLIPS (state, data) {
    let clips = state.clipz.list.clips
    clips.push.apply(clips, data.clips)
    state.page += 1
    state.clipz.list.more = data.more
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}

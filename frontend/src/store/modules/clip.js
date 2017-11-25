import axios from '@/main'

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
  getClip: ({commit, state}, param = {}) => {
    return axios.get('api/clips', param)
    .then(resp => {
      const notFirstPage = param.page && param.page > 1
      const muta = `${notFirstPage ? 'ADD' : 'SET'}_CLIPS`
      commit(muta, resp.data)
      return Promise.resolve(resp.data)
    })
  }
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

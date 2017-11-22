// initial state
const state = {
  rutz: {
    list: {
      ruts: [],
      prev: null,
      more: null,
      total: 0
    },  // get from api
    page: 0
  },
  rutdetail: {}
}

// getters
const getters = {
  rutlist: state => state.rutz.list,
  rutdetail: state => state.rutdetail
}

// actions
const actions = {
}

// mutations
const mutations = {
  SET_RUTS (state, data) {
    state.rutz.list = data
    state.rutz.page = 1
  },
  ADD_RUTS (state, data) {
    let ruts = state.rutz.list.ruts
    ruts.push.apply(ruts, data.ruts)
    state.page += 1
    state.rutz.list.more = data.more
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}

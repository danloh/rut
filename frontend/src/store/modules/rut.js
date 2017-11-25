import axios from '@/main'

// initial state
const perPage = 2
const state = {
  allRuts: [],
  total: 0,
  currentPage: 0,
  currentRuts: [],
  maxPage: 0,
  perPage: perPage,
  rutdetail: {}
}

// actions
const actions = {
  getRuts: ({commit, state}, param = {}) => {
    return axios.get('api/ruts', param)
    .then((resp) => {
      commit('SET_RUTS', resp.data)
    })
  }
}

// mutations
const mutations = {
  SET_RUTS (state, data) {
    state.allRuts = data.ruts
    state.currentPage = 1
    state.maxPage = Math.ceil(data.total / perPage)
    let sliced = data.ruts.slice(0, perPage)
    state.currentRuts.push(...sliced)
  },
  ADD_RUTS (state, page) {
    let start = page * perPage
    let end = start + perPage
    let nextRuts = state.allRuts.slice(start, end)
    state.currentPage += 1
    state.currentRuts.push(...nextRuts)
  }
}

export default {
  state,
  actions,
  mutations
}

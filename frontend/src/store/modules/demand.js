// import axios from '@/main'
import {
  fetchDemands,
  newDemand
} from '@/api/api'

// initial state
const perPage = 15
const state = {
  allDemands: [],
  totalDemands: 0,
  currentD: 0,
  currentDemands: [],
  maxD: 0,
  perD: perPage
}

// actions
const actions = {
  getDemands: ({commit, state}, params = {}) => {
    return fetchDemands(params)
    .then(resp => {
      commit('SET_DEMANDS', resp.data)
    })
  },
  postDemand: ({commit, state}, params = {}) => {
    return newDemand(params)
    .then(resp => {
      commit('ADD_DEMAND', resp.data)
    })
  }
}

// mutations
const mutations = {
  SET_DEMANDS (state, data) {
    state.allDemands = data.demands
    state.totalDemands = data.total
    state.currentD = 1
    state.maxD = Math.ceil(data.total / perPage)
    let sliced = data.demands.slice(0, perPage)
    state.currentDemands = sliced
  },
  ADD_DEMANDS (state, page) {
    let start = page * perPage
    let end = start + perPage
    let nextDemands = state.allDemands.slice(start, end)
    state.currentD += 1
    state.currentDemands.push(...nextDemands)
  },
  ADD_DEMAND (state, data) {
    state.currentDemands.unshift(data)
  }
}

export default {
  state,
  actions,
  mutations
}

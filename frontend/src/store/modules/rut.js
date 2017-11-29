// import axios from '@/main'
import {
  fetchRuts,
  fetchRut,
  fetchTag
} from '@/api/api'

// initial state
const perPage = 15
const state = {
  allRuts: [],
  currentPage: 0,
  currentRuts: [],
  maxPage: 0,
  perPage: perPage,
  allTags: [],
  showTags: [],
  tagDetail: {},
  rutDetail: {}
}

// actions
const actions = {
  getRuts: ({commit, state}, param = {}) => {
    return fetchRuts(param)
    .then(resp => {
      commit('SET_RUTS', resp.data)
    })
  },
  getRut: ({commit, state}, rutid, param = {}) => {
    return fetchRut(rutid, param)
    .then(resp => {
      commit('SET_RUT', resp.data)
    })
  },
  getTag: ({commit, state}, tagid, param = {}) => {
    return fetchTag(tagid, param)
    .then(resp => {
      commit('SET_RUTS', resp.data)
      commit('SET_TAG', resp.data)
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
    state.currentRuts = sliced
    let dtags = data.tags
    state.allTags = dtags
    let sometags = dtags.slice(0, perPage)
    state.showTags = sometags
  },
  ADD_RUTS (state, page) {
    let start = page * perPage
    let end = start + perPage
    let nextRuts = state.allRuts.slice(start, end)
    state.currentPage += 1
    state.currentRuts.push(...nextRuts)
  },
  SET_RUT (state, data) {
    state.rutDetail = data
  },
  SET_TAG (state, data) {
    state.tagDetail = data
  }
}

export default {
  state,
  actions,
  mutations
}

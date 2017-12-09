// import axios from '@/main'
import {
  fetchClips,
  fetchIUClips,
  newClip
} from '@/api/api'

// initial state
const perPage = 15
const state = {
  allClips: [],
  totalClips: 0,
  currentP: 0,
  currentClips: [],
  maxP: 0,
  perP: perPage
}

// actions
const actions = {
  getClips: ({commit, state}, params = {}) => {
    if (params.itemid || params.userid) {
      return fetchIUClips(params)
      .then(resp => {
        commit('SET_CLIPS', resp.data)
      })
    }
    return fetchClips(params)
    .then(resp => {
      commit('SET_CLIPS', resp.data)
    })
  },
  postClip: ({commit, state}, params = {}) => {
    return newClip(params)
    .then(resp => {
      commit('ADD_CLIP', resp.data)
    })
  }
}

// mutations
const mutations = {
  SET_CLIPS (state, data) {
    state.allClips = data.clips
    state.totalClips = data.total
    state.currentP = 1
    state.maxP = Math.ceil(data.total / perPage)
    let sliced = data.clips.slice(0, perPage)
    state.currentClips = sliced
  },
  ADD_CLIPS (state, page) {
    let start = page * perPage
    let end = start + perPage
    let nextClips = state.allClips.slice(start, end)
    state.currentP += 1
    state.currentClips.push(...nextClips)
  },
  ADD_CLIP (state, data) {
    state.currentClips.unshift(data)
  }
}

export default {
  state,
  actions,
  mutations
}

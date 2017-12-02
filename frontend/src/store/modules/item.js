import {
  fetchItem
} from '@/api/api'

// initial state
const perPage = 15
const state = {
  currentItem: {},
  allReviews: [],
  newReviews: [],
  currentReviews: [],
  currentR: 0,
  maxR: 0,
  perR: perPage,
  inRuts: []
}
// actions
const actions = {
  getItem: ({state, commit}, itemid, params) => {
    return fetchItem(itemid, params)
    .then(resp => {
      commit('SET_ITEM', resp.data)
    })
  }
}
// mutations
const mutations = {
  SET_ITEM: (state, data) => {
    state.currentItem = data
    state.allReviews = data.hotreviews
    state.newReviews = data.newreviews
    state.inRuts = data.inruts
    state.currentR = 1
    state.maxR = Math.ceil(data.reviewcount / perPage)
    let sliced = data.hotreviews.slice(0, perPage)
    state.currentReviews = sliced
  },
  NEW_REVIEWS: (state, order) => { // order ref: hot or new
    if (order === 'new') {
      state.currentReviews = state.newReviews
    } else {
      let sliced = state.allReviews.slice(0, perPage)
      state.currentReviews = sliced
    }
  },
  ADD_REVIEWS: (state, page) => {
    let start = page * perPage
    let end = start + perPage
    let nextReviews = state.allReviews.slice(start, end)
    state.currentR += 1
    state.currentReviews.push(...nextReviews)
  }
}

export default {
  state,
  actions,
  mutations
}

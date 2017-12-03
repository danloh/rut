import {
  fetchItem,
  fetchItems
} from '@/api/api'

// initial state
const perPage = 15
const state = {
  allItems: [],
  currentItems: [],
  totalItems: 0,
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
  getItem: ({state, commit}, itemid) => {
    return fetchItem(itemid)
    .then(resp => {
      commit('SET_ITEM', resp.data)
    })
  },
  getItems: ({state, commit}, params) => {
    return fetchItems(params['flag'], params['param'])
    .then(resp => {
      commit('SET_ITEMS', resp.data)
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
  SET_ITEMS: (state, data) => {
    state.allItems = data.items
    state.currentR = 1
    state.totalItems = data.total
    state.maxR = Math.ceil(data.total / perPage)
    let sliced = data.items.slice(0, perPage)
    state.currentItems = sliced
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
  },
  ADD_ITEMS: (state, page) => {
    let start = page * perPage
    let end = start + perPage
    let nextItems = state.allItems.slice(start, end)
    state.currentR += 1
    state.currentItems.push(...nextItems)
  }
}

export default {
  state,
  actions,
  mutations
}

import {
  fetchItem,
  fetchProfileItems
} from '@/api/api'

// initial state
const perPage = 20
const state = {
  currentItems: [],
  totalItems: 0,
  currentItem: {},
  newReviews: [],
  hotReviews: [],
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
    return fetchProfileItems(params['flag'], params['userid'])
    .then(resp => {
      commit('SET_ITEMS', resp.data)
    })
  }
}
// mutations
const mutations = {
  SET_ITEM: (state, data) => {
    state.currentItem = data
    state.newReviews = data.newreviews
    state.hotReviews = data.hotreviews
    state.inRuts = data.inruts
    state.currentR = 1
    state.maxR = Math.ceil(data.reviewcount / perPage)
    state.currentReviews = data.hotreviews
  },
  SET_ITEMS: (state, data) => {
    state.currentR = 1
    state.totalItems = data.total
    state.maxR = Math.ceil(data.total / perPage)
    state.currentItems = data.items
  },
  ALT_REVIEWS: (state, order) => { // order ref: hot or new
    if (order === 'new') {
      state.currentR = 1
      state.currentReviews = state.newReviews
    } else {
      state.currentR = 1
      state.currentReviews = state.hotReviews
    }
  },
  MORE_REVIEWS: (state, data) => {
    state.currentR += 1
    state.currentReviews.push(...data)
  },
  MORE_ITEMS (state, data) {
    state.currentR += 1
    state.currentItems.push(...data)
  }
}

export default {
  state,
  actions,
  mutations
}

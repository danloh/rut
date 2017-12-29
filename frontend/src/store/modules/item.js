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
    state.inRuts = data.inruts
  },
  SET_ITEMS: (state, data) => {
    state.currentR = 1
    state.totalItems = data.total
    state.maxR = Math.ceil(data.total / perPage)
    state.currentItems = data.items
  },
  MORE_INRUTS: (state, data) => {
    state.inRuts.push(...data)
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

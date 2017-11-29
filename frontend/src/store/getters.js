const getters = {
  currentUser: state => state.user,
  allRuts: state => state.rut.allRuts,
  totalRuts: state => state.rut.total,
  currentPage: state => state.rut.currentPage,
  currentRuts: state => state.rut.currentRuts,
  maxPage: state => state.rut.maxPage,
  perPage: state => state.rut.perPage,
  allTags: state => state.rut.allTags,
  showTags: state => state.rut.showTags,
  rutDetail: state => state.rut.rutDetail,
  tagDetail: state => state.rut.tagDetail
}

export default getters

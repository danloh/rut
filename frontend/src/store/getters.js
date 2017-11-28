const getters = {
  currentUser: state => state.user,
  allRuts: state => state.rut.allRuts,
  totalRuts: state => state.rut.total,
  currentPage: state => state.rut.currentPage,
  currentRuts: state => state.rut.currentRuts,
  maxPage: state => state.rut.maxPage,
  perPage: state => state.rut.perPage,
  rutDetail: state => state.rut.rutDetail
}

export default getters

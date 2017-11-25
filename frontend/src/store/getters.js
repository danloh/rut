const getters = {
  allRuts: state => state.rut.allRuts,
  totalRuts: state => state.rut.total,
  currentPage: state => state.rut.currentPage,
  currentRuts: state => state.rut.currentRuts,
  maxPage: state => state.rut.maxPage,
  perPage: state => state.rut.perPage,
  rutdetail: state => state.rut.rutdetail
}

export default getters

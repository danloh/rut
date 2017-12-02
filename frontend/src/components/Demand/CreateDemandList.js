import DemandList from './DemandList.vue'

// higher order components wrapping
export default function createDemandList (type = 'popular') {
  return {
    name: `${type}-demand`,
    render (h) {
      return h(DemandList, {props: { type }})
    }
  }
}

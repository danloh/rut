import DemandList from './DemandList.vue'

// for dynamically creating clip list for different param.
// higher order components wrapping ClipList.vue.
export default function createDemandList (type = 'popular') {
  return {
    name: `${type}-demand`,
    render (h) {
      return h(DemandList, {props: { type }})
    }
  }
}

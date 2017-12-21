// deprecated
import Create from './Create.vue'

// higher order components wrapping
export default function createNewRut (act = 'Create') {
  return {
    name: `${act}-rut`,
    render (h) {
      return h(Create, {props: { act }})
    }
  }
}

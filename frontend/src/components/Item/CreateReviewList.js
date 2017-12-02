import ReviewList from './ReviewList.vue'

// for dynamically creating review list for different order.
// higher order components wrapping ReviewList.vue.
export default function createReviewList (order = 'hot') {
  return {
    name: `${order}-review`,
    render (h) {
      return h(ReviewList, {props: { order }})
    }
  }
}

<template>
  <div class="item-view" v-if="item">
    <template v-if="item">
      <item-sum :item="item"></item-sum>
      <div>
        {{item.details}}
      </div>
      <review v-for="review in reviews" :key="review.id" :review="review"></review>
      <div>
        <router-link :to="'/item/comment' + item.id">Comment</router-link>
      </div>
    </template>
  </div>
</template>

<script>
import { getItem } from '../api/api'
import ItemSum from '../components/ItemSum.vue'
import Review from '../components/Review.vue'
import Comment from '../components/Comment.vue'

export default {
  name: 'item-view',
  title () {
    return this.item.title
  },
  components: { ItemSum, Review, Comment },
  data: () => ({
    item: null
  }),
  computed: {
    reviews () {
      return this.item.reviews
    }
  },

  // Fetch item when mounted on the client
  mounted () {
    this.fetchItem()
  },

  methods: {
    fetchItem () {
      let param = {}
      getItem(this.$route.params.id, param).then((resp) => {
        this.item = resp.data
      })
    }
  }
}
</script>


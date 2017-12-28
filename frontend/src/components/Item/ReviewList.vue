<template>
  <div class="review-list">
    <review-sum v-for="review in currentReviews" :key="review.id" :review="review" :less="true"></review-sum>
    <div v-if="hasMore">
      <el-button class="blockbtn" @click="loadmoreReviews" :disabled="!hasMore">More</el-button>
    </div>
  </div>
</template>

<script>
import ReviewSum from './ReviewSum.vue'
import { fetchItemReviews } from '@/api/api'
import { mapGetters } from 'vuex'

export default {
  name: 'review-list',
  components: { ReviewSum },
  props: {
    order: String
  },
  computed: {
    ...mapGetters([
      'currentItem',
      'currentReviews',
      'currentR',
      'maxR',
      'perR'
    ]),
    hasMore () {
      return Math.ceil(this.currentReviews.length / this.perR) < this.maxR
    }
  },
  created () {
    this.$store.commit('ALT_REVIEWS', this.order)
  },
  methods: {
    loadmoreReviews () {
      let params = {'page': this.currentR, 'ref': this.order}
      fetchItemReviews(this.currentItem.id, params)
      .then(resp => {
        this.$store.commit('MORE_REVIEWS', resp.data)
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.review-list
  padding auto
</style>

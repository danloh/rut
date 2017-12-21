<template>
  <div class="review-list">
    <review-sum v-for="review in currentReviews" :key="review.id" :review="review" :less="true"></review-sum>
    <div v-if="hasMore">
      <el-button class="blockbtn" @click="loadmoreReview" :disabled="!hasMore">More</el-button>
    </div>
  </div>
</template>

<script>
import ReviewSum from './ReviewSum.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'item-list',
  components: { ReviewSum },
  props: {
    order: String
  },
  computed: {
    ...mapGetters([
      'currentItem',
      'currentReviews',
      'currentR',
      'maxR'
    ]),
    hasMore () {
      return this.currentR < this.maxR
    }
  },
  created () {
    this.$store.commit('NEW_REVIEWS', this.order)
  },
  methods: {
    loadmoreReviews () {
      this.$store.commit('ADD_REVIEWS', this.currentR)
    }
  }
}
</script>

<style lang="stylus" scoped>
.item-page
  padding 10px 230px 10px 0px
  position relative
  .item-side
    position absolute
    top 10px
    right 0
    width 220px
    background-color white
    .lefttitle
      background-color #e5ebe4
      padding 10px 15px
    .leftbody
      padding 5px 20px
  .review-list
    padding auto
</style>

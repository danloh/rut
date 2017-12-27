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

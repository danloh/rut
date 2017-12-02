<template>
  <div class="item-page">
    <item-sum :item="currentItem"></item-sum>
    <div v-html="currentItem.details"></div>
    <div class="review-list">
      <h4>Review</h4>
      <review-sum v-for="review in currentReviews" :key="review.id" :review="review"></review-sum>
    </div>
    <div>
      <el-button class="blockbtn" @click="loadmoreReview" :disabled="!hasMore" v-if="hasMore">More</el-button>
    </div>
    <div class="item-side">
      <p>About Author</p>
      <div>The Item included in</div>
    </div>
  </div>
</template>

<script>
import ItemSum from '../components/Item/ItemSum.vue'
import ReviewSum from '../components/Item/ReviewSum.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'item-view',
  title () {
    return this.currentItem.title
  },
  components: { ItemSum, ReviewSum },
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
  mounted () {
    let itemid = this.$route.params.id
    this.$store.dispatch('getItem', itemid)
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


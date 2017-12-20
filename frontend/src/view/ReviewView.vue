<template>
  <div class="review-page">
    <div class="review-main">
      <review-sum :review="review" :key="review.id"></review-sum> <!--Note :key to render-->
    </div>
    <div class="comment">
    </div>
  </div>
</template>

<script>
import { fetchReview } from '@/api/api'
// import { checkAuth } from '@/util/auth'
import ReviewSum from '@/components/Item/ReviewSum.vue'
import Comment from '@/components/Comment/Comment.vue'
import Reply from '@/components/Comment/Reply.vue'

export default {
  name: 'review-view',
  title () {
    return this.review.heading
  },
  components: { ReviewSum, Comment, Reply },
  data () {
    return {
      review: {}
    }
  },
  computed: {
    creator () {
      return this.review.creator
    }
  },
  methods: {
    loadReviewData () {
      let reviewid = this.$route.params.id
      fetchReview(reviewid)
      .then(resp => {
        let data = resp.data
        this.review = data
      })
    }
  },
  created () {
    this.loadReviewData()
  }
}
</script>

<style lang="stylus" scoped>
.review-page
  padding 10px 235px 10px 0px
  position relative
  .review-main
    padding auto
  .review-side
    position absolute
    top 10px
    right 0
    width 225px
</style>

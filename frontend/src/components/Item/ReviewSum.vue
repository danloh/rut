<template>
  <div class="review-main">
    <h3 class="title">
      <router-link :to="'/review/' + review.id">{{ review.heading }}</router-link>
    </h3>
    <p class="meta">
      By <router-link :to="'/profile/' + creator.id">{{ creator.name }}</router-link>
      | {{ review.timestamp | toMDY }}
      | on <router-link :to="'/item/' + review.item.id">{{ review.item.title.slice(0, 60) }}..</router-link>
    </p>
    <div class="review-body" v-html="review.body"></div>
    <div class="bar">
      <router-link :to="'/editreview/' + review.id" v-if="canEdit">...Edit</router-link>
      | <el-button type="text"><span @click="upReview">Helpful</span></el-button> {{ vote }} 
    </div>
  </div>
</template>

<script>
import { upvoteReview } from '@/api/api'
import { checkAuth } from '@/util/auth'

export default {
  name: 'review-sum',
  props: ['review'],
  data () {
    return {
      vote: this.review.vote
    }
  },
  computed: {
    creator () {
      return this.review.creator
    },
    canEdit () {
      return Number(this.review.creator.id) === Number(this.$store.getters.currentUserID)
    }
  },
  methods: {
    upReview () {
      if (checkAuth()) {
        let reviewid = this.review.id
        return upvoteReview(reviewid)
        .then(resp => {
          this.vote = resp.data
        })
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.review-main
  background-color lighten(#f6f6f1, 50%)
  padding 5px
  border-bottom 1px dotted #e09015
  position relative
  .title
    font-weight 700
    a
      &:hover
        color #ff6600
  .meta
    font-size .75em
  .bar
    text-align right
  .review-body
    background-color #f6f6f1
    padding 0 5px
    font-size 1.05em
</style>

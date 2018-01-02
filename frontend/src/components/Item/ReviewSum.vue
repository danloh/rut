<template>
  <div class="review-main" v-if="creator">
    <h3 class="title">
      <router-link :to="'/review/' + review.id">{{ review.heading }}</router-link>
    </h3>
    <p class="meta">
      By <router-link :to="'/profile/' + creator.id">{{ creator.name }}</router-link>
      | {{ review.timestamp | toMDY }}
      | on <router-link :to="'/item/' + review.item.id">{{ review.item.title.slice(0, 60) }}..</router-link>
    </p>
    <div class="review-body">
      <div class="ql-snow">
        <div class="ql-editor" style="font-size:16px;padding:2px" v-html="reviewContent"></div>
      </div>
      <el-button type="text" size="mini" @click="showFull" v-if="spoiler || short">{{ readMore }}</el-button>
    </div>
    <div class="bar">
      <router-link :to="'/editreview/' + review.id" v-if="canEdit">...Edit |</router-link>
      <el-button type="text" @click="upReview">Helpful</el-button>&nbsp;{{ vote }}
    </div>
  </div>
</template>

<script>
import { upvoteReview } from '@/api/api'
import { checkAuth } from '@/util/auth'
import { showLess } from '@/util/filters'

export default {
  name: 'review-sum',
  props: {
    review: Object,
    less: Boolean
  },
  data () {
    return {
      vote: this.review.vote,
      spoiler: this.review.spoiler,
      short: this.less // not directly mutate prop less
    }
  },
  computed: {
    creator () {
      return this.review.creator
    },
    reviewContent () {
      let content = this.review.body
      let least = this.spoiler ? 0 : 255
      return this.short || this.spoiler ? showLess(content, least) : content
    },
    readMore () {
      return this.spoiler ? 'Spoilers Ahead! Continue?' : 'Read More ...'
    },
    canEdit () {
      return Number(this.review.creator.id) === Number(this.$store.getters.currentUserID)
    }
  },
  methods: {
    showFull () {
      this.spoiler = false
      this.short = false
    },
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
    font-size 0.75em
  .bar
    font-size 0.7em
    text-align right
  .review-body
    background-color #f6f6f1
    padding 0 5px
    font-size 1.05em
</style>

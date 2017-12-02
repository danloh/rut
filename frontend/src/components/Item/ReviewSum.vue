<template>
  <div class="review-main">
    <h4 class="title">{{ review.heading }}</h4>
    <p class="meta">
      By <router-link :to="'/profile/' + creator.id">{{ creator.name }}</router-link>
      | {{ review.timestamp }}
    </p>
    <div class="review-body" v-html="review.body"></div>
  </div>
</template>

<script>
export default {
  name: 'review-sum',
  props: ['review'],
  computed: {
    creator () {
      return this.review.creator
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
  .meta
    font-size .75em
  .review-body
    background-color #f6f6f1
    padding 0 5px
    font-size 1.05em
</style>
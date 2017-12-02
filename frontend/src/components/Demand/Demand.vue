<template>
  <div class="demand-main">
    <div class="demand-body">{{demand.body}}</div>
    <p class="demand-bar">
      Requseted by <router-link :to="'/profile/' + requestor.id">{{requestor.name}}</router-link>
      | {{demand.vote}} <el-button type="text">Upvote</el-button>
      | {{demand.answercount}} Answer
      | {{demand.commentcount}} Discuss
    </p>
  </div>
</template>

<script>
export default {
  name: 'demand',
  props: ['demand'],
  components: {},
  computed: {
    requestor () {
      return this.demand.requestor
    }
  }
}
</script>

<style lang="stylus" scoped>
.demand-main
  padding 5px
  background-color lighten(#f6f5f2, 50%)
  border-bottom 1px dotted #689f38
  .demand-body
    background-color #f6f5f2
    padding 10px
    color #3ac
    font-size 1.15em
  .demand-bar
    text-align right
    font-size 0.8em
</style>
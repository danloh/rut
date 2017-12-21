<template>
  <div class="demand-page">
    <div class="demand-main">
      <demand :demand="demandDetail" :key="demandDetail.id"></demand>
      <div class="answer">
        <b>The Answers to This Demand:</b>
        <p class="title" v-for="(rut, index) in answers" :key="index" :rut="rut">
          - <router-link :to="'/readuplist/' + rut.id" :title="rut.title"> {{ rut.title.slice(0, 160) }}...</router-link>
        </p>
      </div>
      <div class="comment">
        <reply class="reply" :refer="refer" :show="true" @newreply="updateNew"></reply>
      </div>
      <div v-for="comment in comments" :key="comment.id">
        <comment :comment="comment"></comment>
      </div>
    </div>
    <div class="demand-side">
    </div>
  </div>
</template>

<script>
import Demand from '@/components/Demand/Demand.vue'
import Comment from '@/components/Comment/Comment.vue'
import Reply from '@/components/Comment/Reply.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'demand-view',
  title () {
    return this.demandDetail.body
  },
  components: { Demand, Comment, Reply },
  data () {
    return {
      refer: { re: 'demand', id: this.$route.params.id },
      comments: []
    }
  },
  computed: {
    ...mapGetters([
      'demandDetail'
    ]),
    answers () {
      return this.demandDetail.answers
    // },
    // comments () {
    //   return this.demandDetail.comments
    }
  },
  methods: {
    loadDemandData () {
      let demandid = this.$route.params.id
      this.$store.dispatch('getDemand', demandid)
      .then(resp => {
        this.comments = resp.data.comments
      })
    },
    updateNew (data) {
      this.comments.unshift(data)
    }
  },
  created () {
    this.loadDemandData()
  }
}
</script>

<style lang="stylus" scoped>
.demand-page
  padding 10px 255px 10px 0px
  position relative
  .demand-main
    padding auto
    .answer
      background-color white
      padding 5px
      margin-bottom 5px
      .title
        a
          &:hover
            color #ff6600
  .demand-side
    position absolute
    top 10px
    right 0
    width 245px
    .include
      margin-top 0px
      padding 5px
      background-color #f0f3f0
      .in-title
        padding 2px 5px
        color green
      .in-item
        padding 2px 5px
        font-size 0.85em
        background-color white
</style>

<template>
  <div class="demand-main">
    <div class="demand-body">{{demand.body}}</div>
    <div class="demand-bar">
      Requseted by <router-link :to="'/profile/' + requestor.id">{{ requestor.name }}</router-link>
      | {{ vote }} <el-button type="text"><span @click="upDemand">Upvote</span></el-button>
      | {{ answercount }} <el-button type="text"><router-link :to="'/create/' + demand.id"><b>Answer</b></router-link></el-button>
      | {{demand.commentcount}} <router-link :to="'/demand/' + demand.id">Discuss</router-link>
    </div>
  </div>
</template>

<script>
import { upvoteDemand } from '@/api/api'

export default {
  name: 'demand',
  props: ['demand'],
  data () {
    return {
      vote: this.demand.vote,
      answercount: this.demand.answercount
    }
  },
  computed: {
    requestor () {
      return this.demand.requestor
    }
  },
  methods: {
    checkAuth () {
      let localToken = localStorage.token
      // let localID = localStorage.userid
      if (localToken) {
        this.$axios.defaults.auth = {
          username: localToken,
          password: localToken
        }
        return true
      } else {
        return false
      }
    },
    upDemand () {
      if (this.checkAuth()) {
        let demandid = this.demand.id
        return upvoteDemand(demandid)
        .then(resp => {
          this.vote = resp.data
        })
      }
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
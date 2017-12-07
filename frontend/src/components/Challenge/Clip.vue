<template>
  <div class="clipmain">
    <div class="clipbody" v-html="clip.body"></div>
    <p class="meta">
      From <router-link :to="'/item/' + fromitem.id" :title="fromitem.title">{{ fromitem.title.slice(0, 60) }}...</router-link>
      via <router-link :to="'/profile/' + creator.id">{{ creator.name.slice(0, 20) }}</router-link>
      | {{ clip.timestamp | toMDY }}
      | {{ vote }} <el-button type="text"><span @click="upClip">Upvote</span></el-button>
    </p>
  </div>
</template>

<script>
import { upvoteClip } from '@/api/api'

export default {
  name: 'clip',
  props: ['clip'],
  data () {
    return {
      vote: this.clip.vote
    }
  },
  computed: {
    creator () {
      return this.clip.creator
    },
    fromitem () {
      return this.clip.fromitem
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
    upClip () {
      if (this.checkAuth()) {
        let clipid = this.clip.id
        return upvoteClip(clipid)
        .then(resp => {
          this.vote = resp.data
        })
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.clipmain
  background-color lighten(#f6f6f1, 50%)
  padding 10px
  border-bottom 1px dotted #e09015
  position relative
  .meta
    font-size .75em
    text-align right
  .clipbody
    background-color #f6f6f1
    padding 10px
    font-size 1.05em
    color #0192b5
li
  list-style-type none
</style>
<template>
  <div class="rutpage">
    <div class="rutview">
      <div>
        <span class="tag" v-for="tag in tags" :key="tag.id">
          <router-link :to="'/tag/' + tag.id">{{tag.tagname}}</router-link>
        </span>
      </div>
      <div>
        <h2>{{ arut.title }}</h2>
        <p class="meta">
          Created by {{ arut.creator.name }}
          | {{ arut.createat }}
          | including {{ arut.itemcount }} items
        </p>
      </div>
      <div class="intro" v-html="arut.intro"></div>
      <div class="toolbar">
        <el-button type="success" size="mini" plain>{{starAction}} {{arut.starcount}}</el-button>
        <el-button type="success" size="mini" plain>{{challengeAction}} {{arut.challengecount}}</el-button>
      </div>
      <div class="itemtip" v-for="tip in tips" :key="tip.order">
        <item-sum class="itemsum" :item="tip.item"></item-sum>
        <div class="tip" v-html="tip.tip"></div>
      </div>
      <div class="epilog">
        {{arut.epilog}}
      </div>
      <div class="comment">
        <router-link :to="'/rut/comment' + arut.id">Comment</router-link>
      </div>
    </div>
    <div class="rutside">
      <h4 class="sidetitle">Creator's Credential</h4>
      <p class="sidebody" v-html="credential"></p>
    </div>
  </div>
</template>

<script>
import Spinner from '../components/Spinner.vue'
import ItemSum from '../components/ItemSum.vue'
import Comment from '../components/Comment.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'rut-view',
  components: { ItemSum, Spinner, Comment },
  data () {
    return {
      starAction: 'Star',
      challengeAction: 'Challenge'
    }
  },
  computed: {
    ...mapGetters({
      arut: 'rutDetail'
    }),
    tips () {
      return this.arut.tips
    },
    tags () {
      return this.arut.tags
    },
    credential () {
      return this.arut.credential
    }
  },
  mounted () {
    let rutid = this.$route.params.id
    this.$store.dispatch('getRut', rutid)
  }
}
</script>

<style lang="stylus" scoped>
$bgcolor = #f6f6f1
.rutpage
  padding-left 700px
  position relative
  .rutview
    position absolute
    left 0
    width 680px
    .meta 
      color green
    .intro
      background-color $bgcolor
      padding 10px
    .itemtip
      background-color $bgcolor
      .itemsum
        top 5px
        margin 5px
      .tip
        padding 10px
    .tag
      display inline-blcok
      padding-right 10px
      border-radius 100px
      a
        color green
        background-color #eef4fa
        font-size 1.2em
        font-weight 700
    .toolbar
      display flex
      align-items center
      justify-content flex-end
  .rutside
    background-color #e5ebe4
    .sidetitle
      background-color #c6efc0
      padding 5px
    .sidebody
      padding 0 5px
      min-height 60px
</style>


<template>
  <div class="rutpage">
    <div class="rutview">
      <div>
        <span class="tag" v-for="tag in tags" :key="tag.id">
          <router-link :to="'/tag/' + tag.id">{{tag.tagname}}</router-link>
        </span>
      </div>
      <div>
        <h3>{{ arut.title }}</h3>
        <p class="meta">
          By <router-link :to="'/profile/' + creator.id">{{ creator.name }}</router-link>
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
      <h5 class="sidetitle">Creator's Credential</h5>
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
    creator () {
      return this.arut.creator
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
      font-size 0.8em
    .intro
      background-color $bgcolor
      padding 10px
      border-bottom 1px dotted orange
    .itemtip
      background-color $bgcolor
      .itemsum
        top 5px
        margin 5px
      .tip
        padding 10px
    .epilog
      background-color $bgcolor
      padding 10px
      margin-top 5px
      border-top 1px dotted orange
    .tag
      display inline-blcok
      padding-right 10px
      border-radius 100px
      a
        color green
        background-color #eef4fa
        font-size 0.85em
        font-weight 700
    .toolbar
      display flex
      align-items center
      justify-content flex-end
  .rutside
    background-color #f5f9f5
    .sidetitle
      background-color #dff0d8
      padding 15px 10px
      color #3c763d
    .sidebody
      padding 0 10px
      min-height 45px
      font-size 0.85em
</style>


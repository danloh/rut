<template>
  <div class="rutpage" :key="arut.id">
    <div class="rutview">
      <div class="tagbar">
        <span class="tag" v-for="tag in tags" :key="tag.id">
          <router-link :to="'/tag/' + tag.id">{{tag.tagname}}</router-link>
        </span>
      </div>
      <div class="title">
        <h3>{{ arut.title }}</h3>
        <p class="meta">
          By <router-link :to="'/profile/' + creator.id">{{ creator.name }}</router-link>
          | {{ arut.createat }}
          | including {{ arut.itemcount }} items
        </p>
      </div>
      <div class="intro" v-html="arut.intro"></div>
      <div class="toolbar">
        <el-button type="info" size="mini" plain v-if="canEdit">...Edit...</el-button>
        <el-button type="info" size="mini" plain v-if="canEdit">...Add Item...</el-button>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <el-button type="success" size="mini" plain><b>{{starAction}} {{arut.starcount}}</b></el-button>
        <el-button type="warning" size="mini" plain><b>{{challengeAction}} {{arut.challengecount}}</b></el-button>
      </div>
      <div class="itemtip" v-for="tip in tips" :key="tip.order">
        <item-sum class="itemsum" :item="tip.item"></item-sum>
        <div class="tip" v-html="tip.tip"></div>
      </div>
      <div class="epilog">
        {{arut.epilog}} <el-button type="text" v-if="canEdit">...Edit Epilog</el-button>
      </div>
      <div class="comment">
        <router-link :to="'/rut/comment' + arut.id">Comment</router-link>
      </div>
    </div>
    <div class="rutside">
      <p class="sidetitle">Creator's Credential</p>
      <p class="sidebody" v-html="credential"></p>
    </div>
  </div>
</template>

<script>
import Spinner from '@/components/Misc/Spinner.vue'
import ItemSum from '@/components/Item/ItemSum.vue'
import Comment from '@/components/Comment.vue'
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
    },
    canEdit () {
      return true // this.creator.id === this.$store.state.userid ||
      // this.arut.editable === 'Everyone'
    }
  },
  title () {
    return this.arut.title
  },
  beforeMount () {
    let rutid = this.$route.params.id
    this.$store.dispatch('getRut', rutid)
  }
}
</script>

<style lang="stylus" scoped>
$bgcolor = lighten(#f6f6f1, 50%)
.rutpage
  padding 10px 250px 10px 0px
  position relative
  .rutview
    background-color lighten(#eceef1, 50%)
    padding auto
    .title
      padding 0 10px
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
    .tagbar
      display inline-blcok
      .tag
        padding-left 10px
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
    position absolute
    right 0
    top 10px
    width 240px
    .sidetitle
      background-color #dff0d8
      padding 10px
      color #3c763d
    .sidebody
      padding 0 10px
      min-height 45px
      font-size 0.85em
</style>


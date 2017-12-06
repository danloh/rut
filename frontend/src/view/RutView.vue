<template>
  <div class="rutpage">
    <div class="rutview">
      <div class="tagbar">
        <span class="tag" v-for="(tag, index) in tags" :key="index">
          <router-link :to="'/tag/' + tag.id">{{tag.tagname}}</router-link>
        </span>
      </div>
      <div class="title">
        <h2>{{ rutDetail.title }}</h2>
        <p class="meta">
          By <router-link :to="'/profile/' + creatorid">{{ creatorname }}</router-link>
          | {{ rutDetail.createat | toLocal }}
          | including {{ rutDetail.itemcount }} items
        </p>
      </div>
      <div class="intro">
        <b>Preface:&nbsp;</b>
        <div v-html="rutDetail.intro"></div>
      </div>
      <div class="toolbar">
        <el-button size="mini" plain v-if="canEdit">
          <router-link :to="'/edit/readuplist/' + rutid">...Edit</router-link>
        </el-button>
        <el-button size="mini" plain v-if="canEdit">
          <router-link :to="'/additemto/readuplist/' + rutid">Add Item...</router-link>
        </el-button>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <el-button type="success" size="mini" plain @click="starRut"><b>{{ starAction }} {{ starCount }}</b></el-button>
        <el-button type="success" size="mini" plain @click="challengeRut"><b>{{ challengeAction }} {{ challengeCount }}</b></el-button>
      </div>
      <div class="itemtip" v-for="tip in tips" :key="tip.order">
        <item-sum class="itemsum" :item="tip.item"></item-sum>
        <b>&nbsp;&nbsp;Read-up-Tips:&nbsp;</b> 
        <el-button type="text" v-if="canEdit">
          <router-link :to="'/edit/readuptips/' + tip.cid">...Edit</router-link>
        </el-button>
        <div class="tip" v-html="tip.tip"></div>
      </div>
      <div class="epilog">
        <b>Epilog:&nbsp;</b>
        <div v-html="rutDetail.epilog"></div>
        <el-button type="text" v-if="canEdit">
          <router-link :to="'/edit/readuplist/' + rutid">...Edit</router-link>
        </el-button>
      </div>
      <div class="comment">
        <router-link :to="'/rut/comment' + rutid">Comment</router-link>
      </div>
    </div>
    <div class="rutside">
      <p class="sidetitle">Creator's Credential</p>
      <div class="sidebody" v-html="credential"></div>
    </div>
  </div>
</template>

<script>
import Spinner from '@/components/Misc/Spinner.vue'
import ItemSum from '@/components/Item/ItemSum.vue'
import Comment from '@/components/Comment.vue'
import { scRut, checkSC } from '@/api/api'  // sc: star and challenge
import { mapGetters } from 'vuex'

export default {
  name: 'rut-view',
  components: { ItemSum, Spinner, Comment },
  data () {
    return {
      starAction: this.checkStar(),
      challengeAction: this.checkChallenge(),
      starCount: 0,
      challengeCount: 0,
      creatorid: null,
      creatorname: '',
      currentUserID: -1
    }
  },
  computed: {
    ...mapGetters([
      'rutDetail'
    ]),
    rutid () {
      return this.rutDetail.id
    },
    tips () {
      return this.rutDetail.tips
    },
    tags () {
      return this.rutDetail.tags
    },
    creator () {
      return this.rutDetail.creator
    },
    contributors () {
      return this.rutDetail.contributors
    },
    contributorIDList () {
      return this.rutDetail.contributoridlist
    },
    credential () {
      return this.rutDetail.credential
    },
    canEdit () {  // ???
      return this.creatorid === this.currentUserID
      // || this.rutDetail.editable === 'Everyone' || this.currentUserID in this.contributorIDList
    },
    canDelete () {
      return this.creatorid === this.currentUserID // ?
    }
  },
  title () {
    return this.rutDetail.title
  },
  created () {
    let crutid = this.$route.params.id
    this.$store.dispatch('getRut', crutid)
    .then(resp => {
      this.starCount = resp.data.starcount
      this.challengeCount = resp.data.challengecount
      this.creatorid = resp.data.creator.id
      this.creatorname = resp.data.creator.name
      this.currentUserID = this.$store.getters.currentUserID
    })
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
    checkStar () {
      if (this.checkAuth()) {
        let rutid = this.$route.params.id // ?? liftcycle timing
        return checkSC(rutid, 'star')
        .then(resp => {
          this.starAction = resp.data
        })
      } else {
        this.starAction = 'Star'
      }
    },
    checkChallenge () {
      if (this.checkAuth()) {
        let rutid = this.$route.params.id // ?? liftcycle timing
        return checkSC(rutid, 'challenge')
        .then(resp => {
          this.challengeAction = resp.data
        })
      } else {
        this.challengeAction = 'Challenge'
      }
    },
    starRut () {
      if (this.checkAuth()) {
        if (this.starAction === 'Star') {
          return scRut('star', this.rutid)
          .then(() => {
            this.starAction = 'Unstar'
            this.starCount += 1
          })
        } else {
          return scRut('unstar', this.rutid)
          .then(() => {
            this.starAction = 'Star'
            this.starCount -= 1
          })
        }
      } else {
        this.$message({
          showClose: true,
          message: 'Should Log in to Continue'
        })
        this.$router.push('/login')
      }
    },
    challengeRut () {
      if (this.checkAuth()) {
        if (this.challengeAction === 'Challenge') {
          return scRut('challenge', this.rutid)
          .then(() => {
            this.challengeAction = 'Endchallenge'
            this.challengeCount += 1
          })
        } else {
          return scRut('unchallenge', this.rutid)
          .then(() => {
            this.challengeAction = 'Challenge'
            this.challengeCount -= 1
          })
        }
      } else {
        this.$message({
          showClose: true,
          message: 'Should Log in to Continue'
        })
        this.$router.push('/login')
      }
    }
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
        color #828282
        font-size 0.8em
    .intro
      background-color $bgcolor
      padding 10px
      border-bottom 1px dotted #f3bc59
    .itemtip
      background-color $bgcolor
      .itemsum
        top 5px
        margin 5px
      .tip
        padding 5px 10px
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


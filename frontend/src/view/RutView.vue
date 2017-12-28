<template>
  <div class="rut-page">
    <div class="rut-view">
      <div class="tagbar">
        <span class="tag" v-for="(tag, index) in tags" :key="index">
          <router-link :to="'/tag/' + tag.id">{{tag.tagname}}</router-link>
        </span>
        <el-button type="text" @click="showDialog=true" v-show="canTag">..Edit</el-button>
      </div>
      <!-- edit tag dialog -->
      <el-dialog title="Edit Tag" :visible.sync="showDialog" width="30%">
        <el-input size="mini" v-model="newTag" @keyup.enter.native="addNewTag" placeholder="Input a Tag, Press Enter to Add"></el-input>
        <div v-for="(tag, index) in newTags" :key="index">
          <p><el-button type="text" size="mini" @click="newTags.splice(index, 1)">X</el-button>&nbsp;&nbsp; {{ tag }} </p>
        </div>
        <div slot="footer" class="dialog-footer">
          <el-button size="mini" @click="showDialog = false">Cancel</el-button>
          <el-button type="success" size="mini" @click="editTag">Done</el-button>
        </div>
      </el-dialog>
      <!-- dialog end -->
      <div class="title">
        <h2>{{ rutDetail.title }}</h2>
        <p class="meta">
          By <router-link :to="'/profile/' + creatorid">{{ creatorname }}</router-link>
          | {{ rutDetail.createat | toMDY }}
          | include {{ rutDetail.itemcount }} items
          | {{ rutDetail.commentcount }} <router-link :to="'/commenton/rut/' + rutid">Comments</router-link>
        </p>
      </div>
      <div class="intro">
        <b class="indicator">Preface:&nbsp;</b>
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
      <div class="itemtip" v-for="tip in tips" :key="tip.cid">
        <item-sum class="itemsum" :item="tip.item" :key="tip.itemid"></item-sum>
        <b class="indicator">&nbsp;&nbsp;Tips:&nbsp;</b> 
        <el-button type="text" size="mini" v-if="canEdit">
          <router-link :to="'/edit/readuptips/' + tip.cid">...Edit</router-link>
        </el-button>
        <div class="tip">
          <div v-html="tip.tip" v-show="!tip.spoiler || !short"></div>
          <el-button type="text" size="mini" @click="short = !short" v-if="tip.spoiler && short">... Spoilers Ahead! Continue?</el-button>
        </div>
      </div>
      <div class="epilog">
        <b class="indicator">Epilog:&nbsp;</b>
        <el-button type="text" size="mini" v-if="canEdit">
          <router-link :to="'/edit/readuplist/' + rutid">...Edit</router-link>
        </el-button>
        <div v-html="rutDetail.epilog"></div>
      </div>
      <div class="bottombar">
        <share-bar></share-bar>
      </div>
    </div> 
    <div class="rut-side">
      <div class="credential">
        <p class="credential-title"><b>Creator's Credential</b></p>
        <div class="credential-body">{{ credential || 'Not Introduce' }}</div>
      </div>
      <div class="demands" v-if="demandCount">
        <b>As Answer to Request:</b>
        <p class="demand-title" v-for="(demand, index) in demands" :key="index" :demand="demand">
          - <router-link :to="'/demand/' + demand.id"> {{ demand.demand.slice(0, 60) }}...</router-link>
        </p>
        <div v-if="hasMoreDemand">
          <el-button size="mini" @click="loadmoreDemand" :disabled="!hasMoreDemand">Show More</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Spinner from '@/components/Misc/Spinner.vue'
import ItemSum from '@/components/Item/ItemSum.vue'
import Comment from '@/components/Comment/Comment.vue'
import ShareBar from '@/components/Misc/ShareBar.vue'
import { scRut, checkSC, editTags, fetchRutDemands } from '@/api/api'  // sc: star and challenge
import { checkAuth } from '@/util/auth'
import { mapGetters } from 'vuex'

export default {
  name: 'rut-view',
  components: { ItemSum, Spinner, Comment, ShareBar },
  data () {
    return {
      starAction: this.checkStar(), // || 'Star',
      challengeAction: this.checkChallenge(), // || 'Challenge',
      starCount: 0,
      challengeCount: 0,
      demands: [],
      currentDP: 1,
      demandCount: 0,
      creatorid: null,
      creatorname: '',
      currentUserID: -1,
      showDialog: false,
      newTag: '',
      newTags: [],
      canTag: checkAuth(),
      short: true
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
    // contributors () {
    //   return this.rutDetail.contributors
    // },
    // contributorIDList () {
    //   return this.rutDetail.contributoridlist
    // },
    credential () {
      return this.rutDetail.credential
    },
    canEdit () {  // ???
      return this.creatorid === this.currentUserID
      // || this.rutDetail.editable === 'Everyone' || this.currentUserID in this.contributorIDList
    },
    canDelete () {
      return this.creatorid === this.currentUserID // ?
    },
    hasMoreDemand () {
      return this.demands.length < this.demandCount
    }
  },
  title () {
    return this.rutDetail.title
  },
  methods: {
    loadRutData () {
      let crutid = this.$route.params.id
      this.$store.dispatch('getRut', crutid)
      .then(resp => {
        let data = resp.data
        this.starCount = data.starcount
        this.challengeCount = data.challengecount
        this.creatorid = data.creator.id
        this.creatorname = data.creator.name
        this.currentUserID = this.$store.getters.currentUserID
        this.newTags = data.tags.map(t => t.tagname)
        this.demands = data.demands
        this.demandCount = data.demandcount
      })
    },
    loadmoreDemand () {
      let rutid = this.$route.params.id
      let params = {'page': this.currentDP}
      fetchRutDemands(rutid, params)
      .then(resp => {
        this.demands.push(...resp.data)
        this.currentDP += 1
      })
    },
    checkStar () {
      if (checkAuth()) {
        let rutid = this.$route.params.id // ?? liftcycle timing
        return checkSC(rutid, 'star')
        .then(resp => {
          this.starAction = resp.data
        })
      } else {
        return 'Star'
      }
    },
    checkChallenge () {
      if (checkAuth()) {
        let rutid = this.$route.params.id // ?? liftcycle timing
        return checkSC(rutid, 'challenge')
        .then(resp => {
          this.challengeAction = resp.data
        })
      } else {
        return 'Challenge'
      }
    },
    starRut () {
      if (checkAuth()) {
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
        this.$router.push({
          path: '/login',
          query: {redirect: this.$route.fullPath}
        })
      }
    },
    challengeRut () {
      if (checkAuth()) {
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
        this.$router.push({
          path: '/login',
          query: {redirect: this.$route.fullPath}
        })
      }
    },
    addNewTag () {
      this.newTags.push(this.newTag)
      this.newTag = ''
    },
    editTag () {
      if (checkAuth()) {
        let oldTags = this.tags.map(t => t.tagname)
        let newTags = this.newTags
        let data = {'old': oldTags, 'new': newTags}
        return editTags(this.rutid, data)
        .then(resp => {
          this.$store.commit('NEW_TAGS', resp.data)
          this.showDialog = false
        })
      } else {
        this.$message({
          showClose: true,
          message: 'Should Log in to Continue'
        })
        this.$router.push({
          path: '/login',
          query: {redirect: this.$route.fullPath}
        })
      }
    }
  },
  watch: {
    '$route': 'loadRutData' // render re-used component for addtorut
  },
  created () {
    this.loadRutData()
  }
}
</script>

<style lang="stylus" scoped>
$bgcolor = lighten(#f6f6f1, 50%)
.rut-page
  padding 10px 250px 10px 0px
  position relative
  .rut-view
    background-color lighten(#eceef1, 50%)
    padding auto
    .title
      padding 0 10px
      .meta 
        color #828282
        font-size 0.8em
    .intro
      background-color $bgcolor
      padding 5px 10px
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
    .bottombar
      font-size 0.85em
      padding 5px
      text-align right
  .indicator
    font-size 0.7em
    color #668e66
  .rut-side
    position absolute
    right 0
    top 10px
    width 240px
    .credential
      background-color #f5f9f5
      .credential-title
        background-color #dff0d8
        padding 10px
        color #3c763d
      .credential-body
        padding 0 10px
        min-height 45px
        font-size 0.85em
    .demands
      background-color white
      padding 5px
      margin-bottom 5px
      .demand-title
        font-size 0.85em
        a
          &:hover
            color #ff6600
</style>

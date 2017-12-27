<template>
  <div class="demand-page">
    <div class="demand-main">
      <demand :demand="demandDetail" :key="demandDetail.id"></demand>
      <div class="answer">
        <b>Answers to This Demand:</b>
        <el-button size="mini" type="text" @click="loadCreatedThenAsAnswer">...Link To Answer</el-button>
        <p class="title" v-for="(rut, index) in answers" :key="index" :rut="rut">
          - <router-link :to="'/readuplist/' + rut.id" :title="rut.title"> {{ rut.title.slice(0, 160) }}...</router-link>
        </p>
      </div>
      <div class="share">
        <share-bar></share-bar>
      </div>
      <!-- link to a rut as answer dialog -->
      <el-dialog title="Link A list as Answer" :visible.sync="showDialog" width="45%">
        <el-form :model="asForm" ref="asForm">
          <el-form-item prop="rut">
            <el-select v-model="asForm.selectRutID">
              <el-option v-for="r in createdRuts" :key="r.id" :label="r.title" :value="r.id"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button size="mini" @click="showDialog = false">Cancel</el-button>
          <el-button size="mini" type="success" @click="asAnswer('asForm', asForm)">As Answer</el-button>
        </div>
      </el-dialog>
      <!-- dialog end -->
      <div class="comment">
        <reply class="reply" :refer="refer" :show="true" @newreply="updateNew"></reply>
      </div>
      <div v-for="comment in comments" :key="comment.id">
        <comment :comment="comment"></comment>
      </div>
      <div v-if="hasMoreComment">
        <el-button class="blockbtn" @click="loadmoreComment" :disabled="!hasMoreComment">More</el-button>
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
import ShareBar from '@/components/Misc/ShareBar.vue'
import { fetchProfileRuts, rutAsAnswer, fetchDemandComments } from '@/api/api'
import { checkAuth } from '@/util/auth'
import { mapGetters } from 'vuex'

export default {
  name: 'demand-view',
  title () {
    return this.demandDetail.body
  },
  components: { Demand, Comment, Reply, ShareBar },
  data () {
    return {
      refer: { re: 'demand', id: this.$route.params.id },
      answers: [],
      answerCount: 0,
      comments: [],
      commentCount: 0,
      currentPage: 1,
      showDialog: false,
      asForm: {
        selectRutID: null
      },
      createdRuts: []
    }
  },
  computed: {
    ...mapGetters([
      'demandDetail'
    ]),
    hasMoreComment () {
      return this.comments.length < this.commentCount
    }
  },
  methods: {
    loadDemandData () {
      let demandid = this.$route.params.id
      this.$store.dispatch('getDemand', demandid)
      .then(resp => {
        let data = resp.data
        this.answers = data.answers
        this.answerCount = data.answercount
        this.comments = data.comments
        this.commentCount = data.commentcount
      })
    },
    updateNew (data) {
      this.comments.unshift(data)
    },
    loadmoreComment () {
      let params = {'page': this.currentPage}
      fetchDemandComments(this.demandDetail.id, params)
      .then(resp => {
        this.comments.push(...resp.data)
        this.currentPage += 1
      })
    },
    // get created ruts then link to demand as answer
    loadCreatedThenAsAnswer () {
      if (checkAuth()) {
        let userid = this.$store.getters.currentUserID
        return fetchProfileRuts('created', userid)
        .then(resp => {
          this.createdRuts = resp.data.ruts
          this.showDialog = true
        })
      } else {
        this.showDialog = false
        this.$message({
          showClose: true,
          message: 'Should Log in to Access'
        })
        this.$router.push({
          path: '/login',
          query: {redirect: this.$route.fullPath}
        })
      }
    },
    asAnswer (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid && checkAuth()) {
          let rutid = form.selectRutID
          let demandid = this.demandDetail.id
          return rutAsAnswer(rutid, demandid)
          .then((resp) => {
            this.showDialog = false
            this.$message({
              showClose: true,
              message: 'Link a New Answer, Done',
              type: 'success'
            })
            this.answers.push(resp.data)
          })
        } else {
          this.showDialog = false
          this.$message({
            showClose: true,
            message: 'Should Log in to Access'
          })
        }
      })
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
.el-select
  width 100%
</style>

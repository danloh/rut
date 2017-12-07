<template>
  <div class="demand-page">
    <div class="demand-main">
      <demand :demand="demand"></demand>
      <div class="answer">
        <b>The Answers to This Demand:</b>
        <p v-for="(rut, index) in answers" :key="index" :rut="rut">
          - <router-link :to="'/readuplist/' + rut.id" :title="rut.title"> {{ rut.title.slice(0, 160) }}...</router-link>
        </p>
      </div>
      <div class="comment">
        <b>Discuss</b>
        <el-form :model="commentForm" :rules="rules" ref="commentForm">
          <el-form-item prop="comment" style="margin-bottom:8px">
            <el-input v-model="commentForm.comment" placeholder="Post a Comment"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button size="mini" @click="submitComment('commentForm', commentForm)">Submit</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="submenu">
        &nbsp;&nbsp;&nbsp;
      </div>
      <div class="comment-view">
        <router-view></router-view>
      </div>
    </div>
    <div class="demand-side">
    </div>
  </div>
</template>

<script>
import Demand from '@/components/Demand/Demand.vue'
import { fetchDemand } from '@/api/api'
// import { mapGetters } from 'vuex'

export default {
  name: 'demand-view',
  title () {
    return this.demand.body
  },
  components: { Demand },
  data () {
    return {
      demand: null,
      commentForm: {
        comment: ''
      },
      rules: {
        comment: [{ required: true, message: 'Required', trigger: 'blur' }]
      }
    }
  },
  computed: {
    answers () {
      return this.demand.answers
    }
  },
  methods: {
    submitDemand (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = { comment: form.comment }
          this.$store.dispatch('postComment', data)
          this.resetForm(formName)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  },
  created () {
    let demandid = this.$route.params.id
    return fetchDemand(demandid)
    .then(resp => {
      this.demand = resp.data
    })
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
    .submenu
        margin-bottom 5px
        a
          color grey
          margin-right 0.85em
          &:hover
            color darkgreen
          &.router-link-active
            color orange
            font-weight 800
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


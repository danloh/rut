<template>
  <div class="review-page">
    <h3 class="title"> Edit Review</h3>
    <el-form class="review-form" :model="reviewForm" :rules="rules" ref="reviewForm" size="mini">
      <el-form-item prop="title">
        <el-input v-model="reviewForm.title"></el-input>
      </el-form-item>
      <el-form-item prop="review">
        <!-- <el-input type="textarea" :rows="16" v-model="reviewForm.review"></el-input> -->
        <quill-editor v-model="reviewForm.review"
                      ref="TextEditor"
                      class="quill-editor">
        </quill-editor>
      </el-form-item>
      <el-form-item prop="spoiler">
        <el-radio-group v-model="reviewForm.spoiler">
          <el-radio-button label="No Spoiler"></el-radio-button>
          <el-radio-button label="Spoiler Ahead"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="success" size="medium" @click="onEdit('reviewForm', reviewForm)" :disabled="!canEdit">Done and Submit</el-button>
        <!-- <el-button @click="resetForm('reviewForm')">Reset</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { editReview, fetchReview } from '@/api/api'
import { checkAuth } from '@/util/auth'

export default {
  name: 'edit-review',
  title: 'Edit Review',
  data () {
    return {
      reviewForm: {
        title: '',
        review: '',
        spoiler: ''
      },
      rules: {
        title: [
          { required: true, message: 'Required', trigger: 'change' }
        ],
        review: [
          { required: true, message: 'Required', trigger: 'change' }
        ]
      },
      canEdit: false
    }
  },
  methods: {
    onEdit (formName, form) {
      if (!this.canEdit) {
        this.$message({
          showClose: true,
          message: 'No Permission'
        })
        return false
      }
      this.$refs[formName].validate((valid) => {
        if (valid && checkAuth() && this.canEdit) {
          let data = {
            title: form.title,
            review: form.review,
            spoiler: form.spoiler
          }
          let reviewid = this.$route.params.id
          editReview(reviewid, data)
          .then(() => {
            this.$router.push(`/review/${reviewid}`)
          }).catch(error => {
            this.$message({
              showClose: true,
              message: error.response.statusText
            })
          })
        } else if (!checkAuth()) {
          this.$message({
            showClose: true,
            message: 'Should Log in to Continue'
          })
          this.$router.push({
            path: '/login',
            query: {redirect: this.$route.fullPath}
          })
        } else {
          this.$message({
            showClose: true,
            message: 'error!! Please Check'
          })
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    loadReviewData () {
      let reviewid = this.$route.params.id
      fetchReview(reviewid)
      .then(resp => {
        let data = resp.data
        this.reviewForm.title = data.heading
        this.reviewForm.review = data.body
        this.reviewForm.spoiler = data.spoiler ? 'Spoiler Ahead' : 'No Spoiler'
        let creatorID = data.creator.id
        let currentUserID = this.$store.getters.currentUserID
        this.canEdit = Number(creatorID) === Number(currentUserID)
      })
    }
  },
  created () {
    this.loadReviewData()
    // if (!this.canEdit) {
    //   this.$router.push(`/review/${this.$route.params.id}`)
    //   this.$message({
    //     showClose: true,
    //     message: 'No Permission to Edit'
    //   })
    // }
  }
}
</script>

<style lang="stylus" scoped>
.review-page
  padding 10px 160px
  position relative
  .review-form
    padding 20px
    border 1px dotted #689f38
  .title
    margin-bottom 20px
</style>
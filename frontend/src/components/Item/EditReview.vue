<template>
  <div class="review-page">
    <h3 class="title"> Edit Review</h3>
    <el-form class="review-form" :model="reviewForm" :rules="rules" ref="reviewForm" size="mini">
      <el-form-item prop="title">
        <el-input v-model="reviewForm.title"></el-input>
      </el-form-item>
      <el-form-item prop="review">
        <el-input type="textarea" :rows="16" v-model="reviewForm.review"></el-input>
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
    var notNull = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Can not be null'))
      } else {
        callback()
      }
    }
    return {
      reviewForm: {
        title: '',
        review: ''
      },
      rules: {
        title: [
          { validator: notNull, message: 'Required', trigger: 'change' }
        ],
        review: [
          { validator: notNull, message: 'Required', trigger: 'change' }
        ]
      },
      creatorID: -1,
      currentUserID: this.$store.getters.currentUserID,
      canEdit: Number(this.creatorID) === Number(this.currentUserID)
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
        if (valid && checkAuth()) {
          let data = {
            title: form.title,
            review: form.review
          }
          let reviewid = this.$route.params.id
          editReview(reviewid, data)
          .then(() => {
            this.$router.push(`/review/${reviewid}`)
          }).catch(error => {
            this.$message.error(error.status)
          })
        } else {
          console.log('error submit!!')
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
        this.creatorID = data.creator.id
        this.currentUserID = this.$store.getters.currentUserID
        this.canEdit = Number(this.creatorID) === Number(this.currentUserID)
      })
    }
  },
  created () {
    this.loadReviewData()
  }
}
</script>

<style lang="stylus" scoped>
.review-page
  padding 10px 180px
  position relative
  .review-form
    padding 20px
    border 1px dotted #689f38
  .title
    margin-bottom 20px
</style>
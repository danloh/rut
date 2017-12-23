<template>
  <div class="review-page">
    <h3 class="title"> Post New Review:</h3>
    <router-link :to="'/item/' + itemId" target="_blank" rel="nofollow noopener noreferrer">Item</router-link>
    <el-form class="review-form" :model="reviewForm" :rules="rules" ref="reviewForm" size="mini">
      <el-form-item prop="title">
        <el-input v-model="reviewForm.title" placeholder="Title"></el-input>
      </el-form-item>
      <el-form-item prop="review">
        <mavon-editor 
          v-model="reviewForm.review" 
          placeholder="Post Review"
          :language="'en'"
          :subfield="false"
          :toolbars="{
            bold: true,
            mark: true,
            quote: true,
            link: true,
            ol: true,
            ul: true,
            code: true,
            fullscreen: true,
            preview: true
          }">
        </mavon-editor>
      </el-form-item>
      <el-form-item prop="spoiler">
        <el-radio-group v-model="reviewForm.spoiler">
          <el-radio-button label="No Spoiler"></el-radio-button>
          <el-radio-button label="Spoiler Ahead"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="success" size="medium" @click="onSubmit('reviewForm', reviewForm)">Submit</el-button>
        <!-- <el-button @click="resetForm('reviewForm')">Reset</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { newReview } from '@/api/api'

export default {
  name: 'new-review',
  title: 'Post New Review',
  data () {
    return {
      reviewForm: {
        title: '',
        review: 'Test',
        spoiler: 'No Spoiler'
      },
      rules: {
        title: [
          { required: true, message: 'Required', trigger: 'blur' }
        ],
        review: [
          { required: true, message: 'Required', trigger: 'blur' }
        ]
      },
      itemId: this.$route.params.id
    }
  },
  methods: {
    onSubmit (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = {
            title: form.title,
            review: form.review,
            spoiler: form.spoiler
          }
          let itemid = this.$route.params.id
          newReview(itemid, data)
          .then(() => {
            this.$router.push(`/item/${itemid}`)
          }).catch(error => {
            this.$message({
              showClose: true,
              message: error.response.statusText
            })
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
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
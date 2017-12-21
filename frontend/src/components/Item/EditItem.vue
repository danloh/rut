<template>
  <div class="edit-page">
    <h3 class="title"> Edit Item:&nbsp;&nbsp;
      <router-link class="title" :to="'/item/' + itemId">{{itemTitle}}</router-link>
    </h3>
    <el-form class="edit-form" :model="itemForm" :rules="rules" ref="itemForm" label-width="120px" size="mini">
      <el-form-item label="Type" prop="cate">
        <el-radio-group v-model="itemForm.cate">
          <el-radio-button label="Book"></el-radio-button>
          <el-radio-button label="Video"></el-radio-button>
          <el-radio-button label="Online"></el-radio-button>
          <el-radio-button label="Album"></el-radio-button>
          <el-radio-button label="Other"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="Title" prop="title">
        <el-input v-model="itemForm.title"></el-input>
      </el-form-item>
      <el-form-item label="UID" prop="uid">
        <el-input v-model="itemForm.uid"></el-input>
      </el-form-item>
      <el-form-item label="Resource URL" prop="resurl">
        <el-input v-model="itemForm.resUrl"></el-input>
      </el-form-item>
      <el-form-item label="Byline" prop="byline">
        <el-input v-model="itemForm.byline"></el-input>
      </el-form-item>
      <el-form-item label="Cover" prop="cover">
        <el-input v-model="itemForm.cover"></el-input>
      </el-form-item>
      <el-form-item label="Language" prop="language">
        <el-input v-model="itemForm.language"></el-input>
      </el-form-item>
      <el-form-item label="Publisher" prop="publisher">
        <el-input v-model="itemForm.publisher"></el-input>
      </el-form-item>
      <el-form-item label="Publish Date" prop="publishDate">
        <el-input v-model="itemForm.publishDate"></el-input>
      </el-form-item>
      <el-form-item label="Page" prop="page">
        <el-input v-model="itemForm.page"></el-input>
      </el-form-item>
      <el-form-item label="Level" prop="level">
        <el-input v-model="itemForm.level"></el-input>
      </el-form-item>
      <el-form-item label="Binding" prop="binding">
        <el-input v-model="itemForm.binding"></el-input>
      </el-form-item>
      <el-form-item label="Price" prop="price">
        <el-input v-model="itemForm.price"></el-input>
      </el-form-item>
      <el-form-item label="More Details" prop="details">
        <el-input type="textarea" v-model="itemForm.details"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="success" size="medium" @click="onEditItem('itemForm', itemForm)">Done and Add</el-button>
        <!-- <el-button @click="resetForm('itemForm')">Reset</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { editItem } from '@/api/api'
import { checkAuth } from '@/util/auth'

export default {
  name: 'edit-item',
  title: 'Edit Item',
  data () {
    return {
      itemForm: {
        cate: 'Book',
        title: '',
        uid: '',
        resUrl: '',
        byline: '',
        cover: '',
        language: '',
        publisher: '',
        publishDate: '',
        level: '',
        binding: '',
        page: '',
        price: '',
        details: ''
      },
      rules: {
        title: [
          { required: true, message: 'Please give a title', trigger: 'blur' }
        ],
        uid: [
          { required: true, message: 'Need an uid', trigger: 'blur' }
        ]
      },
      itemId: null,
      itemTitle: null
    }
  },
  methods: {
    onEditItem (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid && checkAuth()) {
          let data = {
            cate: form.cate,
            title: form.title,
            uid: form.uid,
            resUrl: form.resUrl,
            byline: form.byline,
            cover: form.cover,
            language: form.language,
            publisher: form.publisher,
            publishDate: form.publishDate,
            level: form.level,
            binding: form.binding,
            page: form.page,
            price: form.price,
            details: form.details
          }
          editItem(this.itemId, data)
          .then((resp) => {
            let id = this.itemId
            this.$router.push(`/item/${id}`)
            this.$message({
              showClose: true,
              message: resp.data,
              type: 'success'
            })
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
    },
    loadItemData () {
      let item = this.$store.getters.currentItem
      if (item.id === Number(this.$route.params.id)) {
        this.itemForm.cate = item.cate
        this.itemForm.title = item.title
        this.itemForm.uid = item.uid
        this.itemForm.resUrl = item.resurl
        this.itemForm.byline = item.byline
        this.itemForm.cover = item.cover
        this.itemForm.language = item.language
        this.itemForm.publisher = item.publisher
        this.itemForm.publishDate = item.pubdate
        this.itemForm.level = item.level
        this.itemForm.binding = item.binding
        this.itemForm.price = item.price
        this.itemForm.page = item.page
        this.itemForm.details = item.details
        this.itemId = item.id
        this.itemTitle = item.title
      }
    }
  },
  created () {
    this.loadItemData()
  }
}
</script>

<style lang="stylus" scoped>
.edit-page
  padding 10px 120px 10px 80px
  position relative
  .edit-form
    padding 20px
    border 1px dotted #689f38
  .title
    margin-bottom 20px
</style>
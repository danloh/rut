<template>
  <div class="add-page">
    <h3 class="title"> Add Item to Readup Tips:
      <router-link class="title" :to="'/readuplist/' + rutId">{{rutTitle}}</router-link>
    </h3>
    <spinner :show="loading"></spinner>
    <!-- check via url spider or UID -->
    <el-form class="add-form" :model="checkForm" ref="checkForm" size="mini" v-show="!show">
      <el-form-item label="Amazon URL or ISBN-13" prop="url">
        <el-input v-model="checkForm.url"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="success" size="medium" @click="onCheck('checkForm', checkForm)">Fetch Via Spider</el-button>
      </el-form-item>
    </el-form>
    <el-button size="mini" @click="altShow">Fetch Item Info via Spider or Manually</el-button>
    <!-- add mannually -->
    <el-form class="add-form" :model="addForm" :rules="addRules" ref="addForm" label-width="120px" size="mini" v-show="show">
      <el-form-item label="Type" prop="cate">
        <el-radio-group v-model="addForm.cate">
          <el-radio-button label="Book"></el-radio-button>
          <el-radio-button label="Video"></el-radio-button>
          <el-radio-button label="Online"></el-radio-button>
          <el-radio-button label="Album"></el-radio-button>
          <el-radio-button label="Other"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="Title" prop="title">
        <el-input v-model="addForm.title"></el-input>
      </el-form-item>
      <el-form-item label="UID" prop="uid">
        <el-input v-model="addForm.uid"></el-input>
      </el-form-item>
      <el-form-item label="Resource URL" prop="resurl">
        <el-input v-model="addForm.resUrl"></el-input>
      </el-form-item>
      <el-form-item label="Byline" prop="byline">
        <el-input v-model="addForm.byline"></el-input>
      </el-form-item>
      <el-form-item label="Cover" prop="cover">
        <el-input v-model="addForm.cover"></el-input>
      </el-form-item>
      <el-form-item label="Tips" prop="tips">
        <el-input type="textarea" v-model="addForm.tips"></el-input>
      </el-form-item>
      <el-form-item label="in Tips" prop="spoiler">
        <el-radio-group v-model="addForm.spoiler">
          <el-radio-button label="No Spoiler"></el-radio-button>
          <el-radio-button label="Spoiler Ahead"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-button type="success" size="medium" @click="onAdd('addForm', addForm)">Done and Add</el-button>
        <!-- <el-button @click="resetForm('addForm')">Reset</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { checkItem, addItem } from '@/api/api'
import { checkAuth } from '@/util/auth'
import Spinner from '@/components/Misc/Spinner.vue'

export default {
  name: 'add-rut',
  title: 'Add Item to Readup Tips',
  components: { Spinner },
  data () {
    return {
      checkForm: {
        url: ''  // actually  url or uid
      },
      addForm: {
        cate: 'Book',
        title: '',
        uid: '',
        resUrl: '',
        byline: '',
        cover: '',
        tips: '',
        spoiler: 'No Spoiler'
      },
      addRules: {
        title: [
          { required: true, message: 'Please give a title', trigger: 'blur' }
        ],
        uid: [
          { required: true, message: 'Need an UID', trigger: 'blur' }
        ],
        tips: [
          { required: true, message: 'Required', trigger: 'blur' }
        ],
        resUrl: [
          { required: true, message: 'Required', trigger: 'blur' }
        ]
      },
      show: false,
      loading: false,
      rutId: null,
      rutTitle: null,
      canEdit: false
    }
  },
  methods: {
    // via Spider
    onCheck (formName, form) {
      this.loading = true
      this.$refs[formName].validate((valid) => {
        if (valid && checkAuth() && this.canEdit) {
          let data = {
            url: form.url
          }
          checkItem(this.rutId, data)
          .then(resp => {
            let id = this.rutId
            if (resp.data === 'Back') {
              this.$message({
                showClose: true,
                message: 'Faill to add, no such item, You can Try again via an Amazon url'
              })
            }
            this.loading = false
            this.$router.push(`/readuplist/${id}`)
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
    // manually add
    onAdd (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid && checkAuth() && this.canEdit) {
          let data = {
            title: form.title,
            uid: form.uid,
            resUrl: form.resUrl,
            byline: form.byline,
            cover: form.cover,
            tips: form.tips,
            spoiler: form.spoiler
          }
          addItem(this.rutId, data)
          .then(() => {
            let id = this.rutId
            this.$router.push(`/readuplist/${id}`)
            // this.$message({
            //   showClose: true,
            //   message: 'add Done'
            // })
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
    loadRutData () {
      let rut = this.$store.getters.rutDetail
      let creatorID = rut.creator.id
      let currentUserID = this.$store.getters.currentUserID
      this.canEdit = Number(creatorID) === Number(currentUserID)
      if (rut.id === Number(this.$route.params.id)) {
        this.rutId = rut.id
        this.rutTitle = rut.title
      }
    },
    altShow () {
      this.show = !this.show
    }
  },
  created () {
    this.loadRutData()
  }
}
</script>

<style lang="stylus" scoped>
.add-page
  padding 10px 120px 10px 80px
  position relative
  .add-form
    padding 20px
    border 1px dotted #689f38
  .title
    margin-bottom 20px
</style>
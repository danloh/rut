<template>
  <div class="add-page">
    <h3 class="title"> Add Item to Readup Tips:
      <router-link class="title" :to="'/readuplist/' + rutId">{{rutTitle}}</router-link>
    </h3>
    <!-- check -->
    <el-form class="check-form" :model="checkForm" ref="checkForm" label-width="120px" size="mini">
      <el-form-item label="URL" prop="url">
        <el-input v-model="checkForm.url"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="success" size="medium" @click="onCheck('checkForm', checkForm)">Submit</el-button>
      </el-form-item>
    </el-form>
    <!-- add mannually -->
    <el-form class="add-form" :model="addForm" :rules="addRules" ref="addForm" label-width="120px" size="mini">
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
      <el-form-item>
        <el-button type="success" size="medium" @click="onAdd('addForm', addForm)">Done and Add</el-button>
        <!-- <el-button @click="resetForm('addForm')">Reset</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { addItem } from '@/api/api'

export default {
  name: 'add-rut',
  title: 'Add Item to Readup Tips',
  data () {
    return {
      checkForm: {
        url: ''
      },
      addForm: {
        cate: 'Book',
        title: '',
        uid: '',
        resUrl: '',
        byline: '',
        cover: '',
        tips: ''
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
          { required: this.addForm.cate === 'Online', message: 'Required', trigger: 'blur' }
        ]
      },
      rutId: null,
      rutTitle: null
    }
  },
  methods: {
    onAdd (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = {
            title: form.title,
            intro: form.intro,
            rating: form.rating,
            credential: form.credential,
            epilog: form.epilog
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
            this.$message.error(error.status) // elementui
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
      if (rut.id === Number(this.$route.params.id)) {
        this.addForm.title = rut.title
        this.addForm.intro = rut.intro
        this.addForm.rating = rut.rating
        this.addForm.credential = rut.credential
        this.addForm.epilog = rut.epilog
        this.rutId = rut.id
        this.rutTitle = rut.title
      }
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
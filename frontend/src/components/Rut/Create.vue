<template>
  <div class="create-page">
    <h3 class="title">Create New Readup Tips</h3>
    <p v-if="demandid"> As Answer To A <router-link :to="'/demand/' + demandid" target="_blank" rel="nofollow noopener noreferrer">Request</router-link></p>
    <el-form class="create-form" :model="createForm" :rules="rules" ref="createForm" label-width="120px" size="mini">
      <el-form-item label="Title" prop="title">
        <el-input v-model="createForm.title"></el-input>
      </el-form-item>
      <el-form-item label="Preface" prop="intro">
        <el-input type="textarea" :rows="3" v-model="createForm.intro"></el-input>
      </el-form-item>
      <el-form-item label="Tag" prop="tag">
        <el-input v-model="createForm.tag"></el-input>
      </el-form-item>
      <el-form-item label="Credential" prop="credential">
        <el-input type="textarea" v-model="createForm.credential"></el-input>
      </el-form-item>
      <el-form-item label="Rating" prop="rating">
        <el-select v-model="createForm.rating">
          <el-option v-for="r in ratings" :key="r.value" :label="r.label" :value="r.value"></el-option>
        </el-select>
      </el-form-item>
      <!-- <el-form-item label="Who Can Edit?" prop="editable">
        <el-radio-group v-model="createForm.editable">
          <el-radio-button label="Creator"></el-radio-button>
          <el-radio-button label="Contributors"></el-radio-button>
          <el-radio-button label="Everyone"></el-radio-button>
        </el-radio-group>
      </el-form-item> -->
      <el-form-item>
        <el-button type="success" size="medium" @click="onCreate('createForm', createForm)">Create New Then Add Item Later</el-button>
        <!-- <el-button @click="resetForm('createForm')">Reset</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { newRut } from '@/api/api'

export default {
  name: 'create',
  title: 'Create New',
  data () {
    return {
      createForm: {
        title: '',
        intro: '',
        tag: '',
        rating: 'All',
        credential: '',
        editable: 'Creator'
      },
      rules: {
        title: [
          { required: true, message: 'Please give a title', trigger: 'blur' }
        ],
        intro: [
          { required: true, message: 'Need an introduction', trigger: 'blur' }
        ],
        tag: [
          { required: true, message: 'Please set some tags', trigger: 'blur' }
        ]
      },
      ratings: [
        {value: 'All', label: 'All'}, {value: 'Secondary', label: 'Secondary'},
        {value: 'College', label: 'College'}, {value: 'Elementary', label: 'Elementary'},
        {value: 'Preschool', label: 'Preschool'}, {value: 'Professional', label: 'Professional'}
      ],
      demandid: this.$route.params.id || ''
    }
  },
  methods: {
    onCreate (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = {
            title: form.title,
            intro: form.intro,
            tag: form.tag,
            rating: form.rating,
            credential: form.credential,
            editable: 'Creator' // form.editable
          }
          let demandid = this.$route.params.id || ''
          return newRut(data, demandid)
          .then((resp) => {
            let id = resp.data.id
            // this.$store.commit('SET_', data)
            this.$router.push(`/readuplist/${id}`)
            this.$message({
              showClose: true,
              message: 'A New tips Created, Now you can add item to it'
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
    }
  }
}
</script>

<style lang="stylus" scoped>
.create-page
  padding 10px 120px 10px 80px
  position relative
  .create-form
    padding 20px
    border 1px dotted #689f38
  .title
    text-align center
    margin-bottom 20px
</style>
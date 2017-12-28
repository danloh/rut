<template>
  <div class="edit-page">
    <h3 class="title"> Edit Readup Tips:
      <router-link class="title" :to="'/readuplist/' + rutId">{{rutTitle}}</router-link>
    </h3>
    <el-form class="edit-form" :model="editForm" :rules="rules" ref="editForm" label-width="120px" size="mini">
      <el-form-item label="Title" prop="title">
        <el-input v-model="editForm.title"></el-input>
      </el-form-item>
      <el-form-item label="Preface" prop="intro">
        <!-- <el-input type="textarea" :rows="3" v-model="editForm.intro"></el-input> -->
        <quill-editor v-model="editForm.intro"
                      ref="TextEditor"
                      class="quill-editor">
        </quill-editor>
      </el-form-item>
      <el-form-item label="Credential" prop="credential">
        <el-input type="textarea" v-model="editForm.credential"></el-input>
      </el-form-item>
      <el-form-item label="Epilog" prop="epilog">
        <!-- <el-input type="textarea" :rows="3" v-model="editForm.epilog"></el-input> -->
        <quill-editor v-model="editForm.epilog"
                      ref="TextEditor"
                      class="quill-editor">
        </quill-editor>
      </el-form-item>
      <!-- <el-form-item label="Who Can Edit?" prop="editable">
        <el-radio-group v-model="editForm.editable">
          <el-radio-button label="Creator"></el-radio-button>
          <el-radio-button label="Contributors"></el-radio-button>
          <el-radio-button label="Everyone"></el-radio-button>
        </el-radio-group>
      </el-form-item> -->
      <el-form-item label="Rating" prop="rating">
        <el-select v-model="editForm.rating">
          <el-option v-for="r in ratings" :key="r.value" :label="r.label" :value="r.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="success" size="medium" @click="onEdit('editForm', editForm)">Done and Submit</el-button>
        <!-- <el-button @click="resetForm('editForm')">Reset</el-button> -->
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { editRut } from '@/api/api'
import { checkAuth } from '@/util/auth'

export default {
  name: 'edit-rut',
  title: 'Edit Readup Tips',
  data () {
    return {
      editForm: {
        title: '',
        intro: '',
        tag: '',
        rating: '',
        credential: '',
        epilog: ''
      },
      rules: {
        title: [
          { required: true, message: 'Please give a title', trigger: 'blur' }
        ],
        intro: [
          { required: true, message: 'Need an introduction', trigger: 'blur' }
        ]
      },
      ratings: [
        {value: 'All', label: 'All'}, {value: 'Secondary', label: 'Secondary'},
        {value: 'College', label: 'College'}, {value: 'Elementary', label: 'Elementary'},
        {value: 'Preschool', label: 'Preschool'}, {value: 'Professional', label: 'Professional'}
      ],
      rutId: null,
      rutTitle: null,
      canEdit: false
    }
  },
  methods: {
    onEdit (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid && checkAuth() && this.canEdit) {
          let data = {
            title: form.title,
            intro: form.intro,
            rating: form.rating,
            credential: form.credential,
            epilog: form.epilog
          }
          editRut(this.rutId, data)
          .then(() => {
            let id = this.rutId
            this.$router.push(`/readuplist/${id}`)
            // this.$message({
            //   showClose: true,
            //   message: 'Edit Done'
            // })
          }).catch(error => {
            this.$message({
              showClose: true,
              message: error.response.statusText
            })
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
    loadRutData () {
      let rut = this.$store.getters.rutDetail
      if (rut.id === Number(this.$route.params.id)) {
        this.editForm.title = rut.title
        this.editForm.intro = rut.intro
        this.editForm.rating = rut.rating
        this.editForm.credential = rut.credential
        this.editForm.epilog = rut.epilog
        this.rutId = rut.id
        this.rutTitle = rut.title
        let creatorID = rut.creator.id
        let currentUserID = this.$store.getters.currentUserID
        this.canEdit = Number(creatorID) === Number(currentUserID)
      }
    }
  },
  created () {
    this.loadRutData()
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
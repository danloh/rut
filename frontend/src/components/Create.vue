<template>
  <el-form :model="createForm" :rules="rules" ref="createForm" label-width="100px">
    <el-form-item label="Title" prop="title">
      <el-input v-model="createForm.title"></el-input>
    </el-form-item>
    <el-form-item label="Preface" prop="intro">
      <el-input v-model="createForm.intro"></el-input>
    </el-form-item>
    <el-form-item label="Tag" prop="tag">
      <el-input v-model="createForm.tag"></el-input>
    </el-form-item>
    <el-form-item label="Rating" prop="rating">
      <el-select v-model="createForm.rating">
        <el-option v-for="r in ratings" :key="r.value" :label="r.label" :value="r.value"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Credential" prop="credential">
      <el-input v-model="createForm.credential"></el-input>
    </el-form-item>
    <el-form-item label="Who Can Edit?" prop="editable">
      <el-radio-group v-model="createForm.editable">
        <el-radio-button label="Creator"></el-radio-button>
        <el-radio-button label="Contributors"></el-radio-button>
        <el-radio-button label="Everyone"></el-radio-button>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onCreate('createForm', createForm)">Create New</el-button>
      <el-button @click="resetForm('createForm')">Reset</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
export default {
  name: 'create',
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
      ]
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
            editable: form.credential
          }
          this.$axios.post('api/create', data).then((resp) => {
            let id = resp.data.id
            // this.$store.commit('SET_', data)
            this.$router.push(`/readuplist/${id}`)
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
    }
  }
}
</script>
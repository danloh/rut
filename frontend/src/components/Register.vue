<template>
  <el-form :model="regForm" :rules="rules" ref="regForm">
    <el-form-item label="Username" prop="username">
      <el-input v-model="regForm.username"></el-input>
    </el-form-item>
    <el-form-item label="Password" prop="password">
      <el-input v-model="regForm.password"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onReg('regForm', regForm)">Sign Up</el-button>
      <el-button @click="resetForm('regForm')">Reset</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
export default {
  name: 'register',
  title: 'Register',
  data () {
    return {
      regForm: {
        username: '',
        email: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: 'Please enter username', trigger: 'blur' }
        ],
        password: [
          { required: true, message: 'Please enter password', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    onReg (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = {
            username: form.username,
            email: form.email,
            password: form.password
          }
          this.$axios.post('api/register', data).then((resp) => {
            let data = resp.data
            this.$store.commit('SET_TOKEN', data)
            this.$router.push('/')
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
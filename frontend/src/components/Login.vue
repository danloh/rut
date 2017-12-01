<template>
  <el-row><el-col :span="8" :offset="8"><div>
    <el-form class="card-box" :model="loginForm" :rules="rules" ref="loginForm">
      <h3>Please Log in</h3>
      <el-form-item prop="username">
        <el-input v-model="loginForm.username" placeholder="Username"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input :type="pwdType" v-model="loginForm.password" placeholder="Password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onLogin('loginForm', loginForm)">Log in</el-button>
      </el-form-item>
    </el-form>
  </div></el-col></el-row>
</template>
<script>
export default {
  name: 'login',
  title: 'Log in',
  data () {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [{ required: true, message: 'Please enter username', trigger: 'blur' }],
        password: [{ required: true, message: 'Please enter password', trigger: 'blur' }]
      },
      pwdType: 'password'
    }
  },
  methods: {
    onLogin (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios.defaults.auth = {
            username: form.username,
            password: form.password
          }
          this.$axios.get('api/login').then((resp) => {
            let data = resp.data
            this.$store.commit('SET_TOKEN', data.token)
            this.$store.commit('MOD_USER', data.user)
            this.$router.push('/')
          }).catch(error => {
            this.$message.error(error.status) // elementui
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>
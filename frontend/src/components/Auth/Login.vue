<template>
  <div class="login-page">
    <h3 class="title">Please Log in</h3>
    <el-form class="login-form" :model="loginForm" :rules="rules" ref="loginForm">
      <el-form-item prop="username">
        <el-input v-model="loginForm.username" placeholder="Username"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input :type="pwdType" v-model="loginForm.password" placeholder="Password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button class="blockbtn" type="primary" @click="onLogin('loginForm', loginForm)">Log in</el-button>
      </el-form-item>
      <router-link :to="'/register'">No Account? Sign Up</router-link>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <router-link :to="'/forget'"> Forget Password?</router-link>
    </el-form>
  </div>
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
          this.$axios.get('api/login')
          .then((resp) => {
            let data = resp.data
            this.$store.commit('SET_TOKEN', data.token)
            this.$store.commit('SET_USER', data.userid)
            let nextUrl = this.$route.query.redirect || '/challenge' // uncompletely tackled!!
            this.$router.push(nextUrl)
          }).catch(() => {
            // this.$router.go(0)
            this.$message({
              showClose: true,
              duration: 0,
              message: 'oops...Please Check Account or Password',
              type: 'error'
            })
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

<style lang="stylus" scoped>
.login-page
  padding 10px 250px 10px 250px
  position relative
  .login-form
    padding 20px
    border 1px dotted #689f38
  .title
    text-align center
    margin-bottom 20px
</style>
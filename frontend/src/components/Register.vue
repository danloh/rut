<template>
<div class="sign-page">
  <h3 class="title">Welcome to Join in</h3>
  <el-form class="sign-form" :model="regForm" :rules="rules" ref="regForm" size="mini">
    <el-form-item label="Username" prop="username">
      <el-input v-model="regForm.username"></el-input>
    </el-form-item>
    <el-form-item label="Email" prop="email">
      <el-input v-model="regForm.email"></el-input>
    </el-form-item>
    <el-form-item label="Password" prop="password">
      <el-input :type="pwdType" v-model="regForm.password"></el-input>
    </el-form-item>
    <el-form-item label="Confirm Password" prop="repassword">
      <el-input :type="pwdType" v-model="regForm.repassword"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button class="blockbtn" type="primary" @click="onReg('regForm', regForm)">Sign Up</el-button>
      <br>
      <el-button @click="resetForm('regForm')">Reset</el-button>
    </el-form-item>
  </el-form>
</div>
</template>

<script>
export default {
  name: 'register',
  title: 'Register',
  data () {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the password'))
      } else {
        if (this.regForm.repassword !== '') {
          this.$refs.regForm.validateField('repassword')
        }
        callback()
      }
    }
    var validaterePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the password again'))
      } else if (value !== this.regForm.password) {
        callback(new Error('Two inputs do not match!'))
      } else {
        callback()
      }
    }
    return {
      regForm: {
        username: '',
        email: '',
        password: '',
        repassword: ''
      },
      rules: {
        username: [
          { required: true, message: 'Please enter username', trigger: 'blur' }
        ],
        email: [
          { required: true, message: 'Please enter email', trigger: 'blur' }
        ],
        password: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        repassword: [
          { required: true, validator: validaterePass, trigger: 'blur' }
        ]
      },
      pwdType: 'password'
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

<style lang="stylus" scoped>
.sign-page
  padding 10px 250px 10px 250px
  position relative
  .sign-form
    padding 20px
    border 1px dotted #689f38
  .title
    text-align center
    margin-bottom 20px
</style>
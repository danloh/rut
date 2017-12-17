<template>
<div class="sign-page">
  <h3 class="title">Welcome to Join in</h3>
  <el-form class="sign-form" :model="resetpswForm" :rules="rules" ref="resetpswForm" size="mini">
    <el-form-item label="Password" prop="password">
      <el-input :type="pwdType" v-model="resetpswForm.password"></el-input>
    </el-form-item>
    <el-form-item label="Confirm Password" prop="repassword">
      <el-input :type="pwdType" v-model="resetpswForm.repassword"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button class="blockbtn" type="primary" @click="onReset('resetpswForm', resetpswForm)">Sign Up</el-button>
      <br>
      <el-button @click="resetForm('resetpswForm')">Reset</el-button>
    </el-form-item>
  </el-form>
</div>
</template>

<script>
export default {
  name: 'resetpsw',
  title: 'Reset Password',
  data () {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the password'))
      } else {
        if (this.resetpswForm.repassword !== '') {
          this.$refs.resetpswForm.validateField('repassword')
        }
        callback()
      }
    }
    var validaterePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the password again'))
      } else if (value !== this.resetpswForm.password) {
        callback(new Error('Two inputs do not match!'))
      } else {
        callback()
      }
    }
    return {
      resetpswForm: {
        password: '',
        repassword: ''
      },
      rules: {
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
    onReset (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = {
            newpsw: form.password
          }
          let token = this.$route.params.token
          let params = {'token': token, 'data': data}
          this.$store.dispatch('resetPsw', params)
          .then((resp) => {
            this.$message({
              showClose: true,
              message: resp.data
            })
            this.$router.push('/login')
          }).catch(error => {
            this.$message.error(error.status)
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
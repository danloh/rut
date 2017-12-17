<template>
<div class="sign-page">
  <h3 class="title">Welcome to Join in</h3>
  <el-form class="sign-form" :model="changepswForm" :rules="rules" ref="changepswForm" size="mini">
    <el-form-item label="Password" prop="password">
      <el-input :type="pwdType" v-model="changepswForm.password"></el-input>
    </el-form-item>
    <el-form-item label="New Password" prop="newpassword">
      <el-input :type="pwdType" v-model="changepswForm.newpassword"></el-input>
    </el-form-item>
    <el-form-item label="Confirm New Password" prop="repassword">
      <el-input :type="pwdType" v-model="changepswForm.repassword"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button class="blockbtn" type="primary" @click="onChange('changepswForm', changepswForm)">Sign Up</el-button>
      <br>
      <el-button @click="resetForm('changepswForm')">Reset</el-button>
    </el-form-item>
  </el-form>
</div>
</template>

<script>
export default {
  name: 'changepsw',
  title: 'Change Password',
  data () {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the new password'))
      } else {
        if (this.changepswForm.repassword !== '') {
          this.$refs.changepswForm.validateField('repassword')
        }
        callback()
      }
    }
    var validaterePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the new password again'))
      } else if (value !== this.changepswForm.newpassword) {
        callback(new Error('Two inputs do not match!'))
      } else {
        callback()
      }
    }
    return {
      changepswForm: {
        password: '',
        newpassword: '',
        repassword: ''
      },
      rules: {
        password: [
          { required: true, message: 'Please enter Old Password', trigger: 'blur' }
        ],
        newpassword: [
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
    onChange (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = {
            oldpsw: form.password,
            newpsw: form.newpassword
          }
          this.$axios.post('api/changepassword', data).then((resp) => {
            this.$router.push('/login')
            this.$message({
              showClose: true,
              message: resp.data
            })
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
<template>
  <div class="confirm">
    <p>In Process: Comfirm your email account</p>
  </div>
</template>

<script>
export default {
  name: 'comfirm',
  title: 'Confirm Email Account',
  created () {
    let token = this.$route.params.token
    this.$store.dispatch('confirmEmail', token)
    .then(resp => {
      this.$message({
        showClose: true,
        message: resp.data
      })
      this.$router.push('/')
    })
  }
}
</script>

<style lang="stylus" scoped>
.confirm
  padding 10px 240px
</style>

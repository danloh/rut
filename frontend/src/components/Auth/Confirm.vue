<template>
  <div class="confirm">
    <spinner></spinner>
    <p>In Process: Comfirm your email account</p>
  </div>
</template>

<script>
import Spinner from '@/components/Misc/Spinner.vue'

export default {
  name: 'comfirm',
  title: 'Confirm Email Account',
  components: { Spinner },
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

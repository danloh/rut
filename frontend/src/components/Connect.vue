<template>
    <div class="text-center">
        <div>
            <h4>Please login, You can Connect With:</h4>
        </div>
        <hr>
        <div >
            <a href="/login/Google/">
                &nbsp;&nbsp;<b>Connect With Google</b>&nbsp;&nbsp;
            </a><br>
            <a href="/login/Facebook/">
                &nbsp;&nbsp;<b>Connect With Facebook</b>&nbsp;&nbsp;
            </a><br>
            <a href="http://127.0.0.1:5000/login/Twitter">
                &nbsp;&nbsp;<b>Connect With Twitter</b>&nbsp;&nbsp;
            </a>
        </div>
    </div>
</template>

<script>
export default {
  name: 'connect',
  data () {
    return {
      nexturl: this.$store.state.nexturl
    }
  }
}
</script>

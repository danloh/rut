<template>
    <div class="text-center">
        <div>
            <h4>Please login, You can Connect With:</h4>
        </div>
        <hr>
        <div class="btn btn-group-vertical">
            <a href="/login/Google/"+nexturl class="btn btn-lg btn-danger">
                &nbsp;&nbsp;<b>Connect With Google</b>&nbsp;&nbsp;
            </a><br>
            <a href="/login/Facebook/"+nexturl class="btn btn-lg btn-primary">
                &nbsp;&nbsp;<b>Connect With Facebook</b>&nbsp;&nbsp;
            </a><br>
            <a href="/login/Twitter/"+nexturl class="btn btn-lg btn-info">
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

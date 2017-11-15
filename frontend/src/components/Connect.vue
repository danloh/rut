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
            <button @click="authTwitter">
                &nbsp;&nbsp;<b>Connect With Twitter</b>&nbsp;&nbsp;
            </button>
        </div>
    </div>
</template>

<script>
import { auth } from '../api/api'

export default {
  name: 'connect',
  data () {
    return {
      nexturl: this.$store.state.nexturl
    }
  },

  methods: {
    authTwitter () {
      return auth('Twitter').then((resp) => {
        this.$store.state.user = resp.data
        this.$root.router.push('/')
      })
    }
  }
}
</script>

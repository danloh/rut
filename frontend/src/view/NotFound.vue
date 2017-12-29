<template>
  <div>
    <h1>404 Page Not Found</h1>
    <!-- <button @click="test">click test</button>
    <button @click="testWrapAPI">click wrap</button> -->
  </div>
</template>

<script>
import { testError } from '@/api/api'
export default {
  name: 'not-found',
  title: '404 Page Not Found',
  methods: {
    testWrapAPI () {
      testError().then(resp => { // wrapped api, interceptors nor work why??
        console.log('From Component')
        console.log(resp.data)
        console.log(resp.status)
        console.log(resp.headers)
        console.log(resp.config)
      })
    },
    test () {
      this.$axios.get('api/testerror') // interceptors work
      .then(resp => {
        console.log(resp.data)
        console.log(resp.status)
        console.log(resp.headers)
        console.log(resp.config)
      })
    }
  }
}
</script>

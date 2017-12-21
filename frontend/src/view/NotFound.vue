<template>
  <div>
    <h1>404 Page Not Found</h1>
    <!-- <button @click="test">click test</button> -->
  </div>
</template>

<script>
export default {
  name: 'not-found',
  title: '404 Page Not Found',
  methods: {
    test () {
      this.$axios.get('api/testerror')
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

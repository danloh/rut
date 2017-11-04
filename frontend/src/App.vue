<template>
  <div id="app">
    <header class="header">
      <nav class="inner">
        <router-link to="/">
            <b style="color:darkorange">Readup.Tips</b>
        </router-link>
        <router-link to="/challenge">
          <b>Challenge</b>
        </router-link>
        <router-link to="/demand">
          <b>Request</b>
        </router-link>
        <router-link to="/create">
          <b>Create Now</b>
        </router-link>
      </nav>
    </header>
    <div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import store from './store'

export default {
  name: 'app',
  mounted () {
    store.dispatch('VERIFY')  // check if logged-in
  }
}
</script>

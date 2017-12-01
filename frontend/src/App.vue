<template>
  <div id="app">
    <header class="header">
      <nav class="inner">
        <router-link to="/">
            <b style="color:darkorange; font-size:1.6em">Readup.Tips</b>
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
        <div class="rightmenu">
          <el-dropdown v-if="authed">
            <el-button type="success" size="small">
              <img class="profile" :src="avatar" alt="Avatar">
              <i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>Profile</el-dropdown-item>
              <el-dropdown-item>Setting</el-dropdown-item>
              <el-dropdown-item>
                <el-button size="small" @click="onLogout">Log out</el-button>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <div class="login" v-else>
            <router-link to="/register">Signup</router-link>
            <router-link to="/login">Login</router-link>
          </div>
        </div>
      </nav>
    </header>
    <div class="view">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
// import store from './store'
import { mapGetters } from 'vuex'

export default {
  name: 'app',
  computed: {
    ...mapGetters([
      'currentUser'
    ]),
    authed () {
      return this.currentUser !== null
    },
    avatar () {
      return this.currentUser.avatar
    }
  },
  methods: {
    onLogout () {
      this.$store.commit('DEL_TOKEN')
      this.$router.push('/')
    }
  },
  beforeDestroy () {
    this.onLogout()
  }
}
</script>

<style lang="stylus">
body
  font-family -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  font-size 16px
  line-height 1.6em
  background-color lighten(#eceef1, 30%)
  margin 0
  padding-top 42px
  color #34495e
  overflow-y scroll

a
  color #337ab7
  text-decoration none

.header
  background-color #fafafa
  position fixed
  z-index 999
  height 40px
  top 0
  left 0
  right 0
  .inner
    max-width 960px
    box-sizing border-box
    margin 0px auto
    padding 8px 0px
  a
    color grey
    line-height 24px
    display inline-block
    vertical-align middle
    font-weight 600
    letter-spacing .075em
    margin-right 0.85em
    &:hover
      color darkgreen
    &.router-link-active
      color green
      font-weight 800
  .rightmenu
    float right
    .profile
      width 14px
      height 14px
    .login
      a
        color green
        font-size 1.0em
        font-weight 700
.blockbtn
  display block
  width 100%
  text-align center
.view
  max-width 960px
  width 90%
  margin 0 auto
  position relative
</style>

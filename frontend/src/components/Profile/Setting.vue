<template>
  <div class="setting-page">
    <div class="setting-view">
      <router-view></router-view>
    </div>
    <div class="setting-side">
      <div class="right-avatar">
        <img class="avatar" :src="user.avatar" alt="Avatar">
        <p class="user-info">From: {{user.location || 'Unknown'}}</p>
      </div>
      <div class="right-nav">
        <router-link :to="'/setting/' + userid + '/setting'">Edit Profile</router-link>
        <br>
        <router-link :to="'/setting/' + userid + '/change'">Change Password</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchUser } from '@/api/api'
import { mapGetters } from 'vuex'

export default {
  name: 'setting',
  title: 'Setting',
  data () {
    return {
      user: {},
      userid: this.$route.params.id
    }
  },
  computed: {
    ...mapGetters([
      'currentUser'
    ])
  },
  beforeMount () {
    let userid = this.$route.params.id
    return fetchUser(userid)
    .then(resp => {
      this.user = resp.data
    })
  }
}
</script>

<style lang="stylus" scoped>
.setting-page
  padding 10px 240px 10px 0px
  position relative
  .setting-view
    padding auto
  .setting-side
    position absolute
    top 10px
    right 0
    width 220px
    background-color white
    .right-avatar
      background-color #e5ebe4
      min-height 80px
      padding 5px
      position relative
      .avatar
        width 60px
        height 80px
      .user-info
        position absolute
        top 10px
        right 0
        width 145px
    .right-nav
      padding 5px 20px
      a
        color grey
        line-height 28px
        font-weight 400
        &:hover
          color darkgreen
        &.router-link-active
          color green
          font-weight 800
</style>

<template>
  <div class="profile-page">
    <div class="profile-head">
      <b>{{user.name}}</b>
      <p class="aboutme">{{user.about || 'Not Introduce Self Yet'}}</p>
      <div class="fobar">
        <span>Following {{user.followedcount}} </span>
        &nbsp;<el-button size="mini">Follow</el-button>
      </div>
    </div>
    <div class="profile-view" :key="userid">
      <router-view></router-view>
    </div>
    <div class="profile-side">
      <div class="right-avatar">
        <img class="avatar" :src="user.avatar" alt="Avatar">
        <p class="user-info">From: {{user.location || 'Unknown'}}</p>
      </div>
      <div class="right-nav">
        <router-link :to="'/profile/' + userid + '/created/'">Created</router-link>
        <br>
        <router-link :to="'/profile/' + userid + '/challenge/'">Challenge</router-link>
        <br>
        <router-link :to="'/profile/' + userid + '/star/'">Star</router-link>
        <br>
        <router-link :to="'/profile/' + userid + '/working/'">Working On</router-link>
        <br>
        <router-link :to="'/profile/' + userid + '/scheduled/'">scheduled</router-link>
        <br>
        <router-link :to="'/profile/' + userid + '/havedone/'">Have Done</router-link>
        <br>
        <router-link :to="'/setting/' + userid" v-if="showSetting"><small>~Setting~</small></router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchUser } from '@/api/api'

export default {
  name: 'profile',
  title () {
    return this.user.name
  },
  data () {
    return {
      user: {},
      userid: this.$route.params.id,
      showSetting: false
    }
  },
  methods: {
    loadUser () {
      let userid = this.$route.params.id
      return fetchUser(userid)
      .then(resp => {
        this.user = resp.data
        this.userid = resp.data.id
        let currentUserID = this.$store.getters.currentUserID
        if (Number(userid) === Number(currentUserID)) {
          this.$store.commit('SET_INFO', resp.data)
          this.showSetting = true
        }
      })
    }
  },
  created () {
    this.loadUser()
  },
  watch: {
    '$route': 'loadUser'
  }
}
</script>

<style lang="stylus" scoped>
.profile-page
  padding 10px 240px 10px 0px
  position relative
  .profile-head
    background-color #f6f6f1
    border-bottom 1px dotted orange
    min-height 40px
    padding 10px 180px 10px 10px
    margin-bottom 10px
    position relative
    .fobar
      position absolute
      top 10px
      right 0
      width 160px
  .profile-view
    padding auto
  .profile-side
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
.aboutme, .user-info, .fobar
    font-size 0.85em
</style>

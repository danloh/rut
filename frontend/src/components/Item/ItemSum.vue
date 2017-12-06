<template>
  <div class="itemsum">
    <div>
      <img class="thumb" :src="cover" alt="Cover">
    </div>
    <div class="info">
      <span class="title">
        {{item.cate}} <router-link :to="'/item/' + item.id">{{ item.title }}</router-link>
      </span><br>
      <span><b>Byline:</b> {{ item.byline }} </span><br>
      <span><b>Published:</b> {{ item.publisher }} @ {{ item.pubdate }} # {{ item.language }}</span><br>
      <span><b>UID/ISBN:</b> {{ item.uid }} ...<a :href="item.resurl" v-if="item.resurl"> Resource</a> </span><br>
      <span><b>included:</b> {{ item.rutcount }} </span>
    </div>
    <div class="operate">
      <el-dropdown>
        <el-button type="primary" size="mini" plain>{{flagAction}}<i class="el-icon-arrow-down el-icon--right"></i></el-button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item><span @click="flagSchedule">Schedule</span></el-dropdown-item>
          <el-dropdown-item><span @click="flagWorking">Working On</span></el-dropdown-item>
          <el-dropdown-item><span @click="flagDone">Have Done</span></el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { flagItem, checkFlag } from '@/api/api'

export default {
  name: 'item-sum',
  props: ['item'],
  data () {
    return {
      flagAction: this.checkFlaging() || 'Flag it'
    }
  },
  computed: {
    cover () {
      return this.item.cover
    }
  },
  methods: {
    checkAuth () {
      let localToken = localStorage.token
      // let localID = localStorage.userid
      if (localToken) {
        this.$axios.defaults.auth = {
          username: localToken,
          password: localToken
        }
        return true
      } else {
        return false
      }
    },
    checkFlaging () {
      if (this.checkAuth()) {
        let itemid = this.item.id || this.$route.params.id // why?? liftcycle timing??
        return checkFlag(itemid)
        .then(resp => {
          this.flagAction = resp.data
        })
      } else {
        this.flagAction = 'Flag it'
      }
    },
    flagSchedule () {
      if (this.checkAuth()) {
        return flagItem('todo', this.item.id)
        .then(() => {
          this.flagAction = 'Scheduled'
        })
      } else {
        this.$message({
          showClose: true,
          message: 'Should Log in to Access'
        })
        this.$router.push('/login')
      }
    },
    flagWorking () {
      if (this.checkAuth()) {
        return flagItem('doing', this.item.id)
        .then(() => {
          this.flagAction = 'Working On'
        })
      } else {
        this.$message({
          showClose: true,
          message: 'Should Log in to Access'
        })
        this.$router.push('/login')
      }
    },
    flagDone () {
      if (this.checkAuth()) {
        return flagItem('done', this.item.id)
        .then(() => {
          this.flagAction = 'Have Done'
        })
      } else {
        this.$message({
          showClose: true,
          message: 'Should Log in to Access'
        })
        this.$router.push('/login')
      }
    }
  // },
  // beforeUpdate () {
  //   this.checkFlaging()
  }
}
</script>

<style lang="stylus" scoped>
.itemsum
  background-color #fff
  min-height 180px
  padding 10px 110px 10px 135px
  border-bottom 1px solid #eee
  position relative
  .thumb
    width 120px
    height 160px
    position absolute
    top 10px
    left 2px
  .info
    font-size 0.9em
    .title
      font-size 1.2em
      font-weight 700
      a
        &:hover
          color lightblue
  .operate
    position absolute
    top 10px
    right 2px
li
  list-style-type none
</style>
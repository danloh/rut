<template>
  <div class="demand-page">
    <div class="demand-main">
      <div>
        <el-form :model="demandForm" :rules="rules" ref="demandForm">
          <el-form-item prop="demand">
            <el-input v-model="demandForm.demand" placeholder="Request something, Support #hashtag"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button size="mini" @click="submitDemand('demandForm', demandForm)">Submit</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="submenu">
        <router-link to="/demand/popular">Popular</router-link>
        <router-link to="/demand/new">New</router-link>
      </div>
      <div class="demand-view">
        <router-view></router-view>
      </div>
    </div>
    <div class="demand-side">
    </div>
  </div>
</template>

<script>
import DemandList from '@/components/Demand/DemandList.vue'
// import { mapGetters } from 'vuex'

export default {
  name: 'demands',
  title: 'Request',
  components: { DemandList },
  data () {
    return {
      demandForm: {
        demand: ''
      },
      rules: {
        demand: [{ required: true, message: 'Required', trigger: 'blur' }]
      },
      items: null,
      dueDate: ''
    }
  },
  computed: {
  },
  methods: {
    submitDemand (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = { demand: form.demand }
          this.$store.dispatch('postDemand', data)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
.demand-page
  padding 10px 200px 10px 0px
  position relative
  .demand-main
    padding auto
    .submenu
      margin-bottom 5px
      a
        color grey
        margin-right 0.85em
        &:hover
          color darkgreen
        &.router-link-active
          color orange
          font-weight 800
  .demand-side
    position absolute
    top 10px
    right 0
    width 180px
    background-color #e5ebe4
    padding 5px
    .right-title
      padding 2px 5px
    .right-item
      padding 2px 5px
      font-size 0.8em
      background-color white
</style>
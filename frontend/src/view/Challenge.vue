<template>
  <div class="challenge-page">
    <div class="challenge-view">
      <div>
        <el-form :model="clipForm" :rules="rules" ref="clipForm">
          <el-form-item prop="clip" style="margin-bottom:8px">
            <el-input type="textarea" v-model="clipForm.clip" placeholder="excerpt something"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button size="mini" @click="submitClip('clipForm', clipForm)">Submit</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="submenu">
        <router-link to="/challenge/allclip">All Clips</router-link>
        <router-link to="/challenge/myclip">My Clips</router-link>
      </div>
      <div class="clip-view">
        <router-view></router-view>
      </div>
    </div>
    <div class="challenge-side" v-if="challengeRut">
      <div class="right-title">
        <b>Working on Challenge:</b>
        <br>
        <router-link :to="'/readuplist/' + challengeRut.id"> {{ challengeRut.title }}</router-link>
        <br>
        <span>Due Date: {{dueDate}} <el-button type="text">..Set</el-button></span>
      </div>
      <b> Including Items:</b>
      <p class="right-item" v-for="item in items" :key="item.id" :item="item">
        ~{{item.cate}} <router-link :to="'/item/' + item.id" :title="item.title"> {{ item.title.slice(0, 60) }}...</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import ClipList from '@/components/Challenge/ClipList.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'challenge',
  title: 'Challenge To Reading Anything',
  components: { ClipList },
  data () {
    return {
      clipForm: {
        clip: ''
      },
      rules: {
        clip: [{ required: true, message: 'Required', trigger: 'blur' }]
      },
      items: null,
      dueDate: ''
    }
  },
  computed: {
    ...mapGetters([
      'allRuts'
    ]),
    challengeRut () {
      return this.allRuts[0]
    }
  },
  methods: {
    submitClip (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = { clip: form.clip }
          this.$store.dispatch('postClip', data)
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  },
  mounted () {
    this.$store.dispatch('getChallengeRut')
    .then(resp => {
      this.items = resp.data.items
      this.dueDate = resp.data.deadline
    })
  }
}
</script>

<style lang="stylus" scoped>
.challenge-page
  padding 10px 280px 10px 0px
  position relative
  .challenge-view
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
  .challenge-side
    position absolute
    top 10px
    right 0
    width 270px
    background-color #f0f3f0
    padding 5px
    .right-title
      padding 0px 5px
    .right-item
      padding 0px 5px
      font-size 0.85em
      background-color white
</style>
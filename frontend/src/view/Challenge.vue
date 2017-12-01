<template>
  <div class="challenge-page">
    <div class="challenge-view">
      <div>
        <el-form :model="clipForm" :rules="rules" ref="clipForm">
          <el-form-item prop="clip">
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
        <h4><b>Working on Challenge:</b></h4>
        <router-link :to="'/readuplist/' + challengeRut.id"> {{ challengeRut.title }}</router-link>
        <p>Due Date: {{dueDate}} <el-button type="text">..Set</el-button></p>
      </div>
      <b>including:</b>
      <p class="right-item" v-for="item in items" :key="item.id" :item="item">
        ~{{item.cate}} <router-link :to="'/item/' + item.id"> {{ item.title }}</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import ClipList from '../components/ClipList.vue'
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
    let param = {'ref': 'working'}
    this.$store.dispatch('getChallengeRuts', param)
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
      padding 2px 5px
    .right-item
      padding 2px 5px
      font-size 0.8em
      background-color white
</style>
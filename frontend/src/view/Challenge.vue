<template>
  <div class="challenge-page">
    <div class="challenge-view">
      <div>
        <el-form :model="clipForm" :rules="rules" ref="clipForm">
          <el-form-item prop="clip" style="margin-bottom:16px">
            <el-input type="textarea" v-model="clipForm.clip" placeholder="excerpt something"></el-input>
          </el-form-item>
          <el-form-item prop="doing" style="margin-bottom:8px">
            <el-select class="selectItem" v-model="clipForm.doingItemID" placeholder="Pick an item from which you excerpt clip in Your working-ons">
              <el-option v-for="i in doingItems" :key="i.id" :label="i.title" :value="i.id"></el-option>
            </el-select>
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
        <b>Due Date: {{dueDate}} <el-button type="text">..Set</el-button></b>
        <br>
        <b>Including Items:</b>
      </div>
      <p class="right-item" v-for="(item, index) in items" :key="index" :item="item">
        ~{{item.cate}} <router-link :to="'/item/' + item.id" :title="item.title"> {{ item.title.slice(0, 60) }}...</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import ClipList from '@/components/Challenge/ClipList.vue'
import { fetchChallengeItems } from '@/api/api'
import { mapGetters } from 'vuex'

export default {
  name: 'challenge',
  title: 'Readup.Tips - Challenge To Reading Anything',
  components: { ClipList },
  data () {
    return {
      clipForm: {
        clip: '',
        doingItemID: null
      },
      rules: {
        clip: [{ required: true, message: 'Required', trigger: 'blur' }],
        doingItemID: [{ required: true, message: 'Required', trigger: 'change' }]
      },
      items: null,
      dueDate: '',
      doingItems: []
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
        if (valid && form.doingItemID !== null) {
          let data = { clip: form.clip, itemid: form.doingItemID }
          this.$store.dispatch('postClip', data)
          this.resetForm(formName)
        } else {
          console.log('error submit!!')
          this.$message({
            showClose: true,
            message: 'Something Wrong, Please check input'
          })
          return false
        }
      })
    },
    getChallengeItems () {
      return fetchChallengeItems()
      .then(resp => {
        this.doingItems = resp.data
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  },
  mounted () {
    this.$store.dispatch('getChallengeRut')
    .then(resp => {
      this.items = resp.data.items
      this.dueDate = resp.data.deadline
    })
    this.getChallengeItems()
  }
}
</script>

<style lang="stylus" scoped>
.challenge-page
  padding 10px 285px 10px 0px
  position relative
  .challenge-view
    padding auto
    .selectItem
      width 100%
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
      b
        font-size 0.85em
    .right-item
      padding 0 0 0 10px
      font-size 0.85em
      background-color white
</style>
<template>
  <div class="tagpage">
    <div class="tagside">
      <h4 class="sidetitle">Related Tags</h4>
      <div class="sidebody" v-for="(tag, index) in showTags" :key="index">
        <router-link :to="'/tag/' + tag.tagid">{{tag.tagname}}</router-link>
      </div>
    </div>
    <div class="tagmeta">
      <h4><b>{{ tagDetail.tagname}}</b></h4>
      <div>{{ tagDetail.descript}} 
        <el-button type="text" @click="openDialog = true">...Edit</el-button>
      </div>
      <el-button class="fbtn" type="success" size="mini" plain @click="favTag">{{action}} {{favCount}}</el-button>
    </div>
    <div class="rutlist">
      <rut-list :rutlist="currentRuts" @loadmore="loadmoreRuts"></rut-list>
    </div>
    <!-- dialog -->
    <el-dialog title="Edit Tag Description" :visible.sync="openDialog">
      <el-form :model="tagForm" :rules="rules" ref="tagForm" size="mini">
        <el-form-item label="Tag Name" prop="name">
          <el-input v-model="tagForm.name"></el-input>
        </el-form-item>
        <el-form-item label="Parent Tag" prop="parent">
          <el-input v-model="tagForm.parent"></el-input>
        </el-form-item>
        <el-form-item label="Description" prop="description">
          <el-input type="textarea" v-model="tagForm.description"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="openDialog = false">Cancel</el-button>
        <el-button type="success" @click="editTag('tagForm', tagForm)">Submit</el-button>
      </div>
    </el-dialog>
    <!-- dialog end -->
  </div>
</template>

<script>
import RutList from '@/components/Rut/RutList.vue'
import { mapGetters } from 'vuex'
import { editTag, checkFav, favTag, fetchTagRuts } from '@/api/api'
import { checkAuth } from '@/util/auth'

export default {
  name: 'tag-view',
  components: {
    RutList
  },
  data () {
    return {
      action: this.checkFavor(), // || 'Follow',
      favCount: 0,
      openDialog: false,
      tagForm: {
        name: '',
        parent: '',
        description: ''
      },
      rules: {
        name: [
          { required: true, message: 'Please give a tag name', trigger: 'blur' }
        ],
        description: [
          { required: true, message: 'Descript it', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters([
      'allRuts',
      'totalRuts',
      'currentPage',
      'currentRuts',
      'maxPage',
      'perPage',
      'showTags',
      'tagDetail'
    ])
  },
  tagid () {
    return this.tagDetail.id
  },
  title () {
    return this.tagDetail.tagname
  },
  methods: {
    loadmoreRuts () {
      fetchTagRuts(this.tagDetail.id, {'page': this.currentPage})
      .then(resp => {
        this.$store.commit('MORE_RUTS', resp.data)
      })
    },
    loadData () {
      let tagid = this.$route.params.id
      this.$store.dispatch('getTag', tagid)
      .then(resp => {
        this.tagForm.name = resp.data.tagname
        this.tagForm.description = resp.data.descript
        this.favCount = resp.data.favcount
        this.action = this.checkFavor() // || 'Follow'
      })
    },
    editTag (formName, form) {
      this.$refs[formName].validate((valid) => {
        if (valid && checkAuth()) {
          let data = {
            name: form.name,
            parent: form.parent,
            description: form.description
          }
          let tagid = this.tagDetail.id
          editTag(tagid, data)
          .then((resp) => {
            this.openDialog = false
            this.loadData()  // can be less consumption
            this.$message({
              showClose: true,
              message: resp.data,
              type: 'success'
            })
          }).catch(error => {
            this.$message({
              showClose: true,
              message: error.response.statusText
            })
          })
        } else if (!checkAuth()) {
          this.$message({
            showClose: true,
            message: 'Should Log in to Continue'
          })
          this.$router.push({
            path: '/login',
            query: {redirect: this.$route.fullPath}
          })
        }
      })
    },
    checkFavor () {
      if (checkAuth()) {
        let tagid = this.$route.params.id
        return checkFav(tagid)
        .then(resp => {
          this.action = resp.data
        })
      } else {
        return 'Follow' // work incorrectly when non-login if no return
      }
    },
    favTag () {
      if (checkAuth()) {
        let tagid = this.$route.params.id
        if (this.action === 'Follow') {
          return favTag('fav', tagid)
          .then(() => {
            this.action = 'UnFollow'
            this.favCount += 1
          })
        } else {
          return favTag('unfav', tagid)
          .then(() => {
            this.action = 'Follow'
            this.favCount -= 1
          })
        }
      } else {
        this.$message({
          showClose: true,
          message: 'Should Log in to Continue'
        })
        this.$router.push({
          path: '/login',
          query: {redirect: this.$route.fullPath}
        })
      }
    }
  },
  watch: {
    '$route': 'loadData' // watch to render re-used component
  },
  created () {
    this.loadData()
  }
}
</script>

<style lang="stylus" scoped>
.tagpage
  padding 10px 230px 10px 0px
  position relative
  .tagside
    position absolute
    right 0
    width 220px
    background-color white
    .sidetitle
      background-color #e5ebe4
      padding 5px 10px
    .sidebody
      padding 5px 10px
      a
        &:hover
          color #ff6600
  .tagmeta
    background-color white
    min-height: 40px
    padding 5px 10px
    margin-bottom 5px
    position relative
    .fbtn
      position absolute
      top 10px
      right 5px
  .rutlist
    padding auto
</style>

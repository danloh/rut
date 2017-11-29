<template>
  <div class="tagpage" :key="tagDetail.id">
    <div class="tagside">
      <h4 class="lefttitle">Related Tags</h4>
      <div class="leftbody" v-for="tag in showTags" :key="tag.tagid">
        <router-link :to="'/tag/' + tag.tagid">{{tag.tagname}}</router-link>
      </div>
    </div>
    <div class="tagmeta">
      <h4><b>{{ tagDetail.tagname}}</b></h4>
      <p>{{ tagDetail.descript}} <el-button type="text">...Edit Description</el-button></p>
      <el-button type="success" size="mini" plain>{{action}} {{tagDetail.favcount}}</el-button>
    </div>
    <div class="rutlist">
      <rut-list :rutlist="currentRuts" @loadmore="loadmoreRuts"></rut-list>
    </div>
  </div>
</template>

<script>
import RutList from '../components/RutList.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'tag-view',
  components: {
    RutList
  },
  data () {
    return {
      action: 'Follow'
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
  methods: {
    loadmoreRuts () {
      this.$store.commit('ADD_RUTS', this.currentPage)
    },
    loadNew (id) { // try to reload, fail
      this.$store.dispatch('getTag', id)
    }
  },
  watch: { // try to reload, fail
    currentTagid () {
      let tagid = this.$route.params.id
      this.$store.dispatch('getTag', tagid)
    }
  },
  mounted () {
    let tagid = this.$route.params.id
    this.$store.dispatch('getTag', tagid)
  }
}
</script>

<style lang="stylus" scoped>
.tagpage
  padding-left 230px
  position relative
  .tagside
    position absolute
    left 0
    width 220px
    background-color white
    .lefttitle
      background-color #e5ebe4
      padding 5px 10px
    .leftbody
      padding 5px 10px
  .tagmeta
    background-color white
    min-height: 40px
    padding 5px
  .rutlist
    padding auto
</style>

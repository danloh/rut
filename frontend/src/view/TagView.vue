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
      <el-button class="fbtn" type="success" size="mini" plain>{{action}} {{tagDetail.favcount}}</el-button>
    </div>
    <div class="rutlist">
      <rut-list :rutlist="currentRuts" @loadmore="loadmoreRuts"></rut-list>
    </div>
  </div>
</template>

<script>
import RutList from '@/components/Rut/RutList.vue'
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
  title () {
    return this.tagDetail.tagname
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
  padding 10px 230px 10px 0px
  position relative
  .tagside
    position absolute
    right 0
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

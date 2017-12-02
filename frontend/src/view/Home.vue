<template>
  <div class="homepage">
    <div class="rutlist">
      <rut-list :rutlist="currentRuts" @loadmore="loadmoreRuts"></rut-list>
    </div>
    <div class="homeside">
      <h4 class="righttitle">Top Topics</h4>
      <div class="rightbody" v-for="tag in showTags" :key="tag.tagid">
        <router-link :to="'/tag/' + tag.tagid">{{tag.tagname}}</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import RutList from '../components/RutList.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'home',
  title: 'Home',
  components: {
    RutList
  },
  computed: {
    ...mapGetters([
      'allRuts',
      'totalRuts',
      'currentPage',
      'currentRuts',
      'maxPage',
      'perPage',
      'showTags'
    ]),
    nextPage () {
      return {
        page: this.currentPage + 1
      }
    }
  },
  methods: {
    loadmoreRuts () {
      this.$store.commit('ADD_RUTS', this.currentPage)
    }
  },
  mounted () {
    this.$store.dispatch('getRuts')
  }
}
</script>

<style lang="stylus" scoped>
.homepage
  padding 10px 230px 10px 0px
  position relative
  .rutlist
    padding auto
  .homeside
    position absolute
    top 10px
    right 0
    width 220px
    background-color white
    .righttitle
      background-color #e5ebe4
      padding 10px 15px
    .rightbody
      padding 5px 20px
</style>

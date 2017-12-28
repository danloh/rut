<template>
  <div class="home-page">
    <spinner :show="loading"></spinner>
    <div class="rut-list">
      <keep-alive>
        <rut-list :rutlist="currentRuts" @loadmore="loadmoreRuts"></rut-list>
      </keep-alive>
    </div>
    <div class="home-side">
      <h4 class="right-title">Top Topics</h4>
      <div class="right-body" v-for="(tag, index) in showTags" :key="index">
        <router-link :to="'/tag/' + tag.tagid">{{tag.tagname}}</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Spinner from '@/components/Misc/Spinner.vue'
import RutList from '@/components/Rut/RutList.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'home',
  title: 'Readup.Tips - Share Reading List',
  components: { RutList, Spinner },
  data: () => ({
    loading: true
  }),
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
    this.loading = true
    this.$store.dispatch('getRuts')
    .then(() => {
      this.loading = false
    })
  }
}
</script>

<style lang="stylus" scoped>
.home-page
  padding 10px 230px 10px 0px
  position relative
  .rut-list
    padding auto
  .home-side
    position absolute
    top 10px
    right 0
    width 220px
    background-color white
    .right-title
      background-color #e5ebe4
      padding 10px 15px
    .right-body
      padding 5px 20px
      a
        &:hover
          color #ff6600
</style>

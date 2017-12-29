<template>
  <div class="item-page">
    <div class="item-main">
      <item-sum :item="currentItem" :key="currentItem.id"></item-sum> <!--key to re-render-->
      <div>
        <b>More Details</b> &nbsp;&nbsp;&nbsp;
        <router-link class="editlink" :to="'/edit/item/' + currentItem.id">...Edit Detail</router-link>
      </div>
      <div class="item-detail">
        <div v-html="currentItem.details">...</div>
      </div>
      <div class="submenu">
        <b>>></b>&nbsp;&nbsp;<router-link :to="'/item/' + currentItem.id + '/hotreview'">Hot Reviews</router-link>
        <router-link :to="'/item/' + currentItem.id + '/newreview'">Latest Reviews</router-link> &nbsp;&nbsp;&nbsp;
        <router-link class="editlink" style="color: #337ab7" :to="'/review/item/' + currentItem.id">...Post Review</router-link>
      </div>
      <div class="review-view">
        <router-view></router-view>
      </div>
      <div class="clips">
        <b>>></b>&nbsp;&nbsp;<b style="color: orange">Clips</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <router-link class="editlink" to="/challenge">...Excerpt Quote</router-link>
        <clip-list :param="cliplistParam"></clip-list>
      </div>
    </div>
    <div class="item-side">
      <div class="include">
        <b class="in-title">Included in {{currentItem.rutcount}} Tips</b>
        <p class="in-item" v-for="(rut, index) in inRuts" :key="index" :rut="rut">
          - <router-link :to="'/readuplist/' + rut.id" :title="rut.title"> {{ rut.title.slice(0, 60) }}...</router-link>
        </p>
        <div v-if="hasMoreRut">
          <el-button size="mini" class="blockbtn" @click="loadmoreRuts" :disabled="!hasMoreRut">Show More</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ItemSum from '@/components/Item/ItemSum.vue'
import ClipList from '@/components/Challenge/ClipList.vue'
import { fetchInRuts } from '@/api/api'
import { mapGetters } from 'vuex'

export default {
  name: 'item-view',
  title () {
    return this.currentItem.title
  },
  components: { ItemSum, ClipList },
  data () {
    return {
      cliplistParam: {},
      currentPage: 1
    }
  },
  computed: {
    ...mapGetters([
      'currentItem',
      'inRuts'
    ]),
    hasMoreRut () {
      return this.inRuts.length < this.currentItem.rutcount
    }
  },
  methods: {
    loadmoreRuts () {
      let itemid = this.$route.params.id
      let params = {'page': this.currentPage}
      fetchInRuts(itemid, params)
      .then(resp => {
        this.$store.commit('MORE_INRUTS', resp.data)
        this.currentPage += 1
      })
    }
  },
  beforeMount () {
    let itemid = this.$route.params.id
    this.cliplistParam = {'itemid': itemid}
    this.$store.dispatch('getItem', itemid)
  }
}
</script>

<style lang="stylus" scoped>
.item-page
  padding 10px 255px 10px 0px
  position relative
  .item-main
    padding auto
    .item-detail
      background-color white
      padding 5px
    .clips
      margin 5px 0
      padding 5px
    .review-view
      padding 5px
    .submenu
        margin 5px 0
        padding 5px
        a
          color grey
          margin-right 0.85em
          &:hover
            color darkgreen
          &.router-link-active
            color orange
            font-weight 800
  .editlink
    font-size 0.75em
    font-weight 600
  .item-side
    position absolute
    top 10px
    right 0
    width 245px
    .include
      margin-top 0px
      padding 5px
      background-color #f0f3f0
      .in-title
        padding 2px 5px
        color green
      .in-item
        padding 2px 5px
        font-size 0.85em
        background-color white
        a
          &:hover
            color #ff6600
</style>

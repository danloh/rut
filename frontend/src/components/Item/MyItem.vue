<template>
  <div class="item-page">
    <div class="item-main">
      <div class="submenu">
        <b>>></b>&nbsp;&nbsp;<b style="color: orange">Reviews</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <router-link class="editlink" :to="'/review/item/' + currentItem.id">...Post Review</router-link>
      </div>
      <review-list :param="reviewsParam"></review-list>
      <div class="submenu">
        <b>>></b>&nbsp;&nbsp;<b style="color: orange">Clips</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <router-link class="editlink" to="/challenge">...Excerpt Quote</router-link>
      </div>
      <clip-list :param="cliplistParam"></clip-list>
    </div>
  </div>
</template>

<script>
import ItemSum from '@/components/Item/ItemSum.vue'
import ReviewList from '@/components/Item/ReviewList.vue'
import ClipList from '@/components/Challenge/ClipList.vue'
import { fetchInRuts } from '@/api/api'
import marked from '@/util/marked'
import { mapGetters } from 'vuex'

export default {
  name: 'my-item-view',
  components: { ClipList, ReviewList },
  props: ['itemid'],
  data () {
    return {
      cliplistParam: {},
      reviewsParam: {}
    }
  },
  computed: {
    cliplistParam () {
      return {'itemid': this.itemid}
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
    this.reviewsParam = {'itemid': itemid, 'ref': 'hot'}
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
      background-color lighten(#f0f3f0, 45%)
      padding 5px
    .submenu
        margin 5px 0
        padding 5px
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
        background-color lighten(#f0f3f0, 45%)
        a
          &:hover
            color #ff6600
</style>

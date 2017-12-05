<template>
  <div class="item-page">
    <div class="item-main">
      <item-sum :item="currentItem"></item-sum>
      <div><b>More Details</b> &nbsp;&nbsp;&nbsp;<el-button type="text">...Add More</el-button></div>
      <div class="item-detail">
        <div v-html="currentItem.details">...</div>
      </div>
      <div class="submenu">
        <router-link :to="'/item/' + currentItem.id + '/hotreview'">Hot</router-link>
        <router-link :to="'/item/' + currentItem.id + '/newreview'">New</router-link>
        &nbsp;&nbsp;&nbsp;
        <el-button type="text">...Post a Review</el-button>
      </div>
      <div class="review-view">
        <router-view></router-view>
      </div>
    </div>
    <div class="item-side">
      <div class="include">
        <b class="in-title">Included in {{currentItem.rutcount}} Tips</b>
        <p class="in-item" v-for="rut in inRuts" :key="rut.id" :rut="rut">
          ~ <router-link :to="'/readuplist/' + rut.id" :title="rut.title"> {{ rut.title.slice(0, 60) }}...</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import ItemSum from '@/components/Item/ItemSum.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'item-view',
  title () {
    return this.currentItem.title
  },
  components: { ItemSum },
  computed: {
    ...mapGetters([
      'currentItem',
      'inRuts'
    ])
  },
  beforeMount () {
    let itemid = this.$route.params.id
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
</style>


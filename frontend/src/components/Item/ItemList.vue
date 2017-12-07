<template>
  <div>
    <div class="item-list">
      <item-sum v-for="item in items" :key="item.id" :item="item"></item-sum>
    </div>
    <div>
      <el-button class="blockbtn" @click="$emit('loadmore')" :disabled="!hasMore">More</el-button>
    </div>
    <br>
  </div>
</template>

<script>
import ItemSum from './ItemSum.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'item-list',
  props: ['items'],
  components: { ItemSum },
  computed: {
    ...mapGetters([
      'currentR',
      'maxR'
    ]),
    hasMore () {
      return this.currentR < this.maxR
    }
  }
}
</script>

<style lang="stylus">
.item-list
  width 100%
  li
    list-style-type none
</style>
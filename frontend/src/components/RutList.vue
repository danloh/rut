<template>
  <div>
    <div class="rut-list">
      <rut-sum v-for="rut in rutlist" :key="rut.id" :rut="rut"></rut-sum>
    </div>
    <div>
      <el-button @click="$emit('loadmore')" :disabled="!hasMore">More</el-button>
    </div>
    <br>
  </div>
</template>

<script>
import RutSum from './RutSum.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'rut-list',
  props: ['rutlist'],
  components: { RutSum },
  computed: {
    ...mapGetters([
      'currentPage',
      'maxPage',
      'perPage'
    ]),
    hasMore () {
      return this.currentPage < this.maxPage
    }
  }
}
</script>

<style lang="stylus">
.rut-list
  margin 10px 0
  width 100%
  li
    list-style-type none
</style>
<template>
  <div>
    <div class="rut-list">
      <rut-sum v-for="rut in rutlist" :key="rut.id" :rut="rut"></rut-sum>
    </div>
    <div>
      <button @click="$emit('loadmore')" :disabled="!hasMore">More</button>
    </div>
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
      'perPage',
      'rutdetail'
    ]),
    hasMore () {
      return this.currentPage < this.maxPage
    }
  }
}
</script>

<style lang="stylus">
.rut-list
  position absolute
  margin 30px 0
  width 100%
  ul
    padding 0
    margin 0
@media (max-width 600px)
  .news-list
    margin 10px 0

</style>
<template>
  <div class="demand-list">
    <demand v-for="demand in currentDemands" :key="demand.id" :demand="demand"></demand>
    <div>
      <el-button class="blockbtn" @click="loadmoreDemand" :disabled="!hasMore">More</el-button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Demand from './Demand.vue'

export default {
  name: 'demand-list',
  components: { Demand },
  props: {
    type: String,
    default: 'popular'  // popular or new, may can be deleted
  },
  computed: {
    ...mapGetters([
      'allDemands',
      'totalDemands',
      'currentD',
      'currentDemands',
      'maxD',
      'perD'
    ]),
    hasMore () {
      return this.currentD < this.maxD
    }
  },
  methods: {
    loadmoreDemand () {
      this.$store.commit('ADD_DEMANDS', this.currentD)
    }
  },
  mounted () {
    this.$store.dispatch('getDemands', {'type': this.type})
  }
}
</script>

<style lang="stylus" scoped>
.demand-list
  padding auto
</style>
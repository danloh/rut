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
    userid: null
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
      let params = {'type': this.type, 'userid': this.userid, 'page': this.currentD}
      this.$store.dispatch('moreDemands', params)
    }
  },
  mounted () {
    this.$store.dispatch('getDemands', {'type': this.type, 'userid': this.userid})
  }
}
</script>

<style lang="stylus" scoped>
.demand-list
  padding auto
</style>
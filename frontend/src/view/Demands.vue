<template>
  <div class="list-view">
    <template v-for="demand in demands">
      {{demand.creator}}
      {{demand.body}}
      {{demand.vote}}
    </template>
  </div>
</template>

<script>
import { getDemands } from '../api/api'

export default {
  name: 'demands',

  data () {
    return {
      demands: [],
      total: 0,
      getprev: null,
      getmore: null,
      page: 0
    }
  },

  methods: {
    fetchDemands () {
      let param = {}
      getDemands(param).then((resp) => {
        this.demands = this.demands.concat(resp.data.demands)
        this.total += resp.data.total
        this.getprev = resp.data.prev
        this.getmore = resp.data.more
        this.page += 1
      })
    }
  },

  mounted () {
    this.fetchDemands()
  }
}
</script>

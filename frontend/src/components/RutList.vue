<template>
  <div class="list-view">
    <div class="rut-list">
      <rut-sum v-for="rut in ruts" :key="rut.id" :rut="rut"></rut-sum>
    </div>
    <div class="news-list-nav">
      <button v-if="getmore" @click="fetchRuts">more</button>
      <a v-else class="disabled">more</a>
    </div>
  </div>
</template>

<script>
import { getRuts } from '../api/api'
import RutSum from './RutSum.vue'

export default {
  name: 'rut-list',

  components: { RutSum },

  data () {
    return {
      ruts: [],
      total: 0,
      getprev: null,
      getmore: null,
      page: 0
    }
  },

  methods: {
    fetchRuts () {
      let usr = this.$store.state.user
      let param = { userid: usr ? usr.id : '', page: this.page + 1 }
      getRuts(param).then((resp) => {
        this.ruts = this.ruts.concat(resp.data.ruts)
        this.total += resp.data.total
        this.getprev = resp.data.prev
        this.getmore = resp.data.more
        this.page += 1
      })
    }
  },

  mounted () {
    this.fetchRuts()
  }
}
</script>

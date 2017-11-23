<template>
  <div>
    <rut-list :rutlist="rutlist" @loadmore="loadmoreRuts"></rut-list>
  </div>
</template>

<script>

import RutList from '../components/RutList.vue'

export default {
  name: 'home',
  components: {
    RutList
  },
  computed: {
    rutz () {
      return this.$store.state.rut.rutz
    },
    rutlist () {
      return this.rutz.list
    },
    nextPageParams () {
      return {
        page: this.rutz.page + 1
      }
    }
  },
  methods: {
    loadmoreRuts () {
      this.$store.dispatch('getRuts', this.nextPageParams)
    }
  },
  mounted () {
    this.$store.dispatch('getRuts')
  }
}
</script>

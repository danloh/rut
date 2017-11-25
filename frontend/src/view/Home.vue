<template>
  <div>
    <rut-list :rutlist="currentRuts" @loadmore="loadmoreRuts"></rut-list>
  </div>
</template>

<script>
import RutList from '../components/RutList.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'home',
  components: {
    RutList
  },
  computed: {
    ...mapGetters([
      'allRuts',
      'totalRuts',
      'currentPage',
      'currentRuts',
      'maxPage',
      'perPage',
      'rutdetail'
    ]),
    nextPage () {
      return {
        page: this.currentPage + 1
      }
    }
  },
  methods: {
    loadmoreRuts () {
      this.$store.commit('ADD_RUTS', this.currentPage)
    }
  },
  mounted () {
    this.$store.dispatch('getRuts')
  }
}
</script>

<template>
  <div class="list-view">
    <b>{{flag.toUpperCase()}} {{totalItems}}</b>
    <div class="item-list">
      <item-list :items="currentItems" @loadmore="loadmoreItems"></item-list>
    </div>
  </div>
</template>

<script>
import ItemList from '@/components/Item/ItemList.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'profile-items',
  props: {
    flag: String // tobe: doing, todo, done
  },
  components: { ItemList },
  computed: {
    ...mapGetters([
      'allItems',
      'totalItems',
      'currentR',
      'currentItems',
      'maxR'
    ])
  },
  methods: {
    loadmoreItems () {
      this.$store.commit('ADD_ITEMS', this.currentR)
    }
  },
  mounted () {
    let flag = this.flag
    let userid = this.$route.params.id
    let params = {'flag': flag, 'userid': userid}
    this.$store.dispatch('getItems', params)
  }
}
</script>

<style lang="stylus" scoped>
.item-list
  width 100%
  margin-top 5px
  li
    list-style-type none
</style>
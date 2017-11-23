<template>
  <div class="list-view">
    <div class="clip-list">
      <clip v-for="clip in cliplist" :key="clip.id" :clip="clip"></clip>
    </div>
    <div>
      <button @click="loadmoreClip" :disabled="!hasMore">More</button>
    </div>
  </div>
</template>

<script>
import Clip from '../components/Clip.vue'

export default {
  name: 'clip-list',
  props: {
    param: Object
  },
  components: { Clip },
  computed: {
    clipz () {
      return this.$store.state.clipz
    },
    cliplist () {
      return this.clipz.list
    },
    nextPageParams () {
      return {
        page: this.clipz.page + 1
      }
    },
    hasMore () {
      return this.cliplist.more !== null
    }
  },
  methods: {
    loadmoreClip () {
      this.$store.dispatch('getClip', Object.assign(this.param, this.nextPageParams))
    }
  },
  beforeMount () {
    this.$store.dispatch('getClip', this.param)
  }
}
</script>

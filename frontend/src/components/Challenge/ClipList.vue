<template>
  <div class="list-view">
    <div class="clip-list">
      <!--Here if :key=index,will run into problem when render, reuse component, also in DemandList-->
      <clip v-for="clip in currentClips" :key="clip.id" :clip="clip"></clip>
    </div>
    <div v-if="hasMore">
      <el-button class="blockbtn" size="mini" @click="loadmoreClip" :disabled="!hasMore">Show More</el-button>
    </div>
  </div>
</template>

<script>
import Clip from './Clip.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'clip-list',
  props: {
    param: Object
  },
  components: { Clip },
  computed: {
    ...mapGetters([
      'totalClips',
      'currentP',
      'currentClips',
      'maxP',
      'perP'
    ]),
    hasMore () {
      return this.currentP < this.maxP
    }
  },
  methods: {
    loadmoreClip () {
      let page = { 'page': this.currentP }
      let params = Object.assign(page, this.param)
      this.$store.dispatch('moreClips', params)
    }
  },
  mounted () {
    this.$store.dispatch('getClips', this.param)
  }
}
</script>

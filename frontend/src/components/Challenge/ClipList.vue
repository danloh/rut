<template>
  <div class="cliplist">
    <div class="clip-list">
      <clip v-for="(clip, index) in currentClips" :key="index" :clip="clip"></clip>
    </div>
    <div v-if="hasMore">
      <el-button class="blockbtn" @click="loadmoreClip" :disabled="!hasMore">More</el-button>
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
      'allClips',
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
      this.$store.commit('ADD_CLIPS', this.currentP)
    }
  },
  mounted () {
    this.$store.dispatch('getClips', this.param)
  }
}
</script>

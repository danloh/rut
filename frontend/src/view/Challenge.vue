<template>
  <div class="list-view">
    <div class="clip-list">
      <clip v-for="clip in clips" :key="clip.id" :clip="clip"></clip>
    </div>
  </div>
</template>

<script>
import { getClips } from '../api/api'
import Clip from '../components/Clip.vue'

export default {
  name: 'challenge',
  components: { Clip },

  data () {
    return {
      clips: [],
      total: 0,
      getprev: null,
      getmore: null,
      page: 0
    }
  },

  methods: {
    fetchClips () {
      let param = {}
      getClips(param).then((resp) => {
        this.clips = this.clips.concat(resp.data.clips)
        this.total += resp.data.total
        this.getprev = resp.data.prev
        this.getmore = resp.data.more
        this.page += 1
      })
    }
  },

  mounted () {
    this.fetchClips()
  }
}
</script>

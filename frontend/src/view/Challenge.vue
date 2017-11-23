// to do  nested route-view
<template>
  <div class="list-view">
    <router-link to="/challenge/allclip">All Clips</router-link>
    <div class="clip-list">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import ClipList from '../components/ClipList.vue'

export default {
  name: 'challenge',
  components: { ClipList },
  computed: {
  }
}
</script>

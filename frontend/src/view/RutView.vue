<template>
  <div class="rut-view" v-if="rut">
    <template v-if="rut">
      <div class="item-view-header">
        <h1>{{ rut.title }}</h1>
        <p class="meta">
          Created by <router-link :to="'/user/' + rut.by">{{ rut.by }}</router-link>
          | {{ rut.time | timeAgo }} ago
          | including {{ rut.itemcount }} items
        </p>
      </div>
      <div>
        {{rut.intro}}
      </div>
      <template v-for="tip in tips">
        <item-sum v-if="tip.item" :item="tip.item" :key="tip.order"></item-sum>
        {{tip.tip}}
      </template>
      <div>
        {{rut.epilog}}
      </div>
      <div>
        <router-link :to="'/rut/comment' + rut.id">Comment</router-link>
      </div>
    </template>
  </div>
</template>

<script>
import { getRut } from '../api/api'
import Spinner from '../components/Spinner.vue'
import ItemSum from '../components/ItemSum.vue'
import Comment from '../components/Comment.vue'

export default {
  name: 'rut-view',
  components: { ItemSum, Spinner, Comment },

  data: () => ({
    rut: null
  }),

  computed: {
    tips () {
      let r = this.rut
      return r ? r.tips : null
    }
  },

  // Fetch rut when mounted on the client
  mounted () {
    this.fetchRut()
  },

  methods: {
    fetchRut () {
      let param = {}
      getRut(this.$route.params.rutid, param).then((resp) => {
        this.rut = resp.data
      })
    }
  }
}
</script>


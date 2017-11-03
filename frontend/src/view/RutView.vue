<template>
    <div class="item-view" v-if="rut">
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
            <div>
                <tip v-for="tip in tips" :key="tip.order" :tip="tip"></tip>
            </div>
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
      let r = this.rut;
      return r? r.tips: null;
    }
  },

  // Fetch rut when mounted on the client
  beforeMount () {
    this.fetchRut()
  },

  methods: {
    fetchRut () {
      let param = {}
      getRut(this.$route.params.rutid,param).then( (resp) => {
        this.rut = resp.data;
      });
    }
  }
}
// recursively fetch all descendent comments
function fetchComments (store, item) {
  if (item && item.kids) {
    return store.dispatch('FETCH_ITEMS', {
      ids: item.kids
    }).then(() => Promise.all(item.kids.map(id => {
      return fetchComments(store, store.state.items[id])
    })))
  }
}
</script>


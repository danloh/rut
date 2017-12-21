<template>
  <div class="rut-comment">
    <div class="comment-main">
      <h2>Discuss: <router-link :to="'/readuplist/' + rut.id">{{ rut.title }}</router-link></h2>
    </div>
    {{ comments.length }} Comments
    <div v-for="comment in comments" :key="comment.id">
      <comment :comment="comment"></comment>
    </div>
    <br>
    <div class="comment">
      <reply class="reply" :refer="refer" :show="true" @newreply="updateNew"></reply>
    </div>
  </div>
</template>

<script>
import { fetchRutComment } from '@/api/api'
import Comment from '@/components/Comment/Comment.vue'
import Reply from '@/components/Comment/Reply.vue'

export default {
  name: 'rut-comment',
  title () {
    return 'Discuss: ' + this.rut.title
  },
  components: { Comment, Reply },
  data () {
    return {
      rut: {},
      comments: [],
      refer: { re: 'rut', id: this.$route.params.id }
    }
  },
  methods: {
    loadCommentData () {
      let rutid = this.$route.params.id
      fetchRutComment(rutid)
      .then(resp => {
        let data = resp.data
        this.rut = data
        this.comments = data.comments
      })
    },
    updateNew (data) {
      this.comments.unshift(data)
    }
  },
  created () {
    this.loadCommentData()
  }
}
</script>

<style lang="stylus" scoped>
.rut-comment
  padding 10px 235px 10px 0px
  position relative
  .comment-main
    padding auto
  .comment-side
    position absolute
    top 10px
    right 0
    width 225px
</style>

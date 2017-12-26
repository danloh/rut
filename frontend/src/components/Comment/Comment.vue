<template>
  <div v-if="comment" class="comment">
    <div class="by">
      <router-link :to="'/profile/' + creator.id">{{ creator.name }}</router-link>
      ~ {{ comment.timestamp | timeAgo }}
    </div>
    <div class="text" v-html="commentContent"></div>
    <el-button type="text" size="mini" @click="showRe = !showRe">
      {{ showRe ? 'Hide' : 'Reply' }}
    </el-button>
    <span class="toggle" :class="{ open }" v-if="hasChild">
      <a @click="open = !open">{{ open ? '[-]' : '[+]' }} </a>
    </span>
    <reply class="reply" :refer="refer" :show.sync="showRe" @newreply="updateNew"></reply> <!--sync, hide input once submit-->
    <div class="comment-children" v-show="open">
      <comment v-for="commt in childComments" :key="commt.id" :comment="commt"></comment>  <!--recursively use-->
    </div>
  </div>
</template>

<script>
import Reply from '@/components/Comment/Reply.vue'
import marked from '@/util/marked'

export default {
  name: 'comment',
  props: ['comment'],
  components: { Reply },
  data () {
    return {
      open: true,
      showRe: false,
      hasChild: this.comment.children.length > 0,
      childComments: this.comment.children,
      refer: { re: 'comment', id: this.comment.id } // Reply's prop
    }
  },
  computed: {
    creator () {
      return this.comment.creator
    },
    commentContent () {
      return marked(this.comment.body)
    }
  },
  methods: {
    updateNew (data) {
      this.childComments.unshift(data)
    }
  }
}
</script>

<style lang="stylus" scoped>
.comment
  border-top 1px dotted green
  padding 0.2em 1em
  background-color lighten(#f3f3ed, 60%)
  position relative
  .by, .toggle
    font-size 0.75em
    margin 0.2em 0
  .by
    color #828282
    a
      color #828282
      text-decoration underline
  .text
    overflow-wrap break-word
    font-size 1.05em
    margin 0.3em 0
    a:hover
      color #ff6600
    pre
      white-space pre-wrap
  .toggle
    background-color #fffbf2
    padding 0.2em 0.5em
    border-radius 4px
    a
      color #828282
      cursor pointer
    &.open
      padding 0
      background-color transparent
      margin-bottom -0.5em
  .comment-children
    margin-left 1.5em
</style>

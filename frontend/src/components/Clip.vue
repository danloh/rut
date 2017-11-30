<template>
  <li class="clipmain">
    <p class="meta">
      <router-link :to="'/profile/' + creator.id">{{ creator.name }}</router-link>
      From <router-link :to="'/item/' + fromitem.id">{{ fromitem.title }}</router-link>
      | {{ clip.timestamp }}
    </p>
    <div class="clipbody" v-html="clip.body"></div>
  </li>
</template>

<script>
export default {
  name: 'clip',
  props: ['clip'],
  computed: {
    creator () {
      return this.clip.creator
    },
    fromitem () {
      return this.clip.fromitem
    }
  }
}
</script>

<style lang="stylus" scoped>
.clipmain
  background-color lighten(#f6f6f1, 50%)
  min-height 40px
  padding 10px
  border-bottom 2px solid #eee
  position relative
  .meta
    font-size .85em
  .clipbody
    background-color #f6f6f1
    padding 10px
    font-size 1.05em
li
  list-style-type none
</style>
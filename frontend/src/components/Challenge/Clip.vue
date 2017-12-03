<template>
  <div class="clipmain">
    <div class="clipbody" v-html="clip.body"></div>
    <p class="meta">
      From <router-link :to="'/item/' + fromitem.id" :title="fromitem.title">{{ fromitem.title.slice(0, 60) }}...</router-link>
      via <router-link :to="'/profile/' + creator.id">{{ creator.name.slice(0, 20) }}</router-link>
      | {{ clip.timestamp | toMDY }}
    </p>
  </div>
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
  padding 10px
  border-bottom 1px dotted #e09015
  position relative
  .meta
    font-size .75em
    text-align right
  .clipbody
    background-color #f6f6f1
    padding 10px
    font-size 1.05em
    color #0192b5
li
  list-style-type none
</style>
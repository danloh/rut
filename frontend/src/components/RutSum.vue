<template>
  <li class="news-item">
    <span class="score">{{ rut.score }}</span>
    <span class="title">
      <router-link :to="'/readuplist/' + rut.id">{{ rut.title }}</router-link>
    </span>
    <br>
    <span class="meta" v-html="rut.intro"></span>
    <span class="meta">
      <span>| including {{ rut.itemcount }} items</span>
    </span>
  </li>
</template>

<script>
export default {
  name: 'rut-sum',
  props: ['rut']
}
</script>

<style lang="stylus">
.news-item
  background-color #fff
  padding 20px 30px 20px 80px
  border-bottom 1px solid #eee
  position relative
  line-height 20px
  .score
    color #ff6600
    font-size 1.1em
    font-weight 700
    position absolute
    top 50%
    left 0
    width 80px
    text-align center
    margin-top -10px
  .meta
    font-size .85em
    color #828282
    a
      color #828282
      text-decoration underline
      &:hover
        color #ff6600
</style>
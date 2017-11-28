<template>
  <li class="rutsum">
    <span>
      <img :src="cover" class="cover" style="width:80px; height:100px" alt="Cover">
    </span>
    <span class="title">
      <router-link :to="'/readuplist/' + rut.id"> {{ rut.title }}</router-link>
    </span>
    <br>
    <span class="intro" v-html="rut.intro"></span>
    <br>
    <span class="meta">
      <span>| including {{ rut.itemcount }} items</span>
    </span>
  </li>
</template>

<script>
export default {
  name: 'rut-sum',
  props: ['rut'],
  computed: {
    cover () {
      return this.rut.cover
    }
  }
}
</script>

<style lang="stylus" scoped>
.rutsum
  background-color #fff
  min-height 120px
  padding 20px 30px 20px 100px
  border-bottom 1px solid #eee
  position relative
  line-height 20px
  .cover
    position absolute
    top 20px
    left 5px
  .title
    font-size 1.5em
    font-weight 700
    padding 20px 0
    a
      color #828282
      &:hover
        color #ff6600
  .intro
    font-size 1.0em
  .meta
    font-size .85em
    color #828282
</style>
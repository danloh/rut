<template>
  <div class="rutsum">
    <span>
      <img class="cover" :src="cover" style="width:80px; height:100px" alt="Cover">
    </span>
    <span class="title">
      <router-link :to="'/readuplist/' + rut.id"> {{ rut.title }}</router-link>
    </span>
    <p class="intro" v-html="rut.intro"></p>
    <span class="meta">
      <span> ~| including {{ rut.itemcount }} items | <router-link :to="'/readuplist/' + rut.id">...See Detail</router-link></span>
    </span>
  </div>
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
  padding 10px 30px 10px 100px
  border-bottom 1px solid #eee
  position relative
  .cover
    position absolute
    top 10px
    left 5px
  .title
    font-size 1.2em
    font-weight 700
    padding 10px 0
    a
      &:hover
        color #ff6600
  .meta
    font-size .85em
    color #828282
</style>
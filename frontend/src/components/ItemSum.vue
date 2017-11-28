<template>
  <div class="itemsum">
    <div>
      <img class="thumb" :src="cover" alt="Cover">
    </div>
    <div class="info">
      <span class="title">
        <router-link :to="'/item/' + item.id">{{ item.title }}</router-link>
      </span><br>
      <span><b>Byline:</b> {{ item.byline }} </span><br>
      <span><b>Published:</b> {{ item.publisher }} | {{ item.pubdate }} </span><br>
      <span><b>UID/ISBN:</b> {{ item.uid }} </span><br>
      <span><b>included:</b> {{ item.rutcount }} </span>
    </div>
    <div class="operate">
      <el-dropdown>
        <el-button type="primary" size="mini" plain>Flag it<i class="el-icon-arrow-down el-icon--right"></i></el-button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>Schedule</el-dropdown-item>
          <el-dropdown-item>Working On</el-dropdown-item>
          <el-dropdown-item>Have Done</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
export default {
  name: 'item-sum',
  props: ['item'],
  computed: {
    cover () {
      return this.item.cover
    }
  }
}
</script>

<style lang="stylus" scoped>
.itemsum
  background-color #fff
  min-height 180px
  padding 20px 30px 20px 580px
  border-bottom 1px solid #eee
  position relative
  line-height 20px
  .thumb
    width 120px
    height 160px
    position absolute
    top 10px
    left 2px
  .info
    position absolute
    top 10px
    left 150px
    width 420px
    .title
      font-size 1.2em
      font-weight 700
      a
        color #828282
        &:hover
          color lightblue
    .operate
      padding auto
li
  list-style-type none
</style>
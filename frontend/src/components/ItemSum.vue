<template>
  <div class="itemsum">
    <div>
      <img class="thumb" :src="cover" alt="Cover">
    </div>
    <div class="info">
      <span class="title">
        {{item.cate}} <router-link :to="'/item/' + item.id">{{ item.title }}</router-link>
      </span><br>
      <span><b>Byline:</b> {{ item.byline }} </span><br>
      <span><b>Published:</b> {{ item.publisher }} | {{ item.pubdate }} </span><br>
      <span><b>UID/ISBN:</b> {{ item.uid }} </span><br>
      <span><b>included:</b> {{ item.rutcount }} </span>
    </div>
    <div class="operate">
      <el-dropdown>
        <el-button type="primary" size="mini" plain>{{flagAction}}<i class="el-icon-arrow-down el-icon--right"></i></el-button>
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
  data () {
    return {
      flagAction: 'Flag it'
    }
  },
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
  padding 10px 100px 10px 140px
  border-bottom 1px solid #eee
  position relative
  .thumb
    width 120px
    height 160px
    position absolute
    top 10px
    left 2px
  .info
    font-size 0.9em
    .title
      font-size 1.2em
      font-weight 700
      a
        &:hover
          color lightblue
  .operate
    position absolute
    top 10px
    right 2px
li
  list-style-type none
</style>
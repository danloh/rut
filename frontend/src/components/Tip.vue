<template>
  <div>
    <li class="news-item">
        <item-sum :item="item"></item-sum>
    </li>
    <p>
        {{tip.tip}}
    </p>
  </div>
</template>

<script>
import ItemSum from './ItemSum.vue'

export default {
  name: 'tip',
  props: ['tip'],
  components: ['ItemSum'],
  computed: {
    item () {
      return this.tip.item
    }
  }
}
</script>
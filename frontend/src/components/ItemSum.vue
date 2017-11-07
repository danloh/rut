<template>
  <li class="news-item">
    <span class="cover">{{ item.cover }}</span>
    <span class="title">
      <router-link :to="'/item/' + item.id">{{ item.title }}</router-link>
    </span>
    <br>
    <span>Byline: {{ item.byline }} </span>
    <span>Published: {{ item.publisher }} | {{ item.pubdate }} </span>
    <span>UID/ISBN: {{ item.uid }} </span>
    <span>included: {{ item.rutcount }} </span>
  </li>
</template>

<script>
export default {
  name: 'item-sum',
  props: ['item']
}
</script>
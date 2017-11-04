<template>
  <li class="news-item">
    <span class="score">{{ rut.score }}</span>
    <span class="title">
      <router-link to="/readuplist/" + {{rut.id}}>{{ rut.title }}</router-link>
    </span>
    <br>
    <span class="meta">
      {{ rut.intro }}
    </span>
    <br>
    <span class="meta">
      <span>| including {{ rut.itemscount }} items</span>
    </span>
  </li>
</template>

<script>
export default {
  name: 'rut-sum',
  props: ['rut']
}
</script>

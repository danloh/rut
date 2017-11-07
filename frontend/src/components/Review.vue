<template>
  <li>
    <span class="title">
      {{ review.heading }}
    </span>
    <br>
    <span>{{ review.creator.name }}</span>
    <br>
    <span>{{ review.body }}</span>
  </li>
</template>

<script>
export default {
  name: 'review',
  props: ['review']
}
</script>
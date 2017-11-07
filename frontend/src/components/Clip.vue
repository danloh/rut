<template>
  <li>
    <span>{{ review.creator }}</span>
    <span>{{ clip.timestamp }}</span>
    <span>{{ clip.fromitem }}</span>
    <br>
    <span>{{ clip.body }}</span>
  </li>
</template>

<script>
export default {
  name: 'clip',
  props: ['clip']
}
</script>
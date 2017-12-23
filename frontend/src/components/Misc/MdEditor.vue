<template>
  <div id="editor">
    <mavon-editor 
      :language="'en'"
      :placeholder="'Start Writting'"
      :subfield="false"
      :toolbars="{
        bold: true,
        mark: true,
        quote: true,
        link: true,
        ol: true,
        ul: true,
        code: true,
        fullscreen: true,
        preview: true
      }">
    </mavon-editor>
  </div>
</template>

<script>
import { mavonEditor } from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'

export default {
  name: 'md-editor',
  components: { mavonEditor }
}
</script>

<style lang="stylus">
#editor
  margin: auto
  width: 100%
</style> 
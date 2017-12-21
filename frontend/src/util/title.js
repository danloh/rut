function getTitle (vm) {
  const { title } = vm.$options
  if (title) {
    return typeof title === 'function'
      ? title.call(vm)
      : title
  }
}

// 2 hooks for different data come-out timing
const clientTitleMixin = {
  beforeUpdate () {
    const title = getTitle(this)
    if (title) {
      document.title = `${title} @Readup.Tips`
    }
  },
  mounted () {
    const title = getTitle(this)
    if (title) {
      document.title = `${title} @Readup.Tips`
    }
  }
}

export default clientTitleMixin

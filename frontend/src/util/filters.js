function pluralize (time, label) {
  if (time === 1) {
    return time + label + ' ago'
  }
  return time + label + 's' + ' ago'
}
// time ago formating
export function timeAgo (date) {
  let realDate = new Date(date)
  let time = realDate.getTime()
  let offset = new Date().getTimezoneOffset() * 60
  const between = Number(Date.now()) / 1000 + offset - Number(time) / 1000
  if (between < 3600) {
    if (Object.is(~~(between / 60), 0)) return 'just now'
    return pluralize(~~(between / 60), ' minute') // double bitwise NOT -> floor
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' hour')
  } else {
    return pluralize(~~(between / 86400), ' day')
  }
}
// to local formating
export function toLocal (date) {
  return date ? new Date(date).toLocaleString() : date
}
// MDY time formating
const mapMon = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
export function toMDY (date) {
  if (!date) return date
  date = new Date(date)
  return `${mapMon[date.getMonth() + 1]} ${date.getDate()},${date.getFullYear()}` // ${date.getHours() > 11 ? 'PM' : 'AM'}
}

// showLess
export function showLess (content, least = 152, less = true) {
  if (!content) return ''
  if (content.length > least && less) {
    let lessContent = content.substring(0, least)
    let lastLinkIndex = lessContent.lastIndexOf('<a')
    let lastEndlinkIndex = lessContent.lastIndexOf('</a>')
    let actIndex = lastLinkIndex > lastEndlinkIndex ? lastLinkIndex : least // avoid to cut tag !!
    lessContent = lessContent.substring(0, actIndex) + ' ...'
    return lessContent
  } else {
    return content
  }
}

import marked from 'marked'
import Hljs from './highlight'

marked.setOptions({
  renderer: new marked.Renderer(),
  gfm: true,
  tables: true,
  breaks: true,
  pedantic: false,
  sanitize: false,
  smartLists: true,
  smartypants: false,
  highlight (code) {
    return Hljs.highlightAuto(code).value
  }
})

const renderer = new marked.Renderer()

const paragraphParse = text => `<p>${text}</p>`

const linkParse = (href, title, text) => {
  const isSelf = href.includes('readup.tips')
  const textIsImage = text.includes('<img')
  return `<a href="${href}" 
             target="_blank" 
             title="${title || (textIsImage ? href : text)}" 
             ${isSelf ? '' : 'rel="external nofollow noopenter"'}>${text}</a>`.replace(/\s+/g, ' ').replace('\n', '')
}

const imageParse = (src, title, alt) => {
  src = src.replace(/^http:\/\//ig, '/proxy/')
  return `<img src="${src}" 
               title="${title || alt || 'readup.tips'}" 
               style="width:10%; height:15%"
               alt="${alt || title || src}"/>`.replace(/\s+/g, ' ').replace('\n', '')
}

renderer.link = linkParse
renderer.image = imageParse
renderer.paragraph = paragraphParse

export default (content) => {
  // console.log('content', content)
  if (typeof content !== 'string') {
    return ''
  }
  return marked(content, { renderer })
}

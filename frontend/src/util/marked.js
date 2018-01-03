import marked from 'marked'
import Hljs from './highlight'

marked.setOptions({
  renderer: new marked.Renderer(),
  gfm: true,
  tables: true,
  breaks: false,
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
               alt="${alt || title || src}"/>`.replace(/\s+/g, ' ').replace('\n', '')
}

const blockquoteParse = (text) => {
  const classStyle = 'border-left: 4px solid #ccc; margin: 5px; padding-left: 12px;'
  return `<blockquote style="${classStyle}">${text}</blockquote>`
}

renderer.link = linkParse
renderer.image = imageParse
renderer.paragraph = paragraphParse
renderer.blockquote = blockquoteParse

export default (content) => {
  // console.log('content', content)
  if (typeof content !== 'string') {
    return ''
  }
  return marked(content, { renderer })
}

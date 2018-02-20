webpackJsonp([11],{"2+XA":function(e,t,r){t=e.exports=r("FZ+f")(!1),t.push([e.i,".icon[data-v-85311978]{color:gray}",""])},"3u5X":function(e,t,r){"use strict";var n=r("P9l9"),i=r("iF09"),s=r("6aq2"),a=r("haTO"),o=r("dUqM");t.a={name:"new-item",title:"Add New Item",components:{Spinner:a.a,MdTool:o.a},data:function(){return{checkForm:{url:"",flag:""},itemForm:{cate:"Book",title:"",uid:"",resUrl:"",byline:"",cover:"",language:"",publisher:"",publishDate:"",level:"",binding:"",page:"",price:"",details:"",flag:""},rules:{title:[{required:!0,validator:s.trimValid,message:"Please give a title",trigger:"blur"},{max:500,message:"Max Length should be 500",trigger:"blur"}],uid:[{max:128,message:"Max Length should be 128",trigger:"blur"}],resUrl:[{max:500,message:"Max Length should be 500",trigger:"blur"}],byline:[{max:500,message:"Max Length should be 500",trigger:"blur"}],cover:[{max:500,message:"Max Length should be 500",trigger:"blur"}],language:[{max:128,message:"Max Length should be 128",trigger:"blur"}],publishDate:[{max:128,message:"Max Length should be 128",trigger:"blur"}],publisher:[{max:255,message:"Max Length should be 255",trigger:"blur"}],page:[{max:64,message:"Max Length should be 64",trigger:"blur"}],level:[{max:128,message:"Max Length should be 128",trigger:"blur"}],binding:[{max:128,message:"Max Length should be 128",trigger:"blur"}],price:[{max:128,message:"Max Length should be 128",trigger:"blur"}]},show:!1,loading:!1}},methods:{onCheck:function(e,t){var r=this;this.loading=!0,this.$refs[e].validate(function(e){if(e&&Object(i.a)()){if(!t.url.trim())return r.loading=!1,r.$message("Please Input Url"),!1;var s={resUrl:t.url.trim(),flag:t.flag.trim(),how:"spider"};Object(n._16)(s).then(function(e){r.loading=!1;var t=e.data;r.$router.push("/item/"+t)})}})},onNewItem:function(e,t){var r=this;this.$refs[e].validate(function(e){if(e&&Object(i.a)()){var s=t.uid.trim(),a=t.resUrl.trim();if(!s&&!a)return r.$message({showClose:!0,message:"Either of UID and Resource URL is requied"}),!1;var o={cate:t.cate,title:t.title.trim(),uid:s,resUrl:a,byline:t.byline.trim(),cover:t.cover.trim(),Language:t.language.trim(),Publisher:t.publisher.trim(),"Publication Date":t.publishDate.trim(),Level:t.level.trim(),binding:t.binding.trim(),page:t.page.trim(),price:t.price.trim(),details:t.details.trim(),flag:t.flag.trim()};Object(n._16)(o).then(function(e){var t=e.data;r.$router.push("/item/"+t)})}})},checkAuthed:function(){Object(i.a)()||(this.$message({showClose:!0,message:"Should Log in to Continue"}),this.$router.push({path:"/login",query:{redirect:this.$route.fullPath}}))},updateN:function(e){this.itemForm.details+=e}},created:function(){this.checkAuthed()}}},"3zmR":function(e,t,r){"use strict";var n=r("GwPc");t.a={name:"md-tool",data:function(){return{previewContent:"",previewMode:!1}},props:{pretext:{type:String,default:" "}},methods:{insertContent:function(e){var t={bold:"** **",image:"![](https://)",link:"[](https://)",code:"\n```python\n \n```"};this.$emit("insertmd",t[e])},togglePreviewMode:function(){this.previewContent=Object(n.a)(this.pretext),this.previewMode=!this.previewMode}}}},"95if":function(e,t,r){t=e.exports=r("FZ+f")(!1),t.push([e.i,".spinner[data-v-4e64c895]{-webkit-transition:opacity .15s ease;transition:opacity .15s ease;-webkit-animation:rotator-data-v-4e64c895 1.4s linear infinite;animation:rotator-data-v-4e64c895 1.4s linear infinite;-webkit-animation-play-state:paused;animation-play-state:paused}.spinner.show[data-v-4e64c895]{-webkit-animation-play-state:running;animation-play-state:running}.spinner.v-enter[data-v-4e64c895],.spinner.v-leave-active[data-v-4e64c895]{opacity:0}.spinner.v-enter-active[data-v-4e64c895],.spinner.v-leave[data-v-4e64c895]{opacity:1}.spinner .path[data-v-4e64c895]{stroke:#f60;stroke-dasharray:126;stroke-dashoffset:0;-webkit-transform-origin:center;transform-origin:center;-webkit-animation:dash-data-v-4e64c895 1.4s ease-in-out infinite;animation:dash-data-v-4e64c895 1.4s ease-in-out infinite}@-webkit-keyframes rotator-data-v-4e64c895{0%{-webkit-transform:scale(.5) rotate(0deg);transform:scale(.5) rotate(0deg)}to{-webkit-transform:scale(.5) rotate(270deg);transform:scale(.5) rotate(270deg)}}@keyframes rotator-data-v-4e64c895{0%{-webkit-transform:scale(.5) rotate(0deg);transform:scale(.5) rotate(0deg)}to{-webkit-transform:scale(.5) rotate(270deg);transform:scale(.5) rotate(270deg)}}@-webkit-keyframes dash-data-v-4e64c895{0%{stroke-dashoffset:126}50%{stroke-dashoffset:63;-webkit-transform:rotate(135deg);transform:rotate(135deg)}to{stroke-dashoffset:126;-webkit-transform:rotate(450deg);transform:rotate(450deg)}}@keyframes dash-data-v-4e64c895{0%{stroke-dashoffset:126}50%{stroke-dashoffset:63;-webkit-transform:rotate(135deg);transform:rotate(135deg)}to{stroke-dashoffset:126;-webkit-transform:rotate(450deg);transform:rotate(450deg)}}",""])},A3MH:function(e,t,r){var n=r("dmw8");"string"==typeof n&&(n=[[e.i,n,""]]),n.locals&&(e.exports=n.locals);var i=r("rjj0").default;i("14c49b62",n,!0,{})},CfHv:function(e,t,r){"use strict";r.d(t,"a",function(){return n}),r.d(t,"b",function(){return i});var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"md-editor"},[r("div",{staticClass:"md-tools"},[r("a",{attrs:{href:"",title:"Bold"},on:{click:function(t){t.stopPropagation(),t.preventDefault(),e.insertContent("bold")}}},[r("b",{staticClass:"icon"},[e._v("B  ")])]),e._v(" "),r("a",{attrs:{href:"",title:"Image"},on:{click:function(t){t.stopPropagation(),t.preventDefault(),e.insertContent("image")}}},[r("i",{staticClass:"el-icon-picture icon"})]),e._v(" \n    "),r("a",{attrs:{href:"",title:"Link"},on:{click:function(t){t.stopPropagation(),t.preventDefault(),e.insertContent("link")}}},[r("i",{staticClass:"el-icon-plus icon"})]),e._v(" \n    "),r("a",{attrs:{href:"",title:"Code"},on:{click:function(t){t.stopPropagation(),t.preventDefault(),e.insertContent("code")}}},[r("i",{staticClass:"el-icon-tickets icon"})]),e._v("  \n    "),r("a",{attrs:{href:"",title:"Preview"},on:{click:function(t){t.stopPropagation(),t.preventDefault(),e.togglePreviewMode(t)}}},[r("i",{staticClass:"el-icon-view icon"})])]),e._v(" "),r("div",{directives:[{name:"show",rawName:"v-show",value:e.previewMode,expression:"previewMode"}],domProps:{innerHTML:e._s(e.previewContent)}})])},i=[]},EFqf:function(e,t,r){(function(t){(function(){"use strict";function t(e){this.tokens=[],this.tokens.links={},this.options=e||h.defaults,this.rules=m.normal,this.options.gfm&&(this.options.tables?this.rules=m.tables:this.rules=m.gfm)}function r(e,t){if(this.options=t||h.defaults,this.links=e,this.rules=g.normal,this.renderer=this.options.renderer||new n,this.renderer.options=this.options,!this.links)throw new Error("Tokens array requires a `links` property.");this.options.gfm?this.options.breaks?this.rules=g.breaks:this.rules=g.gfm:this.options.pedantic&&(this.rules=g.pedantic)}function n(e){this.options=e||{}}function i(){}function s(e){this.tokens=[],this.token=null,this.options=e||h.defaults,this.options.renderer=this.options.renderer||new n,this.renderer=this.options.renderer,this.renderer.options=this.options}function a(e,t){return e.replace(t?/&/g:/&(?!#?\w+;)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}function o(e){return e.replace(/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/gi,function(e,t){return t=t.toLowerCase(),"colon"===t?":":"#"===t.charAt(0)?"x"===t.charAt(1)?String.fromCharCode(parseInt(t.substring(2),16)):String.fromCharCode(+t.substring(1)):""})}function l(e,t){return e=e.source,t=t||"",function r(n,i){return n?(i=i.source||i,i=i.replace(/(^|[^\[])\^/g,"$1"),e=e.replace(n,i),r):new RegExp(e,t)}}function u(e,t){return d[" "+e]||(/^[^:]+:\/*[^\/]*$/.test(e)?d[" "+e]=e+"/":d[" "+e]=e.replace(/[^\/]*$/,"")),e=d[" "+e],"//"===t.slice(0,2)?e.replace(/:[\s\S]*/,":")+t:"/"===t.charAt(0)?e.replace(/(:\/*[^\/]*)[\s\S]*/,"$1")+t:e+t}function p(){}function c(e){for(var t,r,n=1;n<arguments.length;n++){t=arguments[n];for(r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e}function h(e,r,n){if(void 0===e||null===e)throw new Error("marked(): input parameter is undefined or null");if("string"!=typeof e)throw new Error("marked(): input parameter is of type "+Object.prototype.toString.call(e)+", string expected");if(n||"function"==typeof r){n||(n=r,r=null),r=c({},h.defaults,r||{});var i,o,l=r.highlight,u=0;try{i=t.lex(e,r)}catch(e){return n(e)}o=i.length;var p=function(e){if(e)return r.highlight=l,n(e);var t;try{t=s.parse(i,r)}catch(t){e=t}return r.highlight=l,e?n(e):n(null,t)};if(!l||l.length<3)return p();if(delete r.highlight,!o)return p();for(;u<i.length;u++)!function(e){"code"!==e.type?--o||p():l(e.text,e.lang,function(t,r){return t?p(t):null==r||r===e.text?--o||p():(e.text=r,e.escaped=!0,void(--o||p()))})}(i[u])}else try{return r&&(r=c({},h.defaults,r)),s.parse(t.lex(e,r),r)}catch(e){if(e.message+="\nPlease report this to https://github.com/chjj/marked.",(r||h.defaults).silent)return"<p>An error occurred:</p><pre>"+a(e.message+"",!0)+"</pre>";throw e}}var m={newline:/^\n+/,code:/^( {4}[^\n]+\n*)+/,fences:p,hr:/^ {0,3}((?:- *){3,}|(?:_ *){3,}|(?:\* *){3,})(?:\n+|$)/,heading:/^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)/,nptable:p,blockquote:/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/,list:/^( *)(bull) [\s\S]+?(?:hr|def|\n{2,}(?! )(?!\1bull )\n*|\s*$)/,html:/^ *(?:comment *(?:\n|\s*$)|closed *(?:\n{2,}|\s*$)|closing *(?:\n{2,}|\s*$))/,def:/^ {0,3}\[(label)\]: *\n? *<?([^\s>]+)>?(?:(?: +\n? *| *\n *)(title))? *(?:\n+|$)/,table:p,lheading:/^([^\n]+)\n *(=|-){2,} *(?:\n+|$)/,paragraph:/^([^\n]+(?:\n?(?!hr|heading|lheading| {0,3}>|tag)[^\n]+)+)/,text:/^[^\n]+/};m._label=/(?:\\[\[\]]|[^\[\]])+/,m._title=/(?:"(?:\\"|[^"]|"[^"\n]*")*"|'\n?(?:[^'\n]+\n?)*'|\([^()]*\))/,m.def=l(m.def)("label",m._label)("title",m._title)(),m.bullet=/(?:[*+-]|\d+\.)/,m.item=/^( *)(bull) [^\n]*(?:\n(?!\1bull )[^\n]*)*/,m.item=l(m.item,"gm")(/bull/g,m.bullet)(),m.list=l(m.list)(/bull/g,m.bullet)("hr","\\n+(?=\\1?(?:(?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$))")("def","\\n+(?="+m.def.source+")")(),m._tag="(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b",m.html=l(m.html)("comment",/<!--[\s\S]*?-->/)("closed",/<(tag)[\s\S]+?<\/\1>/)("closing",/<tag(?:"[^"]*"|'[^']*'|\s[^'"\/>]*)*?\/?>/)(/tag/g,m._tag)(),m.paragraph=l(m.paragraph)("hr",m.hr)("heading",m.heading)("lheading",m.lheading)("tag","<"+m._tag)(),m.blockquote=l(m.blockquote)("paragraph",m.paragraph)(),m.normal=c({},m),m.gfm=c({},m.normal,{fences:/^ *(`{3,}|~{3,})[ \.]*(\S+)? *\n([\s\S]*?)\n? *\1 *(?:\n+|$)/,paragraph:/^/,heading:/^ *(#{1,6}) +([^\n]+?) *#* *(?:\n+|$)/}),m.gfm.paragraph=l(m.paragraph)("(?!","(?!"+m.gfm.fences.source.replace("\\1","\\2")+"|"+m.list.source.replace("\\1","\\3")+"|")(),m.tables=c({},m.gfm,{nptable:/^ *(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)\n*/,table:/^ *\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*/}),t.rules=m,t.lex=function(e,r){return new t(r).lex(e)},t.prototype.lex=function(e){return e=e.replace(/\r\n|\r/g,"\n").replace(/\t/g,"    ").replace(/\u00a0/g," ").replace(/\u2424/g,"\n"),this.token(e,!0)},t.prototype.token=function(e,t){for(var r,n,i,s,a,o,l,u,p,c,e=e.replace(/^ +$/gm,"");e;)if((i=this.rules.newline.exec(e))&&(e=e.substring(i[0].length),i[0].length>1&&this.tokens.push({type:"space"})),i=this.rules.code.exec(e))e=e.substring(i[0].length),i=i[0].replace(/^ {4}/gm,""),this.tokens.push({type:"code",text:this.options.pedantic?i:i.replace(/\n+$/,"")});else if(i=this.rules.fences.exec(e))e=e.substring(i[0].length),this.tokens.push({type:"code",lang:i[2],text:i[3]||""});else if(i=this.rules.heading.exec(e))e=e.substring(i[0].length),this.tokens.push({type:"heading",depth:i[1].length,text:i[2]});else if(t&&(i=this.rules.nptable.exec(e))){for(e=e.substring(i[0].length),o={type:"table",header:i[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:i[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:i[3].replace(/\n$/,"").split("\n")},u=0;u<o.align.length;u++)/^ *-+: *$/.test(o.align[u])?o.align[u]="right":/^ *:-+: *$/.test(o.align[u])?o.align[u]="center":/^ *:-+ *$/.test(o.align[u])?o.align[u]="left":o.align[u]=null;for(u=0;u<o.cells.length;u++)o.cells[u]=o.cells[u].split(/ *\| */);this.tokens.push(o)}else if(i=this.rules.hr.exec(e))e=e.substring(i[0].length),this.tokens.push({type:"hr"});else if(i=this.rules.blockquote.exec(e))e=e.substring(i[0].length),this.tokens.push({type:"blockquote_start"}),i=i[0].replace(/^ *> ?/gm,""),this.token(i,t),this.tokens.push({type:"blockquote_end"});else if(i=this.rules.list.exec(e)){for(e=e.substring(i[0].length),s=i[2],this.tokens.push({type:"list_start",ordered:s.length>1}),i=i[0].match(this.rules.item),r=!1,c=i.length,u=0;u<c;u++)o=i[u],l=o.length,o=o.replace(/^ *([*+-]|\d+\.) +/,""),~o.indexOf("\n ")&&(l-=o.length,o=this.options.pedantic?o.replace(/^ {1,4}/gm,""):o.replace(new RegExp("^ {1,"+l+"}","gm"),"")),this.options.smartLists&&u!==c-1&&(a=m.bullet.exec(i[u+1])[0],s===a||s.length>1&&a.length>1||(e=i.slice(u+1).join("\n")+e,u=c-1)),n=r||/\n\n(?!\s*$)/.test(o),u!==c-1&&(r="\n"===o.charAt(o.length-1),n||(n=r)),this.tokens.push({type:n?"loose_item_start":"list_item_start"}),this.token(o,!1),this.tokens.push({type:"list_item_end"});this.tokens.push({type:"list_end"})}else if(i=this.rules.html.exec(e))e=e.substring(i[0].length),this.tokens.push({type:this.options.sanitize?"paragraph":"html",pre:!this.options.sanitizer&&("pre"===i[1]||"script"===i[1]||"style"===i[1]),text:i[0]});else if(t&&(i=this.rules.def.exec(e)))e=e.substring(i[0].length),i[3]&&(i[3]=i[3].substring(1,i[3].length-1)),p=i[1].toLowerCase(),this.tokens.links[p]||(this.tokens.links[p]={href:i[2],title:i[3]});else if(t&&(i=this.rules.table.exec(e))){for(e=e.substring(i[0].length),o={type:"table",header:i[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:i[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:i[3].replace(/(?: *\| *)?\n$/,"").split("\n")},u=0;u<o.align.length;u++)/^ *-+: *$/.test(o.align[u])?o.align[u]="right":/^ *:-+: *$/.test(o.align[u])?o.align[u]="center":/^ *:-+ *$/.test(o.align[u])?o.align[u]="left":o.align[u]=null;for(u=0;u<o.cells.length;u++)o.cells[u]=o.cells[u].replace(/^ *\| *| *\| *$/g,"").split(/ *\| */);this.tokens.push(o)}else if(i=this.rules.lheading.exec(e))e=e.substring(i[0].length),this.tokens.push({type:"heading",depth:"="===i[2]?1:2,text:i[1]});else if(t&&(i=this.rules.paragraph.exec(e)))e=e.substring(i[0].length),this.tokens.push({type:"paragraph",text:"\n"===i[1].charAt(i[1].length-1)?i[1].slice(0,-1):i[1]});else if(i=this.rules.text.exec(e))e=e.substring(i[0].length),this.tokens.push({type:"text",text:i[0]});else if(e)throw new Error("Infinite loop on byte: "+e.charCodeAt(0));return this.tokens};var g={escape:/^\\([\\`*{}\[\]()#+\-.!_>])/,autolink:/^<(scheme:[^\s\x00-\x1f<>]*|email)>/,url:p,tag:/^<!--[\s\S]*?-->|^<\/?[a-zA-Z0-9\-]+(?:"[^"]*"|'[^']*'|\s[^<'">\/]*)*?\/?>/,link:/^!?\[(inside)\]\(href\)/,reflink:/^!?\[(inside)\]\s*\[([^\]]*)\]/,nolink:/^!?\[((?:\[[^\]]*\]|\\[\[\]]|[^\[\]])*)\]/,strong:/^__([\s\S]+?)__(?!_)|^\*\*([\s\S]+?)\*\*(?!\*)/,em:/^_([^\s_](?:[^_]|__)+?[^\s_])_\b|^\*((?:\*\*|[^*])+?)\*(?!\*)/,code:/^(`+)(\s*)([\s\S]*?[^`]?)\2\1(?!`)/,br:/^ {2,}\n(?!\s*$)/,del:p,text:/^[\s\S]+?(?=[\\<!\[`*]|\b_| {2,}\n|$)/};g._scheme=/[a-zA-Z][a-zA-Z0-9+.-]{1,31}/,g._email=/[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/,g.autolink=l(g.autolink)("scheme",g._scheme)("email",g._email)(),g._inside=/(?:\[[^\]]*\]|\\[\[\]]|[^\[\]]|\](?=[^\[]*\]))*/,g._href=/\s*<?([\s\S]*?)>?(?:\s+['"]([\s\S]*?)['"])?\s*/,g.link=l(g.link)("inside",g._inside)("href",g._href)(),g.reflink=l(g.reflink)("inside",g._inside)(),g.normal=c({},g),g.pedantic=c({},g.normal,{strong:/^__(?=\S)([\s\S]*?\S)__(?!_)|^\*\*(?=\S)([\s\S]*?\S)\*\*(?!\*)/,em:/^_(?=\S)([\s\S]*?\S)_(?!_)|^\*(?=\S)([\s\S]*?\S)\*(?!\*)/}),g.gfm=c({},g.normal,{escape:l(g.escape)("])","~|])")(),url:l(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/)("email",g._email)(),_backpedal:/(?:[^?!.,:;*_~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_~)]+(?!$))+/,del:/^~~(?=\S)([\s\S]*?\S)~~/,text:l(g.text)("]|","~]|")("|","|https?://|ftp://|www\\.|[a-zA-Z0-9.!#$%&'*+/=?^_`{\\|}~-]+@|")()}),g.breaks=c({},g.gfm,{br:l(g.br)("{2,}","*")(),text:l(g.gfm.text)("{2,}","*")()}),r.rules=g,r.output=function(e,t,n){return new r(t,n).output(e)},r.prototype.output=function(e){for(var t,r,n,i,s="";e;)if(i=this.rules.escape.exec(e))e=e.substring(i[0].length),s+=i[1];else if(i=this.rules.autolink.exec(e))e=e.substring(i[0].length),"@"===i[2]?(r=a(this.mangle(i[1])),n="mailto:"+r):(r=a(i[1]),n=r),s+=this.renderer.link(n,null,r);else if(this.inLink||!(i=this.rules.url.exec(e))){if(i=this.rules.tag.exec(e))!this.inLink&&/^<a /i.test(i[0])?this.inLink=!0:this.inLink&&/^<\/a>/i.test(i[0])&&(this.inLink=!1),e=e.substring(i[0].length),s+=this.options.sanitize?this.options.sanitizer?this.options.sanitizer(i[0]):a(i[0]):i[0];else if(i=this.rules.link.exec(e))e=e.substring(i[0].length),this.inLink=!0,s+=this.outputLink(i,{href:i[2],title:i[3]}),this.inLink=!1;else if((i=this.rules.reflink.exec(e))||(i=this.rules.nolink.exec(e))){if(e=e.substring(i[0].length),t=(i[2]||i[1]).replace(/\s+/g," "),!(t=this.links[t.toLowerCase()])||!t.href){s+=i[0].charAt(0),e=i[0].substring(1)+e;continue}this.inLink=!0,s+=this.outputLink(i,t),this.inLink=!1}else if(i=this.rules.strong.exec(e))e=e.substring(i[0].length),s+=this.renderer.strong(this.output(i[2]||i[1]));else if(i=this.rules.em.exec(e))e=e.substring(i[0].length),s+=this.renderer.em(this.output(i[2]||i[1]));else if(i=this.rules.code.exec(e))e=e.substring(i[0].length),s+=this.renderer.codespan(a(i[3].trim(),!0));else if(i=this.rules.br.exec(e))e=e.substring(i[0].length),s+=this.renderer.br();else if(i=this.rules.del.exec(e))e=e.substring(i[0].length),s+=this.renderer.del(this.output(i[1]));else if(i=this.rules.text.exec(e))e=e.substring(i[0].length),s+=this.renderer.text(a(this.smartypants(i[0])));else if(e)throw new Error("Infinite loop on byte: "+e.charCodeAt(0))}else i[0]=this.rules._backpedal.exec(i[0])[0],e=e.substring(i[0].length),"@"===i[2]?(r=a(i[0]),n="mailto:"+r):(r=a(i[0]),n="www."===i[1]?"http://"+r:r),s+=this.renderer.link(n,null,r);return s},r.prototype.outputLink=function(e,t){var r=a(t.href),n=t.title?a(t.title):null;return"!"!==e[0].charAt(0)?this.renderer.link(r,n,this.output(e[1])):this.renderer.image(r,n,a(e[1]))},r.prototype.smartypants=function(e){return this.options.smartypants?e.replace(/---/g,"—").replace(/--/g,"–").replace(/(^|[-\u2014\/(\[{"\s])'/g,"$1‘").replace(/'/g,"’").replace(/(^|[-\u2014\/(\[{\u2018\s])"/g,"$1“").replace(/"/g,"”").replace(/\.{3}/g,"…"):e},r.prototype.mangle=function(e){if(!this.options.mangle)return e;for(var t,r="",n=e.length,i=0;i<n;i++)t=e.charCodeAt(i),Math.random()>.5&&(t="x"+t.toString(16)),r+="&#"+t+";";return r},n.prototype.code=function(e,t,r){if(this.options.highlight){var n=this.options.highlight(e,t);null!=n&&n!==e&&(r=!0,e=n)}return t?'<pre><code class="'+this.options.langPrefix+a(t,!0)+'">'+(r?e:a(e,!0))+"\n</code></pre>\n":"<pre><code>"+(r?e:a(e,!0))+"\n</code></pre>"},n.prototype.blockquote=function(e){return"<blockquote>\n"+e+"</blockquote>\n"},n.prototype.html=function(e){return e},n.prototype.heading=function(e,t,r){return"<h"+t+' id="'+this.options.headerPrefix+r.toLowerCase().replace(/[^\w]+/g,"-")+'">'+e+"</h"+t+">\n"},n.prototype.hr=function(){return this.options.xhtml?"<hr/>\n":"<hr>\n"},n.prototype.list=function(e,t){var r=t?"ol":"ul";return"<"+r+">\n"+e+"</"+r+">\n"},n.prototype.listitem=function(e){return"<li>"+e+"</li>\n"},n.prototype.paragraph=function(e){return"<p>"+e+"</p>\n"},n.prototype.table=function(e,t){return"<table>\n<thead>\n"+e+"</thead>\n<tbody>\n"+t+"</tbody>\n</table>\n"},n.prototype.tablerow=function(e){return"<tr>\n"+e+"</tr>\n"},n.prototype.tablecell=function(e,t){var r=t.header?"th":"td";return(t.align?"<"+r+' style="text-align:'+t.align+'">':"<"+r+">")+e+"</"+r+">\n"},n.prototype.strong=function(e){return"<strong>"+e+"</strong>"},n.prototype.em=function(e){return"<em>"+e+"</em>"},n.prototype.codespan=function(e){return"<code>"+e+"</code>"},n.prototype.br=function(){return this.options.xhtml?"<br/>":"<br>"},n.prototype.del=function(e){return"<del>"+e+"</del>"},n.prototype.link=function(e,t,r){if(this.options.sanitize){try{var n=decodeURIComponent(o(e)).replace(/[^\w:]/g,"").toLowerCase()}catch(e){return r}if(0===n.indexOf("javascript:")||0===n.indexOf("vbscript:")||0===n.indexOf("data:"))return r}this.options.baseUrl&&!f.test(e)&&(e=u(this.options.baseUrl,e));var i='<a href="'+e+'"';return t&&(i+=' title="'+t+'"'),i+=">"+r+"</a>"},n.prototype.image=function(e,t,r){this.options.baseUrl&&!f.test(e)&&(e=u(this.options.baseUrl,e));var n='<img src="'+e+'" alt="'+r+'"';return t&&(n+=' title="'+t+'"'),n+=this.options.xhtml?"/>":">"},n.prototype.text=function(e){return e},i.prototype.strong=i.prototype.em=i.prototype.codespan=i.prototype.del=i.prototype.text=function(e){return e},i.prototype.link=i.prototype.image=function(e,t,r){return""+r},i.prototype.br=function(){return""},s.parse=function(e,t){return new s(t).parse(e)},s.prototype.parse=function(e){this.inline=new r(e.links,this.options),this.inlineText=new r(e.links,c({},this.options,{renderer:new i})),this.tokens=e.reverse();for(var t="";this.next();)t+=this.tok();return t},s.prototype.next=function(){return this.token=this.tokens.pop()},s.prototype.peek=function(){return this.tokens[this.tokens.length-1]||0},s.prototype.parseText=function(){for(var e=this.token.text;"text"===this.peek().type;)e+="\n"+this.next().text;return this.inline.output(e)},s.prototype.tok=function(){switch(this.token.type){case"space":return"";case"hr":return this.renderer.hr();case"heading":return this.renderer.heading(this.inline.output(this.token.text),this.token.depth,o(this.inlineText.output(this.token.text)));case"code":return this.renderer.code(this.token.text,this.token.lang,this.token.escaped);case"table":var e,t,r,n,i="",s="";for(r="",e=0;e<this.token.header.length;e++)r+=this.renderer.tablecell(this.inline.output(this.token.header[e]),{header:!0,align:this.token.align[e]});for(i+=this.renderer.tablerow(r),e=0;e<this.token.cells.length;e++){for(t=this.token.cells[e],r="",n=0;n<t.length;n++)r+=this.renderer.tablecell(this.inline.output(t[n]),{header:!1,align:this.token.align[n]});s+=this.renderer.tablerow(r)}return this.renderer.table(i,s);case"blockquote_start":for(var s="";"blockquote_end"!==this.next().type;)s+=this.tok();return this.renderer.blockquote(s);case"list_start":for(var s="",a=this.token.ordered;"list_end"!==this.next().type;)s+=this.tok();return this.renderer.list(s,a);case"list_item_start":for(var s="";"list_item_end"!==this.next().type;)s+="text"===this.token.type?this.parseText():this.tok();return this.renderer.listitem(s);case"loose_item_start":for(var s="";"list_item_end"!==this.next().type;)s+=this.tok();return this.renderer.listitem(s);case"html":var l=this.token.pre||this.options.pedantic?this.token.text:this.inline.output(this.token.text);return this.renderer.html(l);case"paragraph":return this.renderer.paragraph(this.inline.output(this.token.text));case"text":return this.renderer.paragraph(this.parseText())}};var d={},f=/^$|^[a-z][a-z0-9+.-]*:|^[?#]/i;p.exec=p,h.options=h.setOptions=function(e){return c(h.defaults,e),h},h.defaults={gfm:!0,tables:!0,breaks:!1,pedantic:!1,sanitize:!1,sanitizer:null,mangle:!0,smartLists:!1,silent:!1,highlight:null,langPrefix:"lang-",smartypants:!1,headerPrefix:"",renderer:new n,xhtml:!1,baseUrl:null},h.Parser=s,h.parser=s.parse,h.Renderer=n,h.TextRenderer=i,h.Lexer=t,h.lexer=t.lex,h.InlineLexer=r,h.inlineLexer=r.output,h.parse=h,e.exports=h}).call(function(){return this||("undefined"!=typeof window?window:t)}())}).call(t,r("DuR2"))},GwPc:function(e,t,r){"use strict";var n=r("EFqf"),i=r.n(n);i.a.setOptions({renderer:new i.a.Renderer,gfm:!0,tables:!0,breaks:!0,pedantic:!1,sanitize:!1,smartLists:!0,smartypants:!1});var s=new i.a.Renderer,a=function(e){return"<p>"+e+"</p>"},o=function(e,t,r){var n=e.includes("readup.tips"),i=r.includes("<img");return('<a href="'+e+'" \n             target="_blank"\n             title="'+(t||(i?e:r))+'" \n             '+(n?"":'rel="external nofollow noopener noreferrer"')+">"+r+"\n          </a>").replace(/\s+/g," ").replace("\n","")},l=function(e,t,r){return('<a href="'+e+'" \n             target="_blank" rel="nofollow noopener noreferrer">\n            <img src="'+e+'" \n                title="'+(t||r||"readup.tips")+'" \n                style="width:10%; height:15%"\n                alt="'+(r||t||e)+'"/>\n          </a>').replace(/\s+/g," ").replace("\n","")};s.link=o,s.image=l,s.paragraph=a,t.a=function(e){return"string"!=typeof e?"":i()(e,{renderer:s})}},Yl6R:function(e,t,r){"use strict";t.a={name:"spinner",props:["show"]}},ZBxN:function(e,t,r){"use strict";r.d(t,"a",function(){return n}),r.d(t,"b",function(){return i});var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("transition",[r("svg",{directives:[{name:"show",rawName:"v-show",value:e.show,expression:"show"}],staticClass:"spinner",class:{show:e.show},attrs:{width:"44px",height:"44px",viewBox:"0 0 44 44"}},[r("circle",{staticClass:"path",attrs:{fill:"none","stroke-width":"4","stroke-linecap":"round",cx:"22",cy:"22",r:"20"}})])])},i=[]},cGds:function(e,t,r){var n=r("2+XA");"string"==typeof n&&(n=[[e.i,n,""]]),n.locals&&(e.exports=n.locals);var i=r("rjj0").default;i("5a562a63",n,!0,{})},dUqM:function(e,t,r){"use strict";function n(e){r("cGds")}var i=r("3zmR"),s=r("CfHv"),a=r("XyMi"),o=n,l=Object(a.a)(i.a,s.a,s.b,!1,o,"data-v-85311978",null);t.a=l.exports},dmw8:function(e,t,r){t=e.exports=r("FZ+f")(!1),t.push([e.i,".new-page[data-v-fcd78518]{padding:10px 120px 10px 80px;position:relative}.new-page .check-form[data-v-fcd78518],.new-page .new-form[data-v-fcd78518]{padding:20px;border:1px dotted #689f38}.new-page .title[data-v-fcd78518]{margin-bottom:10px;text-align:center}",""])},hTVM:function(e,t,r){"use strict";function n(e){r("A3MH")}Object.defineProperty(t,"__esModule",{value:!0});var i=r("3u5X"),s=r("zwbl"),a=r("XyMi"),o=n,l=Object(a.a)(i.a,s.a,s.b,!1,o,"data-v-fcd78518",null);t.default=l.exports},haTO:function(e,t,r){"use strict";function n(e){r("zO16")}var i=r("Yl6R"),s=r("ZBxN"),a=r("XyMi"),o=n,l=Object(a.a)(i.a,s.a,s.b,!1,o,"data-v-4e64c895",null);t.a=l.exports},zO16:function(e,t,r){var n=r("95if");"string"==typeof n&&(n=[[e.i,n,""]]),n.locals&&(e.exports=n.locals);var i=r("rjj0").default;i("15ca878a",n,!0,{})},zwbl:function(e,t,r){"use strict";r.d(t,"a",function(){return n}),r.d(t,"b",function(){return i});var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"new-page"},[e._m(0),e._v(" "),r("p",{staticStyle:{color:"green","font-size":"0.8em"}},[e._v("\n    An Item can be anything: Book, Course, Documentary, Paper, Atlas, Place to visit, Exppriment to perform, etc.\n  ")]),e._v(" "),r("spinner",{attrs:{show:e.loading}}),e._v(" "),r("el-button",{attrs:{size:"small",type:"primary"}},[e._v("\n    "+e._s(e.show?"Add Item Info Manually":"Fetch Item Info via Spider")+"\n  ")]),e._v(" "),r("el-button",{attrs:{size:"mini",type:"text"},on:{click:function(t){e.show=!e.show}}},[e._v("\n    or "+e._s(e.show?"Fetch Item Info via Spider":"Add Item Info Manually")+"\n  ")]),e._v(" "),r("el-form",{directives:[{name:"show",rawName:"v-show",value:!e.show,expression:"!show"}],ref:"checkForm",staticClass:"check-form",attrs:{model:e.checkForm,size:"mini"}},[r("el-form-item",{attrs:{label:"URL: e.g. Amazon/Coursera url Or UID: e.g. ISBN-13",prop:"url"}},[r("el-input",{attrs:{type:"textarea",autosize:""},model:{value:e.checkForm.url,callback:function(t){e.$set(e.checkForm,"url",t)},expression:"checkForm.url"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Flag as",prop:"flag"}},[r("el-radio-group",{model:{value:e.checkForm.flag,callback:function(t){e.$set(e.checkForm,"flag",t)},expression:"checkForm.flag"}},[r("el-radio-button",{attrs:{label:"Have Done"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Schedule"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Working On"}})],1)],1),e._v(" "),r("el-form-item",[r("el-button",{attrs:{type:"success",size:"medium"},on:{click:function(t){e.onCheck("checkForm",e.checkForm)}}},[e._v("\n                 Fetch Via Spider\n      ")])],1)],1),e._v(" "),r("el-form",{directives:[{name:"show",rawName:"v-show",value:e.show,expression:"show"}],ref:"itemForm",staticClass:"new-form",attrs:{model:e.itemForm,rules:e.rules,"label-width":"130px",size:"mini"}},[r("el-form-item",{attrs:{label:"Type",prop:"cate"}},[r("el-radio-group",{model:{value:e.itemForm.cate,callback:function(t){e.$set(e.itemForm,"cate",t)},expression:"itemForm.cate"}},[r("el-radio-button",{attrs:{label:"Book"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Video"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Course"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Online"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Paper"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Atlas"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Album"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Place"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Other"}})],1)],1),e._v(" "),r("el-form-item",{attrs:{label:"Title",prop:"title"}},[r("el-input",{attrs:{type:"textarea",autosize:""},model:{value:e.itemForm.title,callback:function(t){e.$set(e.itemForm,"title",t)},expression:"itemForm.title"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"UID*",prop:"uid"}},[r("el-input",{attrs:{placeholder:"either UID. e.g. ISBN, etc. "},model:{value:e.itemForm.uid,callback:function(t){e.$set(e.itemForm,"uid",t)},expression:"itemForm.uid"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Resource URL*",prop:"resurl"}},[r("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"or URL. e.g. a online course link, etc. "},model:{value:e.itemForm.resUrl,callback:function(t){e.$set(e.itemForm,"resUrl",t)},expression:"itemForm.resUrl"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Byline",prop:"byline"}},[r("el-input",{attrs:{placeholder:"Auther or Instructor, etc."},model:{value:e.itemForm.byline,callback:function(t){e.$set(e.itemForm,"byline",t)},expression:"itemForm.byline"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Cover / Logo",prop:"cover"}},[r("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"Image URL"},model:{value:e.itemForm.cover,callback:function(t){e.$set(e.itemForm,"cover",t)},expression:"itemForm.cover"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Language",prop:"language"}},[r("el-input",{model:{value:e.itemForm.language,callback:function(t){e.$set(e.itemForm,"language",t)},expression:"itemForm.language"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Publisher",prop:"publisher"}},[r("el-input",{model:{value:e.itemForm.publisher,callback:function(t){e.$set(e.itemForm,"publisher",t)},expression:"itemForm.publisher"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Publish Date",prop:"publishDate"}},[r("el-input",{attrs:{placeholder:"Book Publish date or Start date of a Course"},model:{value:e.itemForm.publishDate,callback:function(t){e.$set(e.itemForm,"publishDate",t)},expression:"itemForm.publishDate"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Page / Duration",prop:"page"}},[r("el-input",{attrs:{placeholder:"Pages of Book or Duration of video / course"},model:{value:e.itemForm.page,callback:function(t){e.$set(e.itemForm,"page",t)},expression:"itemForm.page"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Level",prop:"level"}},[r("el-input",{model:{value:e.itemForm.level,callback:function(t){e.$set(e.itemForm,"level",t)},expression:"itemForm.level"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Binding / Format",prop:"binding"}},[r("el-input",{model:{value:e.itemForm.binding,callback:function(t){e.$set(e.itemForm,"binding",t)},expression:"itemForm.binding"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Price",prop:"price"}},[r("el-input",{model:{value:e.itemForm.price,callback:function(t){e.$set(e.itemForm,"price",t)},expression:"itemForm.price"}})],1),e._v(" "),r("el-form-item",{attrs:{label:"More Details",prop:"details"}},[r("el-input",{attrs:{type:"textarea",autosize:{minRows:3}},model:{value:e.itemForm.details,callback:function(t){e.$set(e.itemForm,"details",t)},expression:"itemForm.details"}}),e._v(" "),r("md-tool",{attrs:{pretext:e.itemForm.details},on:{insertmd:e.updateN}})],1),e._v(" "),r("el-form-item",{attrs:{label:"Flag as",prop:"flag"}},[r("el-radio-group",{model:{value:e.itemForm.flag,callback:function(t){e.$set(e.itemForm,"flag",t)},expression:"itemForm.flag"}},[r("el-radio-button",{attrs:{label:"Have Done"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Schedule"}}),e._v(" "),r("el-radio-button",{attrs:{label:"Working On"}})],1)],1),e._v(" "),r("el-form-item",[r("el-button",{attrs:{type:"success",size:"medium"},on:{click:function(t){e.onNewItem("itemForm",e.itemForm)}}},[e._v("\n                 Done and Add\n      ")])],1)],1)],1)},i=[function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"title"},[r("b",[e._v("Submit New Item")]),e._v(" ")])}]}});
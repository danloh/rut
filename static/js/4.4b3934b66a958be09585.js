webpackJsonp([4],{"+lgA":function(e,t,n){"use strict";var r=n("P9l9"),s=n("iF09");t.a={name:"demand",props:["demand"],data:function(){return{vote:this.demand.vote,answercount:this.demand.answercount}},computed:{requestor:function(){return this.demand.requestor}},methods:{upDemand:function(){var e=this;if(Object(s.a)()){var t=this.demand.id;Object(r._48)(t).then(function(t){e.vote=t.data})}}}}},"+rdc":function(e,t,n){var r=n("wmsc");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);var s=n("rjj0").default;s("377391e2",r,!0,{})},"1ngo":function(e,t,n){var r=n("uGMt");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);var s=n("rjj0").default;s("246aa54c",r,!0,{})},"2Xs0":function(e,t,n){var r=n("OjYV");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);var s=n("rjj0").default;s("52134d86",r,!0,{})},"5zb4":function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return s});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"comment-view"},[e.comment?n("div",{staticClass:"comment"},[n("div",{staticClass:"by",attrs:{id:"comment"+e.commentid}},[n("router-link",{attrs:{to:"/profile/"+e.creator.id}},[n("b",[e._v(e._s(e.creator.name))])]),e._v("\n        "+e._s(e._f("timeAgo")(e.comment.timestamp))+"\n    ")],1),e._v(" "),n("div",{staticClass:"content",domProps:{innerHTML:e._s(e.commentContent)}}),e._v(" "),n("el-button",{attrs:{type:"text",size:"mini",title:"like"},on:{click:e.upComment}},[n("small",{staticStyle:{color:"#aaa"}},[e._v("Like")])]),e._v(" "),n("el-button",{attrs:{type:"text",size:"mini"},on:{click:function(t){e.showRe=!e.showRe}}},[n("small",{staticStyle:{color:"#aaa"}},[e._v("\n        "+e._s(e.showRe?"Hide":e.childComments.length+"  Reply")+"\n      ")])]),e._v(" "),n("div",{directives:[{name:"show",rawName:"v-show",value:e.showRe,expression:"showRe"}],staticClass:"comment-children"},[e._l(e.childComments,function(e){return n("comment",{key:e.id,attrs:{comment:e}})}),e._v(" "),n("reply",{staticClass:"reply",staticStyle:{"margin-left":"5px"},attrs:{refer:e.refer,show:e.showRe},on:{"update:show":function(t){e.showRe=t},newreply:e.updateNew}})],2)],1):e._e()])},s=[]},"80WQ":function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return s});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return e.requestor?n("div",{staticClass:"demand-main"},[n("div",{staticClass:"demand-body"},[n("router-link",{attrs:{to:"/demand/"+e.demand.id}},[n("b",[e._v(e._s(e.demand.body))])])],1),e._v(" "),n("div",{staticClass:"demand-bar"},[e.demand.tag.tagname?n("router-link",{attrs:{to:"/tag/"+e.demand.tag.tagname}},[e._v("\n      #"+e._s(e.demand.tag.tagname)+"\n    ")]):e._e(),e._v("\n    | "+e._s(e._f("toMDY")(e.demand.timestamp))+"\n    - by "),n("router-link",{attrs:{to:"/profile/"+e.requestor.id}},[e._v("\n        "+e._s(e.requestor.name)+"\n      ")]),e._v("\n    | "+e._s(e.vote)+" "),n("el-button",{attrs:{type:"text"},on:{click:e.upDemand}},[e._v("vote")]),e._v("\n    | "),n("router-link",{attrs:{to:"/create/"+e.demand.id}},[e._v("\n        "+e._s(e._f("pluralise")(e.answercount,"Answer"))+"\n      ")]),e._v("\n    - "),n("router-link",{attrs:{to:"/demand/"+e.demand.id}},[e._v("\n        "+e._s(e._f("pluralise")(e.demand.commentcount,"Comment"))+"\n      ")])],1)]):e._e()},s=[]},EFqf:function(e,t,n){(function(t){!function(t){"use strict";function n(e){this.tokens=[],this.tokens.links={},this.options=e||m.defaults,this.rules=f.normal,this.options.pedantic?this.rules=f.pedantic:this.options.gfm&&(this.options.tables?this.rules=f.tables:this.rules=f.gfm)}function r(e,t){if(this.options=t||m.defaults,this.links=e,this.rules=g.normal,this.renderer=this.options.renderer||new s,this.renderer.options=this.options,!this.links)throw new Error("Tokens array requires a `links` property.");this.options.pedantic?this.rules=g.pedantic:this.options.gfm&&(this.options.breaks?this.rules=g.breaks:this.rules=g.gfm)}function s(e){this.options=e||m.defaults}function i(){}function a(e){this.tokens=[],this.token=null,this.options=e||m.defaults,this.options.renderer=this.options.renderer||new s,this.renderer=this.options.renderer,this.renderer.options=this.options}function o(e,t){return e.replace(t?/&/g:/&(?!#?\w+;)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}function l(e){return e.replace(/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/gi,function(e,t){return t=t.toLowerCase(),"colon"===t?":":"#"===t.charAt(0)?"x"===t.charAt(1)?String.fromCharCode(parseInt(t.substring(2),16)):String.fromCharCode(+t.substring(1)):""})}function c(e,t){return e=e.source||e,t=t||"",{replace:function(t,n){return n=n.source||n,n=n.replace(/(^|[^\[])\^/g,"$1"),e=e.replace(t,n),this},getRegex:function(){return new RegExp(e,t)}}}function u(e,t){return b[" "+e]||(/^[^:]+:\/*[^\/]*$/.test(e)?b[" "+e]=e+"/":b[" "+e]=e.replace(/[^\/]*$/,"")),e=b[" "+e],"//"===t.slice(0,2)?e.replace(/:[\s\S]*/,":")+t:"/"===t.charAt(0)?e.replace(/(:\/*[^\/]*)[\s\S]*/,"$1")+t:e+t}function h(){}function p(e){for(var t,n,r=1;r<arguments.length;r++){t=arguments[r];for(n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e}function d(e,t){var n=e.replace(/([^\\])\|/g,"$1 |").split(/ +\| */),r=0;if(n.length>t)n.splice(t);else for(;n.length<t;)n.push("");for(;r<n.length;r++)n[r]=n[r].replace(/\\\|/g,"|");return n}function m(e,t,r){if(void 0===e||null===e)throw new Error("marked(): input parameter is undefined or null");if("string"!=typeof e)throw new Error("marked(): input parameter is of type "+Object.prototype.toString.call(e)+", string expected");if(r||"function"==typeof t){r||(r=t,t=null),t=p({},m.defaults,t||{});var s,i,l=t.highlight,c=0;try{s=n.lex(e,t)}catch(e){return r(e)}i=s.length;var u=function(e){if(e)return t.highlight=l,r(e);var n;try{n=a.parse(s,t)}catch(t){e=t}return t.highlight=l,e?r(e):r(null,n)};if(!l||l.length<3)return u();if(delete t.highlight,!i)return u();for(;c<s.length;c++)!function(e){"code"!==e.type?--i||u():l(e.text,e.lang,function(t,n){return t?u(t):null==n||n===e.text?--i||u():(e.text=n,e.escaped=!0,void(--i||u()))})}(s[c])}else try{return t&&(t=p({},m.defaults,t)),a.parse(n.lex(e,t),t)}catch(e){if(e.message+="\nPlease report this to https://github.com/markedjs/marked.",(t||m.defaults).silent)return"<p>An error occurred:</p><pre>"+o(e.message+"",!0)+"</pre>";throw e}}var f={newline:/^\n+/,code:/^( {4}[^\n]+\n*)+/,fences:h,hr:/^ {0,3}((?:- *){3,}|(?:_ *){3,}|(?:\* *){3,})(?:\n+|$)/,heading:/^ *(#{1,6}) *([^\n]+?) *(?:#+ *)?(?:\n+|$)/,nptable:h,blockquote:/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/,list:/^( *)(bull) [\s\S]+?(?:hr|def|\n{2,}(?! )(?!\1bull )\n*|\s*$)/,html:"^ {0,3}(?:<(script|pre|style)[\\s>][\\s\\S]*?(?:</\\1>[^\\n]*\\n+|$)|comment[^\\n]*(\\n+|$)|<\\?[\\s\\S]*?\\?>\\n*|<![A-Z][\\s\\S]*?>\\n*|<!\\[CDATA\\[[\\s\\S]*?\\]\\]>\\n*|</?(tag)(?: +|\\n|/?>)[\\s\\S]*?(?:\\n{2,}|$)|<(?!script|pre|style)([a-z][\\w-]*)(?:attribute)*? */?>(?=\\h*\\n)[\\s\\S]*?(?:\\n{2,}|$)|</(?!script|pre|style)[a-z][\\w-]*\\s*>(?=\\h*\\n)[\\s\\S]*?(?:\\n{2,}|$))",def:/^ {0,3}\[(label)\]: *\n? *<?([^\s>]+)>?(?:(?: +\n? *| *\n *)(title))? *(?:\n+|$)/,table:h,lheading:/^([^\n]+)\n *(=|-){2,} *(?:\n+|$)/,paragraph:/^([^\n]+(?:\n(?!hr|heading|lheading| {0,3}>|<\/?(?:tag)(?: +|\n|\/?>)|<(?:script|pre|style|!--))[^\n]+)*)/,text:/^[^\n]+/};f._label=/(?!\s*\])(?:\\[\[\]]|[^\[\]])+/,f._title=/(?:"(?:\\"?|[^"\\])*"|'[^'\n]*(?:\n[^'\n]+)*\n?'|\([^()]*\))/,f.def=c(f.def).replace("label",f._label).replace("title",f._title).getRegex(),f.bullet=/(?:[*+-]|\d+\.)/,f.item=/^( *)(bull) [^\n]*(?:\n(?!\1bull )[^\n]*)*/,f.item=c(f.item,"gm").replace(/bull/g,f.bullet).getRegex(),f.list=c(f.list).replace(/bull/g,f.bullet).replace("hr","\\n+(?=\\1?(?:(?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$))").replace("def","\\n+(?="+f.def.source+")").getRegex(),f._tag="address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|meta|nav|noframes|ol|optgroup|option|p|param|section|source|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul",f._comment=/<!--(?!-?>)[\s\S]*?-->/,f.html=c(f.html,"i").replace("comment",f._comment).replace("tag",f._tag).replace("attribute",/ +[a-zA-Z:_][\w.:-]*(?: *= *"[^"\n]*"| *= *'[^'\n]*'| *= *[^\s"'=<>`]+)?/).getRegex(),f.paragraph=c(f.paragraph).replace("hr",f.hr).replace("heading",f.heading).replace("lheading",f.lheading).replace("tag",f._tag).getRegex(),f.blockquote=c(f.blockquote).replace("paragraph",f.paragraph).getRegex(),f.normal=p({},f),f.gfm=p({},f.normal,{fences:/^ *(`{3,}|~{3,})[ \.]*(\S+)? *\n([\s\S]*?)\n? *\1 *(?:\n+|$)/,paragraph:/^/,heading:/^ *(#{1,6}) +([^\n]+?) *#* *(?:\n+|$)/}),f.gfm.paragraph=c(f.paragraph).replace("(?!","(?!"+f.gfm.fences.source.replace("\\1","\\2")+"|"+f.list.source.replace("\\1","\\3")+"|").getRegex(),f.tables=p({},f.gfm,{nptable:/^ *([^|\n ].*\|.*)\n *([-:]+ *\|[-| :]*)(?:\n((?:.*[^>\n ].*(?:\n|$))*)\n*|$)/,table:/^ *\|(.+)\n *\|?( *[-:]+[-| :]*)(?:\n((?: *[^>\n ].*(?:\n|$))*)\n*|$)/}),f.pedantic=p({},f.normal,{html:c("^ *(?:comment *(?:\\n|\\s*$)|<(tag)[\\s\\S]+?</\\1> *(?:\\n{2,}|\\s*$)|<tag(?:\"[^\"]*\"|'[^']*'|\\s[^'\"/>\\s]*)*?/?> *(?:\\n{2,}|\\s*$))").replace("comment",f._comment).replace(/tag/g,"(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b").getRegex(),def:/^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +(["(][^\n]+[")]))? *(?:\n+|$)/}),n.rules=f,n.lex=function(e,t){return new n(t).lex(e)},n.prototype.lex=function(e){return e=e.replace(/\r\n|\r/g,"\n").replace(/\t/g,"    ").replace(/\u00a0/g," ").replace(/\u2424/g,"\n"),this.token(e,!0)},n.prototype.token=function(e,t){e=e.replace(/^ +$/gm,"");for(var n,r,s,i,a,o,l,c,u,h,p,m,g;e;)if((s=this.rules.newline.exec(e))&&(e=e.substring(s[0].length),s[0].length>1&&this.tokens.push({type:"space"})),s=this.rules.code.exec(e))e=e.substring(s[0].length),s=s[0].replace(/^ {4}/gm,""),this.tokens.push({type:"code",text:this.options.pedantic?s:s.replace(/\n+$/,"")});else if(s=this.rules.fences.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"code",lang:s[2],text:s[3]||""});else if(s=this.rules.heading.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"heading",depth:s[1].length,text:s[2]});else if(t&&(s=this.rules.nptable.exec(e))&&(o={type:"table",header:d(s[1].replace(/^ *| *\| *$/g,"")),align:s[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:s[3]?s[3].replace(/\n$/,"").split("\n"):[]},o.header.length===o.align.length)){for(e=e.substring(s[0].length),c=0;c<o.align.length;c++)/^ *-+: *$/.test(o.align[c])?o.align[c]="right":/^ *:-+: *$/.test(o.align[c])?o.align[c]="center":/^ *:-+ *$/.test(o.align[c])?o.align[c]="left":o.align[c]=null;for(c=0;c<o.cells.length;c++)o.cells[c]=d(o.cells[c],o.header.length);this.tokens.push(o)}else if(s=this.rules.hr.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"hr"});else if(s=this.rules.blockquote.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"blockquote_start"}),s=s[0].replace(/^ *> ?/gm,""),this.token(s,t),this.tokens.push({type:"blockquote_end"});else if(s=this.rules.list.exec(e)){for(e=e.substring(s[0].length),i=s[2],p=i.length>1,this.tokens.push({type:"list_start",ordered:p,start:p?+i:""}),s=s[0].match(this.rules.item),n=!1,h=s.length,c=0;c<h;c++)o=s[c],l=o.length,o=o.replace(/^ *([*+-]|\d+\.) +/,""),~o.indexOf("\n ")&&(l-=o.length,o=this.options.pedantic?o.replace(/^ {1,4}/gm,""):o.replace(new RegExp("^ {1,"+l+"}","gm"),"")),this.options.smartLists&&c!==h-1&&(a=f.bullet.exec(s[c+1])[0],i===a||i.length>1&&a.length>1||(e=s.slice(c+1).join("\n")+e,c=h-1)),r=n||/\n\n(?!\s*$)/.test(o),c!==h-1&&(n="\n"===o.charAt(o.length-1),r||(r=n)),m=/^\[[ xX]\] /.test(o),g=void 0,m&&(g=" "!==o[1],o=o.replace(/^\[[ xX]\] +/,"")),this.tokens.push({type:r?"loose_item_start":"list_item_start",task:m,checked:g}),this.token(o,!1),this.tokens.push({type:"list_item_end"});this.tokens.push({type:"list_end"})}else if(s=this.rules.html.exec(e))e=e.substring(s[0].length),this.tokens.push({type:this.options.sanitize?"paragraph":"html",pre:!this.options.sanitizer&&("pre"===s[1]||"script"===s[1]||"style"===s[1]),text:s[0]});else if(t&&(s=this.rules.def.exec(e)))e=e.substring(s[0].length),s[3]&&(s[3]=s[3].substring(1,s[3].length-1)),u=s[1].toLowerCase().replace(/\s+/g," "),this.tokens.links[u]||(this.tokens.links[u]={href:s[2],title:s[3]});else if(t&&(s=this.rules.table.exec(e))&&(o={type:"table",header:d(s[1].replace(/^ *| *\| *$/g,"")),align:s[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:s[3]?s[3].replace(/(?: *\| *)?\n$/,"").split("\n"):[]},o.header.length===o.align.length)){for(e=e.substring(s[0].length),c=0;c<o.align.length;c++)/^ *-+: *$/.test(o.align[c])?o.align[c]="right":/^ *:-+: *$/.test(o.align[c])?o.align[c]="center":/^ *:-+ *$/.test(o.align[c])?o.align[c]="left":o.align[c]=null;for(c=0;c<o.cells.length;c++)o.cells[c]=d(o.cells[c].replace(/^ *\| *| *\| *$/g,""),o.header.length);this.tokens.push(o)}else if(s=this.rules.lheading.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"heading",depth:"="===s[2]?1:2,text:s[1]});else if(t&&(s=this.rules.paragraph.exec(e)))e=e.substring(s[0].length),this.tokens.push({type:"paragraph",text:"\n"===s[1].charAt(s[1].length-1)?s[1].slice(0,-1):s[1]});else if(s=this.rules.text.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"text",text:s[0]});else if(e)throw new Error("Infinite loop on byte: "+e.charCodeAt(0));return this.tokens};var g={escape:/^\\([!"#$%&'()*+,\-.\/:;<=>?@\[\]\\^_`{|}~])/,autolink:/^<(scheme:[^\s\x00-\x1f<>]*|email)>/,url:h,tag:"^comment|^</[a-zA-Z][\\w:-]*\\s*>|^<[a-zA-Z][\\w-]*(?:attribute)*?\\s*/?>|^<\\?[\\s\\S]*?\\?>|^<![a-zA-Z]+\\s[\\s\\S]*?>|^<!\\[CDATA\\[[\\s\\S]*?\\]\\]>",link:/^!?\[(label)\]\(href(?:\s+(title))?\s*\)/,reflink:/^!?\[(label)\]\[(?!\s*\])((?:\\[\[\]]?|[^\[\]\\])+)\]/,nolink:/^!?\[(?!\s*\])((?:\[[^\[\]]*\]|\\[\[\]]|[^\[\]])*)\](?:\[\])?/,strong:/^__([^\s][\s\S]*?[^\s])__(?!_)|^\*\*([^\s][\s\S]*?[^\s])\*\*(?!\*)|^__([^\s])__(?!_)|^\*\*([^\s])\*\*(?!\*)/,em:/^_([^\s][\s\S]*?[^\s_])_(?!_)|^_([^\s_][\s\S]*?[^\s])_(?!_)|^\*([^\s][\s\S]*?[^\s*])\*(?!\*)|^\*([^\s*][\s\S]*?[^\s])\*(?!\*)|^_([^\s_])_(?!_)|^\*([^\s*])\*(?!\*)/,code:/^(`+)\s*([\s\S]*?[^`]?)\s*\1(?!`)/,br:/^ {2,}\n(?!\s*$)/,del:h,text:/^[\s\S]+?(?=[\\<!\[`*]|\b_| {2,}\n|$)/};g._escapes=/\\([!"#$%&'()*+,\-.\/:;<=>?@\[\]\\^_`{|}~])/g,g._scheme=/[a-zA-Z][a-zA-Z0-9+.-]{1,31}/,g._email=/[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/,g.autolink=c(g.autolink).replace("scheme",g._scheme).replace("email",g._email).getRegex(),g._attribute=/\s+[a-zA-Z:_][\w.:-]*(?:\s*=\s*"[^"]*"|\s*=\s*'[^']*'|\s*=\s*[^\s"'=<>`]+)?/,g.tag=c(g.tag).replace("comment",f._comment).replace("attribute",g._attribute).getRegex(),g._label=/(?:\[[^\[\]]*\]|\\[\[\]]?|`[^`]*`|[^\[\]\\])*?/,g._href=/\s*(<(?:\\[<>]?|[^\s<>\\])*>|(?:\\[()]?|\([^\s\x00-\x1f()\\]*\)|[^\s\x00-\x1f()\\])*?)/,g._title=/"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)/,g.link=c(g.link).replace("label",g._label).replace("href",g._href).replace("title",g._title).getRegex(),g.reflink=c(g.reflink).replace("label",g._label).getRegex(),g.normal=p({},g),g.pedantic=p({},g.normal,{strong:/^__(?=\S)([\s\S]*?\S)__(?!_)|^\*\*(?=\S)([\s\S]*?\S)\*\*(?!\*)/,em:/^_(?=\S)([\s\S]*?\S)_(?!_)|^\*(?=\S)([\s\S]*?\S)\*(?!\*)/,link:c(/^!?\[(label)\]\((.*?)\)/).replace("label",g._label).getRegex(),reflink:c(/^!?\[(label)\]\s*\[([^\]]*)\]/).replace("label",g._label).getRegex()}),g.gfm=p({},g.normal,{escape:c(g.escape).replace("])","~|])").getRegex(),url:c(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/).replace("email",g._email).getRegex(),_backpedal:/(?:[^?!.,:;*_~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_~)]+(?!$))+/,del:/^~~(?=\S)([\s\S]*?\S)~~/,text:c(g.text).replace("]|","~]|").replace("|","|https?://|ftp://|www\\.|[a-zA-Z0-9.!#$%&'*+/=?^_`{\\|}~-]+@|").getRegex()}),g.breaks=p({},g.gfm,{br:c(g.br).replace("{2,}","*").getRegex(),text:c(g.gfm.text).replace("{2,}","*").getRegex()}),r.rules=g,r.output=function(e,t,n){return new r(t,n).output(e)},r.prototype.output=function(e){for(var t,n,s,i,a,l="";e;)if(a=this.rules.escape.exec(e))e=e.substring(a[0].length),l+=a[1];else if(a=this.rules.autolink.exec(e))e=e.substring(a[0].length),"@"===a[2]?(n=o(this.mangle(a[1])),s="mailto:"+n):(n=o(a[1]),s=n),l+=this.renderer.link(s,null,n);else if(this.inLink||!(a=this.rules.url.exec(e))){if(a=this.rules.tag.exec(e))!this.inLink&&/^<a /i.test(a[0])?this.inLink=!0:this.inLink&&/^<\/a>/i.test(a[0])&&(this.inLink=!1),e=e.substring(a[0].length),l+=this.options.sanitize?this.options.sanitizer?this.options.sanitizer(a[0]):o(a[0]):a[0];else if(a=this.rules.link.exec(e))e=e.substring(a[0].length),this.inLink=!0,s=a[2],this.options.pedantic?(t=/^([^'"]*[^\s])\s+(['"])(.*)\2/.exec(s),t?(s=t[1],i=t[3]):i=""):i=a[3]?a[3].slice(1,-1):"",s=s.trim().replace(/^<([\s\S]*)>$/,"$1"),l+=this.outputLink(a,{href:r.escapes(s),title:r.escapes(i)}),this.inLink=!1;else if((a=this.rules.reflink.exec(e))||(a=this.rules.nolink.exec(e))){if(e=e.substring(a[0].length),t=(a[2]||a[1]).replace(/\s+/g," "),!(t=this.links[t.toLowerCase()])||!t.href){l+=a[0].charAt(0),e=a[0].substring(1)+e;continue}this.inLink=!0,l+=this.outputLink(a,t),this.inLink=!1}else if(a=this.rules.strong.exec(e))e=e.substring(a[0].length),l+=this.renderer.strong(this.output(a[4]||a[3]||a[2]||a[1]));else if(a=this.rules.em.exec(e))e=e.substring(a[0].length),l+=this.renderer.em(this.output(a[6]||a[5]||a[4]||a[3]||a[2]||a[1]));else if(a=this.rules.code.exec(e))e=e.substring(a[0].length),l+=this.renderer.codespan(o(a[2].trim(),!0));else if(a=this.rules.br.exec(e))e=e.substring(a[0].length),l+=this.renderer.br();else if(a=this.rules.del.exec(e))e=e.substring(a[0].length),l+=this.renderer.del(this.output(a[1]));else if(a=this.rules.text.exec(e))e=e.substring(a[0].length),l+=this.renderer.text(o(this.smartypants(a[0])));else if(e)throw new Error("Infinite loop on byte: "+e.charCodeAt(0))}else a[0]=this.rules._backpedal.exec(a[0])[0],e=e.substring(a[0].length),"@"===a[2]?(n=o(a[0]),s="mailto:"+n):(n=o(a[0]),s="www."===a[1]?"http://"+n:n),l+=this.renderer.link(s,null,n);return l},r.escapes=function(e){return e?e.replace(r.rules._escapes,"$1"):e},r.prototype.outputLink=function(e,t){var n=t.href,r=t.title?o(t.title):null;return"!"!==e[0].charAt(0)?this.renderer.link(n,r,this.output(e[1])):this.renderer.image(n,r,o(e[1]))},r.prototype.smartypants=function(e){return this.options.smartypants?e.replace(/---/g,"—").replace(/--/g,"–").replace(/(^|[-\u2014\/(\[{"\s])'/g,"$1‘").replace(/'/g,"’").replace(/(^|[-\u2014\/(\[{\u2018\s])"/g,"$1“").replace(/"/g,"”").replace(/\.{3}/g,"…"):e},r.prototype.mangle=function(e){if(!this.options.mangle)return e;for(var t,n="",r=e.length,s=0;s<r;s++)t=e.charCodeAt(s),Math.random()>.5&&(t="x"+t.toString(16)),n+="&#"+t+";";return n},s.prototype.code=function(e,t,n){if(this.options.highlight){var r=this.options.highlight(e,t);null!=r&&r!==e&&(n=!0,e=r)}return t?'<pre><code class="'+this.options.langPrefix+o(t,!0)+'">'+(n?e:o(e,!0))+"</code></pre>\n":"<pre><code>"+(n?e:o(e,!0))+"</code></pre>"},s.prototype.blockquote=function(e){return"<blockquote>\n"+e+"</blockquote>\n"},s.prototype.html=function(e){return e},s.prototype.heading=function(e,t,n){return this.options.headerIds?"<h"+t+' id="'+this.options.headerPrefix+n.toLowerCase().replace(/[^\w]+/g,"-")+'">'+e+"</h"+t+">\n":"<h"+t+">"+e+"</h"+t+">\n"},s.prototype.hr=function(){return this.options.xhtml?"<hr/>\n":"<hr>\n"},s.prototype.list=function(e,t,n){var r=t?"ol":"ul";return"<"+r+(t&&1!==n?' start="'+n+'"':"")+">\n"+e+"</"+r+">\n"},s.prototype.listitem=function(e){return"<li>"+e+"</li>\n"},s.prototype.checkbox=function(e){return"<input "+(e?'checked="" ':"")+'disabled="" type="checkbox"'+(this.options.xhtml?" /":"")+"> "},s.prototype.paragraph=function(e){return"<p>"+e+"</p>\n"},s.prototype.table=function(e,t){return t&&(t="<tbody>"+t+"</tbody>"),"<table>\n<thead>\n"+e+"</thead>\n"+t+"</table>\n"},s.prototype.tablerow=function(e){return"<tr>\n"+e+"</tr>\n"},s.prototype.tablecell=function(e,t){var n=t.header?"th":"td";return(t.align?"<"+n+' align="'+t.align+'">':"<"+n+">")+e+"</"+n+">\n"},s.prototype.strong=function(e){return"<strong>"+e+"</strong>"},s.prototype.em=function(e){return"<em>"+e+"</em>"},s.prototype.codespan=function(e){return"<code>"+e+"</code>"},s.prototype.br=function(){return this.options.xhtml?"<br/>":"<br>"},s.prototype.del=function(e){return"<del>"+e+"</del>"},s.prototype.link=function(e,t,n){if(this.options.sanitize){try{var r=decodeURIComponent(l(e)).replace(/[^\w:]/g,"").toLowerCase()}catch(e){return n}if(0===r.indexOf("javascript:")||0===r.indexOf("vbscript:")||0===r.indexOf("data:"))return n}this.options.baseUrl&&!v.test(e)&&(e=u(this.options.baseUrl,e));try{e=encodeURI(e).replace(/%25/g,"%")}catch(e){return n}var s='<a href="'+o(e)+'"';return t&&(s+=' title="'+t+'"'),s+=">"+n+"</a>"},s.prototype.image=function(e,t,n){this.options.baseUrl&&!v.test(e)&&(e=u(this.options.baseUrl,e));var r='<img src="'+e+'" alt="'+n+'"';return t&&(r+=' title="'+t+'"'),r+=this.options.xhtml?"/>":">"},s.prototype.text=function(e){return e},i.prototype.strong=i.prototype.em=i.prototype.codespan=i.prototype.del=i.prototype.text=function(e){return e},i.prototype.link=i.prototype.image=function(e,t,n){return""+n},i.prototype.br=function(){return""},a.parse=function(e,t){return new a(t).parse(e)},a.prototype.parse=function(e){this.inline=new r(e.links,this.options),this.inlineText=new r(e.links,p({},this.options,{renderer:new i})),this.tokens=e.reverse();for(var t="";this.next();)t+=this.tok();return t},a.prototype.next=function(){return this.token=this.tokens.pop()},a.prototype.peek=function(){return this.tokens[this.tokens.length-1]||0},a.prototype.parseText=function(){for(var e=this.token.text;"text"===this.peek().type;)e+="\n"+this.next().text;return this.inline.output(e)},a.prototype.tok=function(){switch(this.token.type){case"space":return"";case"hr":return this.renderer.hr();case"heading":return this.renderer.heading(this.inline.output(this.token.text),this.token.depth,l(this.inlineText.output(this.token.text)));case"code":return this.renderer.code(this.token.text,this.token.lang,this.token.escaped);case"table":var e,t,n,r,s="",i="";for(n="",e=0;e<this.token.header.length;e++)n+=this.renderer.tablecell(this.inline.output(this.token.header[e]),{header:!0,align:this.token.align[e]});for(s+=this.renderer.tablerow(n),e=0;e<this.token.cells.length;e++){for(t=this.token.cells[e],n="",r=0;r<t.length;r++)n+=this.renderer.tablecell(this.inline.output(t[r]),{header:!1,align:this.token.align[r]});i+=this.renderer.tablerow(n)}return this.renderer.table(s,i);case"blockquote_start":for(i="";"blockquote_end"!==this.next().type;)i+=this.tok();return this.renderer.blockquote(i);case"list_start":i="";for(var a=this.token.ordered,o=this.token.start;"list_end"!==this.next().type;)i+=this.tok();return this.renderer.list(i,a,o);case"list_item_start":for(i="",this.token.task&&(i+=this.renderer.checkbox(this.token.checked));"list_item_end"!==this.next().type;)i+="text"===this.token.type?this.parseText():this.tok();return this.renderer.listitem(i);case"loose_item_start":for(i="";"list_item_end"!==this.next().type;)i+=this.tok();return this.renderer.listitem(i);case"html":return this.renderer.html(this.token.text);case"paragraph":return this.renderer.paragraph(this.inline.output(this.token.text));case"text":return this.renderer.paragraph(this.parseText())}};var b={},v=/^$|^[a-z][a-z0-9+.-]*:|^[?#]/i;h.exec=h,m.options=m.setOptions=function(e){return p(m.defaults,e),m},m.getDefaults=function(){return{baseUrl:null,breaks:!1,gfm:!0,headerIds:!0,headerPrefix:"",highlight:null,langPrefix:"language-",mangle:!0,pedantic:!1,renderer:new s,sanitize:!1,sanitizer:null,silent:!1,smartLists:!1,smartypants:!1,tables:!0,xhtml:!1}},m.defaults=m.getDefaults(),m.Parser=a,m.parser=a.parse,m.Renderer=s,m.TextRenderer=i,m.Lexer=n,m.lexer=n.lex,m.InlineLexer=r,m.inlineLexer=r.output,m.parse=m,e.exports=m}(this||"undefined"!=typeof window&&window)}).call(t,n("DuR2"))},GwPc:function(e,t,n){"use strict";var r=n("EFqf"),s=n.n(r);s.a.setOptions({renderer:new s.a.Renderer,gfm:!0,tables:!0,breaks:!0,pedantic:!1,sanitize:!1,smartLists:!0,smartypants:!1});var i=new s.a.Renderer,a=function(e){return"<p>\n"+e+"</p>"},o=function(e,t,n){var r=e.includes("readup.tips"),s=n.includes("<img");return('<a href="'+e+'" target="_blank"\n             title="'+(t||(s?e:n))+'" \n             '+(r?"":'rel="external nofollow noopener noreferrer"')+">\n             "+n+"</a>").replace(/\s+/g," ").replace("\n","")},l=function(e,t,n){return('<a href="'+e+'" \n             target="_blank" rel="nofollow noopener noreferrer">\n            <img src="'+e+'" \n                referrerPolicy="no-referrer" \n                title="'+(t||n||"readup.tips")+'" \n                style="width:10%; height:15%"\n                alt="'+(n||t||e)+'"/>\n          </a>').replace(/\s+/g," ").replace("\n","")},c=function(e,t,n){var r=t+2;return"<h"+r+">"+e+"</h"+r+">\n"};i.link=o,i.image=l,i.paragraph=a,i.heading=c,t.a=function(e){return"string"!=typeof e?"":s()(e,{renderer:i})}},HJfm:function(e,t,n){"use strict";n.d(t,"d",function(){return r}),n.d(t,"a",function(){return s}),n.d(t,"b",function(){return i}),n.d(t,"c",function(){return a}),n.d(t,"e",function(){return o});var r=/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[#@!~%^$&*-])[a-zA-Z\d#@!~%^$&*-]{6,18}$/,s=/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/,i=/^[a-z][0-9a-z_]{2,19}$/,a=/^\w{2,20}$/,o=/[\n|\r|\s]#(\w+)/g},JAFF:function(e,t,n){"use strict";function r(e){n("2Xs0")}var s=n("+lgA"),i=n("80WQ"),a=n("XyMi"),o=r,l=Object(a.a)(s.a,i.a,i.b,!1,o,"data-v-d24ae332",null);t.a=l.exports},"L1/O":function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return s});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{directives:[{name:"show",rawName:"v-show",value:e.show,expression:"show"}],staticClass:"reply"},[n("el-form",{ref:"commentForm",attrs:{model:e.commentForm,rules:e.rules}},[n("el-form-item",{staticStyle:{"margin-bottom":"4px"},attrs:{prop:"comment"}},[n("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"Post a Comment"},model:{value:e.commentForm.comment,callback:function(t){e.$set(e.commentForm,"comment",t)},expression:"commentForm.comment"}})],1),e._v(" "),n("el-form-item",[n("el-button",{attrs:{size:"mini",disabled:!e.commentForm.comment.trim()},on:{click:function(t){e.reply("commentForm",e.commentForm)}}},[e._v("\n                 Submit\n      ")])],1)],1)],1)},s=[]},LUaW:function(e,t,n){var r=n("XQaa");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);var s=n("rjj0").default;s("1e428ae5",r,!0,{})},Nucc:function(e,t,n){"use strict";var r=n("kRrK"),s=n("GwPc"),i=n("iF09"),a=n("P9l9"),o=n("HJfm");t.a={name:"comment",props:["comment"],components:{Reply:r.a},data:function(){return{showRe:!1,hasChild:this.comment.children.length>0,childComments:this.comment.children,commentid:this.comment.id,refer:{re:"comment",id:this.comment.id}}},computed:{creator:function(){return this.comment.creator},commentContent:function(){return Object(s.a)(this.comment.body).replace(o.e,' <a href="/tag/$1"><small>#$1</small></a>')}},methods:{upComment:function(){Object(i.a)()&&Object(a._47)(this.comment.id)},updateNew:function(e){this.childComments.unshift(e)}}}},OjYV:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".demand-main[data-v-d24ae332]{padding:10px;background-color:#f8f9fa;border-bottom:1px dashed #ddd}.demand-main .demand-body a[data-v-d24ae332]:hover{color:#409eff}.demand-main .demand-bar[data-v-d24ae332]{font-size:12px}",""])},P1Nl:function(e,t,n){var r=n("YfKu");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);var s=n("rjj0").default;s("54e60262",r,!0,{})},UZ7o:function(e,t,n){"use strict";var r=n("Gu7T"),s=n.n(r),i=n("JAFF"),a=n("reXA"),o=n("kRrK"),l=n("ZCVe"),c=n("P9l9"),u=n("iF09");t.a={name:"demand-view",title:function(){return this.demandDetail.body},components:{Demand:i.a,Comment:a.a,Reply:o.a,ShareBar:l.a},data:function(){return{refer:{re:"demand",id:this.$route.params.id},demandDetail:{},answers:[],answerCount:0,currentaPage:1,comments:[],commentCount:0,currentPage:1,showDialog:!1,asForm:{selectRutID:null},createdRuts:[]}},computed:{hasMoreComment:function(){return this.comments.length<this.commentCount},hasMoreAnswer:function(){return this.answers.length<this.answerCount}},methods:{loadDemandData:function(){var e=this,t=this.$route.params.id;this.$store.dispatch("getDemand",t).then(function(t){var n=t.data;e.demandDetail=n,e.answers=n.answers,e.answerCount=n.answercount,e.comments=n.comments,e.commentCount=n.commentcount})},updateNew:function(e){this.comments.unshift(e)},loadmoreComment:function(){var e=this,t={page:this.currentPage};Object(c.K)(this.demandDetail.id,t).then(function(t){var n;(n=e.comments).push.apply(n,s()(t.data)),e.currentPage+=1})},loadmoreAnswer:function(){var e=this,t={page:this.currentaPage};Object(c.J)(this.demandDetail.id,t).then(function(t){var n;(n=e.answers).push.apply(n,s()(t.data)),e.currentaPage+=1})},loadCreatedThenAsAnswer:function(){var e=this;if(Object(u.a)()){var t=this.$store.getters.currentUserID;Object(c._2)("created",t).then(function(t){e.createdRuts=t.data.ruts,e.showDialog=!0})}else this.showDialog=!1,this.$message({showClose:!0,message:"Should Log in to Access"}),this.$router.push({path:"/login",query:{redirect:this.$route.fullPath}})},asAnswer:function(e,t){var n=this;if(!t.selectRutID)return this.$message({showClose:!0,message:"Please Select One"}),!1;this.$refs[e].validate(function(e){if(e&&Object(u.a)()){var r=t.selectRutID,s=n.demandDetail.id;Object(c._39)(r,s).then(function(e){e.data&&(n.showDialog=!1,n.answers.push(e.data)),n.$message({showClose:!0,message:e.data?"Done":"Up To 6"})})}else Object(u.a)()||(n.showDialog=!1,n.$message({showClose:!0,message:"Should Log in to Continue"}),n.$router.push({path:"/login",query:{redirect:n.$route.fullPath}}))})}},created:function(){this.loadDemandData()}}},"Ws/S":function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return s});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{attrs:{id:"social-share-bar"}},[n("a",{staticClass:"share-link twitter",attrs:{title:"Twitter",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://twitter.com/share?text="+e.title()+"&url="+e.url)}}},[n("img",{staticClass:"icon",attrs:{alt:"TW",src:"/static/pic/twitter.svg"}})]),e._v(" "),n("a",{staticClass:"share-link facebook",attrs:{title:"Facebook",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://www.facebook.com/sharer/sharer.php?u="+e.url)}}},[n("img",{staticClass:"icon",attrs:{alt:"FB",src:"/static/pic/facebook.svg"}})]),e._v(" "),n("a",{staticClass:"share-link linkedin",attrs:{title:"Linkedin",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://www.linkedin.com/shareArticle?mini=true&url="+e.url+"&title="+e.title())}}},[n("img",{staticClass:"icon",attrs:{alt:"Linkedin",src:"/static/pic/linkedin.svg"}})]),e._v(" "),n("a",{staticClass:"share-link google-plus",attrs:{title:"Google+",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://plus.google.com/share?url="+e.url)}}},[n("img",{staticClass:"icon",attrs:{alt:"G+",src:"/static/pic/gplus.svg"}})]),e._v(" "),n("a",{staticClass:"share-link evernote",attrs:{title:"Evernote",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://www.evernote.com/clip.action?url="+e.url+"&title="+e.title())}}},[n("img",{staticClass:"icon",attrs:{alt:"Evernote",src:"/static/pic/evernote.svg"}})])])},s=[]},XQaa:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".comment-view[data-v-0e9c510c]{background-color:#fcfcfb;border-top:1px dashed #ddd;padding:5px 2px 5px 5px;position:relative}.comment-view .avatar[data-v-0e9c510c]{position:absolute;top:20px;left:2px}.comment-view .comment[data-v-0e9c510c]{padding:5px}.comment-view .comment .by[data-v-0e9c510c]{font-size:10px;margin:2px 0;color:#bbb}.comment-view .comment .by a[data-v-0e9c510c]{color:#828282;text-decoration:underline}.comment-view .comment .content[data-v-0e9c510c]{margin:.2em 0}.comment-view .comment .content a[data-v-0e9c510c]:hover{color:#f60}.comment-view .comment .comment-children[data-v-0e9c510c]{margin-left:.5em;border-left:.5px solid #eee}",""])},YfKu:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".reply[data-v-77e97f9a]{padding:5px 0}",""])},Yhyb:function(e,t,n){"use strict";function r(e){n("1ngo")}Object.defineProperty(t,"__esModule",{value:!0});var s=n("UZ7o"),i=n("o0vY"),a=n("XyMi"),o=r,l=Object(a.a)(s.a,i.a,i.b,!1,o,"data-v-cd8ddbc0",null);t.default=l.exports},ZCVe:function(e,t,n){"use strict";function r(e){n("+rdc")}var s=n("r8Lr"),i=n("Ws/S"),a=n("XyMi"),o=r,l=Object(a.a)(s.a,i.a,i.b,!1,o,"data-v-755a1738",null);t.a=l.exports},dn1P:function(e,t,n){"use strict";var r=n("P9l9"),s=n("iF09");t.a={name:"reply",props:{refer:Object,tagsuf:{type:String,default:""},show:{default:!1}},data:function(){return{commentForm:{comment:""},rules:{comment:[{min:1,max:500,message:"Required, Max 500 Characters",trigger:"blur"}]}}},methods:{reply:function(e,t){var n=this;this.$refs[e].validate(function(i){if(i&&t.comment.trim()&&Object(s.a)()){var a={comment:t.comment.trim()+n.tagsuf},o=n.refer.re,l=n.refer.id;Object(r._26)(o,l,a).then(function(e){n.$emit("newreply",e.data)}),n.resetForm(e),n.$emit("update:show",!1)}else Object(s.a)()||(n.$message({showClose:!0,message:"Should Log in to post Comment"}),n.$router.push({path:"/login",query:{redirect:n.$route.fullPath}}))})},resetForm:function(e){this.$refs[e].resetFields()}}}},kRrK:function(e,t,n){"use strict";function r(e){n("P1Nl")}var s=n("dn1P"),i=n("L1/O"),a=n("XyMi"),o=r,l=Object(a.a)(s.a,i.a,i.b,!1,o,"data-v-77e97f9a",null);t.a=l.exports},o0vY:function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return s});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"demand-page"},[n("div",{staticClass:"demand-main"},[n("demand",{key:e.demandDetail.id,attrs:{demand:e.demandDetail}}),e._v(" "),n("div",{staticClass:"answer"},[n("b",{staticStyle:{"font-size":"12px"}},[e._v("Answers to This Demand:")]),e._v(" "),n("el-button",{attrs:{size:"mini",type:"text"},on:{click:e.loadCreatedThenAsAnswer}},[e._v("\n                 ...Link To Answer\n      ")]),e._v(" "),e._l(e.answers,function(t,r){return n("div",{key:r,staticClass:"title",attrs:{rut:t}},[e._v(" - \n           "),n("router-link",{attrs:{to:"/readlist/"+t.id,title:t.title}},[e._v("\n             "+e._s(t.title.slice(0,142))+" ...\n           ")])],1)}),e._v(" "),e.hasMoreAnswer?n("div",[n("el-button",{attrs:{size:"mini",disabled:!e.hasMoreAnswer},on:{click:e.loadmoreAnswer}},[e._v("\n                   Show More\n        ")])],1):e._e()],2),e._v(" "),n("div",{staticClass:"share"},[n("share-bar",{attrs:{prefix:"Would you like answer this question:  "}})],1),e._v(" "),n("el-dialog",{attrs:{title:"Link A list as Answer",width:"480px",visible:e.showDialog},on:{"update:visible":function(t){e.showDialog=t}}},[n("el-form",{ref:"asForm",attrs:{model:e.asForm}},[n("el-form-item",{attrs:{prop:"rut"}},[n("el-select",{model:{value:e.asForm.selectRutID,callback:function(t){e.$set(e.asForm,"selectRutID",t)},expression:"asForm.selectRutID"}},e._l(e.createdRuts,function(e){return n("el-option",{key:e.id,attrs:{label:e.title,value:e.id}})}))],1)],1),e._v(" "),n("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{attrs:{size:"mini",type:"success"},on:{click:function(t){e.asAnswer("asForm",e.asForm)}}},[e._v("\n          As Answer\n        ")])],1)],1),e._v(" "),e._l(e.comments,function(e){return n("div",{key:e.id},[n("comment",{attrs:{comment:e}})],1)}),e._v(" "),e.hasMoreComment?n("div",[n("el-button",{staticClass:"blockbtn",attrs:{size:"mini",disabled:!e.hasMoreComment},on:{click:e.loadmoreComment}},[e._v("\n                 Show More Comments\n      ")])],1):e._e(),e._v(" "),n("div",{staticClass:"comment"},[n("reply",{staticClass:"reply",attrs:{refer:e.refer,show:!0},on:{newreply:e.updateNew}})],1)],2),e._v(" "),n("div",{staticClass:"demand-side"})])},s=[]},r8Lr:function(e,t,n){"use strict";t.a={name:"share-bar",props:{passUrl:String,passTitle:String,prefix:{type:String,default:""}},computed:{url:function(){return this.passUrl||"https://readup.tips"+this.$route.fullPath}},methods:{title:function(){try{if(document)return this.prefix+(this.passTitle||document.title)}catch(e){return"Readup.Tips"}},shareWindow:function(e){e=encodeURI(e),console.log(e);var t=screen.availWidth/2,n=screen.availHeight/5*2,r=(screen.availHeight-n)/2,s=(screen.availWidth-t)/2,i="top="+r+",left="+s+",width="+t+",height="+n+",scrollbars=0,status=0,menubar=0,resizable=2,location=0";window.open(e,"newWin",i).focus()}}}},reXA:function(e,t,n){"use strict";function r(e){n("LUaW")}var s=n("Nucc"),i=n("5zb4"),a=n("XyMi"),o=r,l=Object(a.a)(s.a,i.a,i.b,!1,o,"data-v-0e9c510c",null);t.a=l.exports},uGMt:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".demand-page[data-v-cd8ddbc0]{padding:10px 260px 10px 0;position:relative}.demand-page .demand-main .answer[data-v-cd8ddbc0]{background-color:#f7f8fa;padding:5px 10px;margin-bottom:5px}.demand-page .demand-main .answer .title a[data-v-cd8ddbc0]:hover{color:#f60}.demand-page .demand-side[data-v-cd8ddbc0]{position:absolute;top:10px;right:0;width:240px}.el-select[data-v-cd8ddbc0]{width:100%}",""])},wmsc:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,"#social-share-bar[data-v-755a1738]{text-align:right}#social-share-bar>.share-link[data-v-755a1738]{cursor:pointer;display:inline-block;text-align:center}#social-share-bar>.share-link.evernote[data-v-755a1738]:hover{background-color:#8be056}#social-share-bar>.share-link.twitter[data-v-755a1738]:hover{background-color:#55acee}#social-share-bar>.share-link.facebook[data-v-755a1738]:hover{background-color:#3b5998}#social-share-bar>.share-link.google-plus[data-v-755a1738]:hover{background-color:#dd4b39}#social-share-bar>.share-link.linkedin[data-v-755a1738]:hover{background-color:#007bb5}#social-share-bar>.share-link .icon[data-v-755a1738]{padding:5px;width:16px;height:16px}",""])}});
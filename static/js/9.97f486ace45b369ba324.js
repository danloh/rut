webpackJsonp([9],{"0VnM":function(e,t,n){var r=n("p+vJ");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);var s=n("rjj0").default;s("12c7e17c",r,!0,{})},B88Q:function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return s});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("transition",[n("svg",{directives:[{name:"show",rawName:"v-show",value:e.show,expression:"show"}],staticClass:"spinner",class:{show:e.show},attrs:{width:"44px",height:"44px",viewBox:"0 0 44 44"}},[n("circle",{staticClass:"path",attrs:{fill:"none","stroke-width":"4","stroke-linecap":"round",cx:"22",cy:"22",r:"20"}})])])},s=[]},D3Jz:function(e,t,n){"use strict";var r=n("6aq2"),s=n("GwPc");t.a={name:"rut-sum",props:["rut"],computed:{cover:function(){return this.rut.cover},intro:function(){var e=Object(s.a)(this.rut.intro);return Object(r.showLess)(e)}}}},DkQ0:function(e,t,n){"use strict";var r=n("Dd8w"),s=n.n(r),i=n("haTO"),a=n("cgFa"),o=n("P9l9"),l=n("NYxO");t.a={name:"home",title:"Share ReadList or RoadMaps To Readers",components:{RutSum:a.a,Spinner:i.a},data:function(){return{loading:!0}},computed:s()({},Object(l.b)(["indexRuts","showTags"])),methods:{loadIndex:function(){var e=this,t=this.$store.getters.indexRuts;this.loading=!0,0!==t.length?this.loading=!1:Object(o.R)().then(function(t){e.$store.commit("SET_INDEX",t.data),e.loading=!1})}},created:function(){this.loadIndex()}}},EFqf:function(e,t,n){(function(t){!function(t){"use strict";function n(e){this.tokens=[],this.tokens.links={},this.options=e||g.defaults,this.rules=d.normal,this.options.gfm&&(this.options.tables?this.rules=d.tables:this.rules=d.gfm)}function r(e,t){if(this.options=t||g.defaults,this.links=e,this.rules=f.normal,this.renderer=this.options.renderer||new s,this.renderer.options=this.options,!this.links)throw new Error("Tokens array requires a `links` property.");this.options.gfm?this.options.breaks?this.rules=f.breaks:this.rules=f.gfm:this.options.pedantic&&(this.rules=f.pedantic)}function s(e){this.options=e||{}}function i(){}function a(e){this.tokens=[],this.token=null,this.options=e||g.defaults,this.options.renderer=this.options.renderer||new s,this.renderer=this.options.renderer,this.renderer.options=this.options}function o(e,t){return e.replace(t?/&/g:/&(?!#?\w+;)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}function l(e){return e.replace(/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/gi,function(e,t){return t=t.toLowerCase(),"colon"===t?":":"#"===t.charAt(0)?"x"===t.charAt(1)?String.fromCharCode(parseInt(t.substring(2),16)):String.fromCharCode(+t.substring(1)):""})}function p(e,t){return e=e.source,t=t||"",{replace:function(t,n){return n=n.source||n,n=n.replace(/(^|[^\[])\^/g,"$1"),e=e.replace(t,n),this},getRegex:function(){return new RegExp(e,t)}}}function h(e,t){return m[" "+e]||(/^[^:]+:\/*[^\/]*$/.test(e)?m[" "+e]=e+"/":m[" "+e]=e.replace(/[^\/]*$/,"")),e=m[" "+e],"//"===t.slice(0,2)?e.replace(/:[\s\S]*/,":")+t:"/"===t.charAt(0)?e.replace(/(:\/*[^\/]*)[\s\S]*/,"$1")+t:e+t}function u(){}function c(e){for(var t,n,r=1;r<arguments.length;r++){t=arguments[r];for(n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e}function g(e,t,r){if(void 0===e||null===e)throw new Error("marked(): input parameter is undefined or null");if("string"!=typeof e)throw new Error("marked(): input parameter is of type "+Object.prototype.toString.call(e)+", string expected");if(r||"function"==typeof t){r||(r=t,t=null),t=c({},g.defaults,t||{});var s,i,l=t.highlight,p=0;try{s=n.lex(e,t)}catch(e){return r(e)}i=s.length;var h=function(e){if(e)return t.highlight=l,r(e);var n;try{n=a.parse(s,t)}catch(t){e=t}return t.highlight=l,e?r(e):r(null,n)};if(!l||l.length<3)return h();if(delete t.highlight,!i)return h();for(;p<s.length;p++)!function(e){"code"!==e.type?--i||h():l(e.text,e.lang,function(t,n){return t?h(t):null==n||n===e.text?--i||h():(e.text=n,e.escaped=!0,void(--i||h()))})}(s[p])}else try{return t&&(t=c({},g.defaults,t)),a.parse(n.lex(e,t),t)}catch(e){if(e.message+="\nPlease report this to https://github.com/markedjs/marked.",(t||g.defaults).silent)return"<p>An error occurred:</p><pre>"+o(e.message+"",!0)+"</pre>";throw e}}var d={newline:/^\n+/,code:/^( {4}[^\n]+\n*)+/,fences:u,hr:/^ {0,3}((?:- *){3,}|(?:_ *){3,}|(?:\* *){3,})(?:\n+|$)/,heading:/^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)/,nptable:u,blockquote:/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/,list:/^( *)(bull) [\s\S]+?(?:hr|def|\n{2,}(?! )(?!\1bull )\n*|\s*$)/,html:/^ *(?:comment *(?:\n|\s*$)|closed *(?:\n{2,}|\s*$)|closing *(?:\n{2,}|\s*$))/,def:/^ {0,3}\[(label)\]: *\n? *<?([^\s>]+)>?(?:(?: +\n? *| *\n *)(title))? *(?:\n+|$)/,table:u,lheading:/^([^\n]+)\n *(=|-){2,} *(?:\n+|$)/,paragraph:/^([^\n]+(?:\n?(?!hr|heading|lheading| {0,3}>|tag)[^\n]+)+)/,text:/^[^\n]+/};d._label=/(?:\\[\[\]]|[^\[\]])+/,d._title=/(?:"(?:\\"|[^"]|"[^"\n]*")*"|'\n?(?:[^'\n]+\n?)*'|\([^()]*\))/,d.def=p(d.def).replace("label",d._label).replace("title",d._title).getRegex(),d.bullet=/(?:[*+-]|\d+\.)/,d.item=/^( *)(bull) [^\n]*(?:\n(?!\1bull )[^\n]*)*/,d.item=p(d.item,"gm").replace(/bull/g,d.bullet).getRegex(),d.list=p(d.list).replace(/bull/g,d.bullet).replace("hr","\\n+(?=\\1?(?:(?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$))").replace("def","\\n+(?="+d.def.source+")").getRegex(),d._tag="(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b",d.html=p(d.html).replace("comment",/<!--[\s\S]*?-->/).replace("closed",/<(tag)[\s\S]+?<\/\1>/).replace("closing",/<tag(?:"[^"]*"|'[^']*'|\s[^'"\/>\s]*)*?\/?>/).replace(/tag/g,d._tag).getRegex(),d.paragraph=p(d.paragraph).replace("hr",d.hr).replace("heading",d.heading).replace("lheading",d.lheading).replace("tag","<"+d._tag).getRegex(),d.blockquote=p(d.blockquote).replace("paragraph",d.paragraph).getRegex(),d.normal=c({},d),d.gfm=c({},d.normal,{fences:/^ *(`{3,}|~{3,})[ \.]*(\S+)? *\n([\s\S]*?)\n? *\1 *(?:\n+|$)/,paragraph:/^/,heading:/^ *(#{1,6}) +([^\n]+?) *#* *(?:\n+|$)/}),d.gfm.paragraph=p(d.paragraph).replace("(?!","(?!"+d.gfm.fences.source.replace("\\1","\\2")+"|"+d.list.source.replace("\\1","\\3")+"|").getRegex(),d.tables=c({},d.gfm,{nptable:/^ *(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)\n*/,table:/^ *\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*/}),n.rules=d,n.lex=function(e,t){return new n(t).lex(e)},n.prototype.lex=function(e){return e=e.replace(/\r\n|\r/g,"\n").replace(/\t/g,"    ").replace(/\u00a0/g," ").replace(/\u2424/g,"\n"),this.token(e,!0)},n.prototype.token=function(e,t){e=e.replace(/^ +$/gm,"");for(var n,r,s,i,a,o,l,p,h,u;e;)if((s=this.rules.newline.exec(e))&&(e=e.substring(s[0].length),s[0].length>1&&this.tokens.push({type:"space"})),s=this.rules.code.exec(e))e=e.substring(s[0].length),s=s[0].replace(/^ {4}/gm,""),this.tokens.push({type:"code",text:this.options.pedantic?s:s.replace(/\n+$/,"")});else if(s=this.rules.fences.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"code",lang:s[2],text:s[3]||""});else if(s=this.rules.heading.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"heading",depth:s[1].length,text:s[2]});else if(t&&(s=this.rules.nptable.exec(e))){for(e=e.substring(s[0].length),o={type:"table",header:s[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:s[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:s[3].replace(/\n$/,"").split("\n")},p=0;p<o.align.length;p++)/^ *-+: *$/.test(o.align[p])?o.align[p]="right":/^ *:-+: *$/.test(o.align[p])?o.align[p]="center":/^ *:-+ *$/.test(o.align[p])?o.align[p]="left":o.align[p]=null;for(p=0;p<o.cells.length;p++)o.cells[p]=o.cells[p].split(/ *\| */);this.tokens.push(o)}else if(s=this.rules.hr.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"hr"});else if(s=this.rules.blockquote.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"blockquote_start"}),s=s[0].replace(/^ *> ?/gm,""),this.token(s,t),this.tokens.push({type:"blockquote_end"});else if(s=this.rules.list.exec(e)){for(e=e.substring(s[0].length),i=s[2],this.tokens.push({type:"list_start",ordered:i.length>1}),s=s[0].match(this.rules.item),n=!1,u=s.length,p=0;p<u;p++)o=s[p],l=o.length,o=o.replace(/^ *([*+-]|\d+\.) +/,""),~o.indexOf("\n ")&&(l-=o.length,o=this.options.pedantic?o.replace(/^ {1,4}/gm,""):o.replace(new RegExp("^ {1,"+l+"}","gm"),"")),this.options.smartLists&&p!==u-1&&(a=d.bullet.exec(s[p+1])[0],i===a||i.length>1&&a.length>1||(e=s.slice(p+1).join("\n")+e,p=u-1)),r=n||/\n\n(?!\s*$)/.test(o),p!==u-1&&(n="\n"===o.charAt(o.length-1),r||(r=n)),this.tokens.push({type:r?"loose_item_start":"list_item_start"}),this.token(o,!1),this.tokens.push({type:"list_item_end"});this.tokens.push({type:"list_end"})}else if(s=this.rules.html.exec(e))e=e.substring(s[0].length),this.tokens.push({type:this.options.sanitize?"paragraph":"html",pre:!this.options.sanitizer&&("pre"===s[1]||"script"===s[1]||"style"===s[1]),text:s[0]});else if(t&&(s=this.rules.def.exec(e)))e=e.substring(s[0].length),s[3]&&(s[3]=s[3].substring(1,s[3].length-1)),h=s[1].toLowerCase(),this.tokens.links[h]||(this.tokens.links[h]={href:s[2],title:s[3]});else if(t&&(s=this.rules.table.exec(e))){for(e=e.substring(s[0].length),o={type:"table",header:s[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:s[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:s[3].replace(/(?: *\| *)?\n$/,"").split("\n")},p=0;p<o.align.length;p++)/^ *-+: *$/.test(o.align[p])?o.align[p]="right":/^ *:-+: *$/.test(o.align[p])?o.align[p]="center":/^ *:-+ *$/.test(o.align[p])?o.align[p]="left":o.align[p]=null;for(p=0;p<o.cells.length;p++)o.cells[p]=o.cells[p].replace(/^ *\| *| *\| *$/g,"").split(/ *\| */);this.tokens.push(o)}else if(s=this.rules.lheading.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"heading",depth:"="===s[2]?1:2,text:s[1]});else if(t&&(s=this.rules.paragraph.exec(e)))e=e.substring(s[0].length),this.tokens.push({type:"paragraph",text:"\n"===s[1].charAt(s[1].length-1)?s[1].slice(0,-1):s[1]});else if(s=this.rules.text.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"text",text:s[0]});else if(e)throw new Error("Infinite loop on byte: "+e.charCodeAt(0));return this.tokens};var f={escape:/^\\([\\`*{}\[\]()#+\-.!_>])/,autolink:/^<(scheme:[^\s\x00-\x1f<>]*|email)>/,url:u,tag:/^<!--[\s\S]*?-->|^<\/?[a-zA-Z0-9\-]+(?:"[^"]*"|'[^']*'|\s[^<'">\/\s]*)*?\/?>/,link:/^!?\[(inside)\]\(href\)/,reflink:/^!?\[(inside)\]\s*\[([^\]]*)\]/,nolink:/^!?\[((?:\[[^\[\]]*\]|\\[\[\]]|[^\[\]])*)\]/,strong:/^__([\s\S]+?)__(?!_)|^\*\*([\s\S]+?)\*\*(?!\*)/,em:/^_([^\s_](?:[^_]|__)+?[^\s_])_\b|^\*((?:\*\*|[^*])+?)\*(?!\*)/,code:/^(`+)\s*([\s\S]*?[^`]?)\s*\1(?!`)/,br:/^ {2,}\n(?!\s*$)/,del:u,text:/^[\s\S]+?(?=[\\<!\[`*]|\b_| {2,}\n|$)/};f._scheme=/[a-zA-Z][a-zA-Z0-9+.-]{1,31}/,f._email=/[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/,f.autolink=p(f.autolink).replace("scheme",f._scheme).replace("email",f._email).getRegex(),f._inside=/(?:\[[^\[\]]*\]|\\[\[\]]|[^\[\]]|\](?=[^\[]*\]))*/,f._href=/\s*<?([\s\S]*?)>?(?:\s+['"]([\s\S]*?)['"])?\s*/,f.link=p(f.link).replace("inside",f._inside).replace("href",f._href).getRegex(),f.reflink=p(f.reflink).replace("inside",f._inside).getRegex(),f.normal=c({},f),f.pedantic=c({},f.normal,{strong:/^__(?=\S)([\s\S]*?\S)__(?!_)|^\*\*(?=\S)([\s\S]*?\S)\*\*(?!\*)/,em:/^_(?=\S)([\s\S]*?\S)_(?!_)|^\*(?=\S)([\s\S]*?\S)\*(?!\*)/}),f.gfm=c({},f.normal,{escape:p(f.escape).replace("])","~|])").getRegex(),url:p(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/).replace("email",f._email).getRegex(),_backpedal:/(?:[^?!.,:;*_~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_~)]+(?!$))+/,del:/^~~(?=\S)([\s\S]*?\S)~~/,text:p(f.text).replace("]|","~]|").replace("|","|https?://|ftp://|www\\.|[a-zA-Z0-9.!#$%&'*+/=?^_`{\\|}~-]+@|").getRegex()}),f.breaks=c({},f.gfm,{br:p(f.br).replace("{2,}","*").getRegex(),text:p(f.gfm.text).replace("{2,}","*").getRegex()}),r.rules=f,r.output=function(e,t,n){return new r(t,n).output(e)},r.prototype.output=function(e){for(var t,n,r,s,i="";e;)if(s=this.rules.escape.exec(e))e=e.substring(s[0].length),i+=s[1];else if(s=this.rules.autolink.exec(e))e=e.substring(s[0].length),"@"===s[2]?(n=o(this.mangle(s[1])),r="mailto:"+n):(n=o(s[1]),r=n),i+=this.renderer.link(r,null,n);else if(this.inLink||!(s=this.rules.url.exec(e))){if(s=this.rules.tag.exec(e))!this.inLink&&/^<a /i.test(s[0])?this.inLink=!0:this.inLink&&/^<\/a>/i.test(s[0])&&(this.inLink=!1),e=e.substring(s[0].length),i+=this.options.sanitize?this.options.sanitizer?this.options.sanitizer(s[0]):o(s[0]):s[0];else if(s=this.rules.link.exec(e))e=e.substring(s[0].length),this.inLink=!0,i+=this.outputLink(s,{href:s[2],title:s[3]}),this.inLink=!1;else if((s=this.rules.reflink.exec(e))||(s=this.rules.nolink.exec(e))){if(e=e.substring(s[0].length),t=(s[2]||s[1]).replace(/\s+/g," "),!(t=this.links[t.toLowerCase()])||!t.href){i+=s[0].charAt(0),e=s[0].substring(1)+e;continue}this.inLink=!0,i+=this.outputLink(s,t),this.inLink=!1}else if(s=this.rules.strong.exec(e))e=e.substring(s[0].length),i+=this.renderer.strong(this.output(s[2]||s[1]));else if(s=this.rules.em.exec(e))e=e.substring(s[0].length),i+=this.renderer.em(this.output(s[2]||s[1]));else if(s=this.rules.code.exec(e))e=e.substring(s[0].length),i+=this.renderer.codespan(o(s[2].trim(),!0));else if(s=this.rules.br.exec(e))e=e.substring(s[0].length),i+=this.renderer.br();else if(s=this.rules.del.exec(e))e=e.substring(s[0].length),i+=this.renderer.del(this.output(s[1]));else if(s=this.rules.text.exec(e))e=e.substring(s[0].length),i+=this.renderer.text(o(this.smartypants(s[0])));else if(e)throw new Error("Infinite loop on byte: "+e.charCodeAt(0))}else s[0]=this.rules._backpedal.exec(s[0])[0],e=e.substring(s[0].length),"@"===s[2]?(n=o(s[0]),r="mailto:"+n):(n=o(s[0]),r="www."===s[1]?"http://"+n:n),i+=this.renderer.link(r,null,n);return i},r.prototype.outputLink=function(e,t){var n=o(t.href),r=t.title?o(t.title):null;return"!"!==e[0].charAt(0)?this.renderer.link(n,r,this.output(e[1])):this.renderer.image(n,r,o(e[1]))},r.prototype.smartypants=function(e){return this.options.smartypants?e.replace(/---/g,"—").replace(/--/g,"–").replace(/(^|[-\u2014\/(\[{"\s])'/g,"$1‘").replace(/'/g,"’").replace(/(^|[-\u2014\/(\[{\u2018\s])"/g,"$1“").replace(/"/g,"”").replace(/\.{3}/g,"…"):e},r.prototype.mangle=function(e){if(!this.options.mangle)return e;for(var t,n="",r=e.length,s=0;s<r;s++)t=e.charCodeAt(s),Math.random()>.5&&(t="x"+t.toString(16)),n+="&#"+t+";";return n},s.prototype.code=function(e,t,n){if(this.options.highlight){var r=this.options.highlight(e,t);null!=r&&r!==e&&(n=!0,e=r)}return t?'<pre><code class="'+this.options.langPrefix+o(t,!0)+'">'+(n?e:o(e,!0))+"\n</code></pre>\n":"<pre><code>"+(n?e:o(e,!0))+"\n</code></pre>"},s.prototype.blockquote=function(e){return"<blockquote>\n"+e+"</blockquote>\n"},s.prototype.html=function(e){return e},s.prototype.heading=function(e,t,n){return"<h"+t+' id="'+this.options.headerPrefix+n.toLowerCase().replace(/[^\w]+/g,"-")+'">'+e+"</h"+t+">\n"},s.prototype.hr=function(){return this.options.xhtml?"<hr/>\n":"<hr>\n"},s.prototype.list=function(e,t){var n=t?"ol":"ul";return"<"+n+">\n"+e+"</"+n+">\n"},s.prototype.listitem=function(e){return"<li>"+e+"</li>\n"},s.prototype.paragraph=function(e){return"<p>"+e+"</p>\n"},s.prototype.table=function(e,t){return"<table>\n<thead>\n"+e+"</thead>\n<tbody>\n"+t+"</tbody>\n</table>\n"},s.prototype.tablerow=function(e){return"<tr>\n"+e+"</tr>\n"},s.prototype.tablecell=function(e,t){var n=t.header?"th":"td";return(t.align?"<"+n+' style="text-align:'+t.align+'">':"<"+n+">")+e+"</"+n+">\n"},s.prototype.strong=function(e){return"<strong>"+e+"</strong>"},s.prototype.em=function(e){return"<em>"+e+"</em>"},s.prototype.codespan=function(e){return"<code>"+e+"</code>"},s.prototype.br=function(){return this.options.xhtml?"<br/>":"<br>"},s.prototype.del=function(e){return"<del>"+e+"</del>"},s.prototype.link=function(e,t,n){if(this.options.sanitize){try{var r=decodeURIComponent(l(e)).replace(/[^\w:]/g,"").toLowerCase()}catch(e){return n}if(0===r.indexOf("javascript:")||0===r.indexOf("vbscript:")||0===r.indexOf("data:"))return n}this.options.baseUrl&&!k.test(e)&&(e=h(this.options.baseUrl,e));var s='<a href="'+e+'"';return t&&(s+=' title="'+t+'"'),s+=">"+n+"</a>"},s.prototype.image=function(e,t,n){this.options.baseUrl&&!k.test(e)&&(e=h(this.options.baseUrl,e));var r='<img src="'+e+'" alt="'+n+'"';return t&&(r+=' title="'+t+'"'),r+=this.options.xhtml?"/>":">"},s.prototype.text=function(e){return e},i.prototype.strong=i.prototype.em=i.prototype.codespan=i.prototype.del=i.prototype.text=function(e){return e},i.prototype.link=i.prototype.image=function(e,t,n){return""+n},i.prototype.br=function(){return""},a.parse=function(e,t){return new a(t).parse(e)},a.prototype.parse=function(e){this.inline=new r(e.links,this.options),this.inlineText=new r(e.links,c({},this.options,{renderer:new i})),this.tokens=e.reverse();for(var t="";this.next();)t+=this.tok();return t},a.prototype.next=function(){return this.token=this.tokens.pop()},a.prototype.peek=function(){return this.tokens[this.tokens.length-1]||0},a.prototype.parseText=function(){for(var e=this.token.text;"text"===this.peek().type;)e+="\n"+this.next().text;return this.inline.output(e)},a.prototype.tok=function(){switch(this.token.type){case"space":return"";case"hr":return this.renderer.hr();case"heading":return this.renderer.heading(this.inline.output(this.token.text),this.token.depth,l(this.inlineText.output(this.token.text)));case"code":return this.renderer.code(this.token.text,this.token.lang,this.token.escaped);case"table":var e,t,n,r,s="",i="";for(n="",e=0;e<this.token.header.length;e++)n+=this.renderer.tablecell(this.inline.output(this.token.header[e]),{header:!0,align:this.token.align[e]});for(s+=this.renderer.tablerow(n),e=0;e<this.token.cells.length;e++){for(t=this.token.cells[e],n="",r=0;r<t.length;r++)n+=this.renderer.tablecell(this.inline.output(t[r]),{header:!1,align:this.token.align[r]});i+=this.renderer.tablerow(n)}return this.renderer.table(s,i);case"blockquote_start":for(i="";"blockquote_end"!==this.next().type;)i+=this.tok();return this.renderer.blockquote(i);case"list_start":i="";for(var a=this.token.ordered;"list_end"!==this.next().type;)i+=this.tok();return this.renderer.list(i,a);case"list_item_start":for(i="";"list_item_end"!==this.next().type;)i+="text"===this.token.type?this.parseText():this.tok();return this.renderer.listitem(i);case"loose_item_start":for(i="";"list_item_end"!==this.next().type;)i+=this.tok();return this.renderer.listitem(i);case"html":var o=this.token.pre||this.options.pedantic?this.token.text:this.inline.output(this.token.text);return this.renderer.html(o);case"paragraph":return this.renderer.paragraph(this.inline.output(this.token.text));case"text":return this.renderer.paragraph(this.parseText())}};var m={},k=/^$|^[a-z][a-z0-9+.-]*:|^[?#]/i;u.exec=u,g.options=g.setOptions=function(e){return c(g.defaults,e),g},g.defaults={gfm:!0,tables:!0,breaks:!1,pedantic:!1,sanitize:!1,sanitizer:null,mangle:!0,smartLists:!1,silent:!1,highlight:null,langPrefix:"lang-",smartypants:!1,headerPrefix:"",renderer:new s,xhtml:!1,baseUrl:null},g.Parser=a,g.parser=a.parse,g.Renderer=s,g.TextRenderer=i,g.Lexer=n,g.lexer=n.lex,g.InlineLexer=r,g.inlineLexer=r.output,g.parse=g,e.exports=g}(this||"undefined"!=typeof window&&window)}).call(t,n("DuR2"))},GwPc:function(e,t,n){"use strict";var r=n("EFqf"),s=n.n(r);s.a.setOptions({renderer:new s.a.Renderer,gfm:!0,tables:!0,breaks:!0,pedantic:!1,sanitize:!1,smartLists:!0,smartypants:!1});var i=new s.a.Renderer,a=function(e){return"<p>"+e+"</p>"},o=function(e,t,n){var r=e.includes("readup.tips"),s=n.includes("<img");return('<a href="'+e+'" \n             target="_blank"\n             title="'+(t||(s?e:n))+'" \n             '+(r?"":'rel="external nofollow noopener noreferrer"')+">"+n+"\n          </a>").replace(/\s+/g," ").replace("\n","")},l=function(e,t,n){return('<a href="'+e+'" \n             target="_blank" rel="nofollow noopener noreferrer">\n            <img src="'+e+'" \n                title="'+(t||n||"readup.tips")+'" \n                style="width:10%; height:15%"\n                alt="'+(n||t||e)+'"/>\n          </a>').replace(/\s+/g," ").replace("\n","")};i.link=o,i.image=l,i.paragraph=a,t.a=function(e){return"string"!=typeof e?"":s()(e,{renderer:i})}},HTl0:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".spinner[data-v-4e64c895]{-webkit-transition:opacity .15s ease;transition:opacity .15s ease;-webkit-animation:rotator-data-v-4e64c895 1.4s linear infinite;animation:rotator-data-v-4e64c895 1.4s linear infinite;-webkit-animation-play-state:paused;animation-play-state:paused}.spinner.show[data-v-4e64c895]{-webkit-animation-play-state:running;animation-play-state:running}.spinner.v-enter[data-v-4e64c895],.spinner.v-leave-active[data-v-4e64c895]{opacity:0}.spinner.v-enter-active[data-v-4e64c895],.spinner.v-leave[data-v-4e64c895]{opacity:1}.spinner .path[data-v-4e64c895]{stroke:#f60;stroke-dasharray:126;stroke-dashoffset:0;-webkit-transform-origin:center;transform-origin:center;-webkit-animation:dash-data-v-4e64c895 1.4s ease-in-out infinite;animation:dash-data-v-4e64c895 1.4s ease-in-out infinite}@-webkit-keyframes rotator-data-v-4e64c895{0%{-webkit-transform:scale(.5) rotate(0deg);transform:scale(.5) rotate(0deg)}to{-webkit-transform:scale(.5) rotate(270deg);transform:scale(.5) rotate(270deg)}}@keyframes rotator-data-v-4e64c895{0%{-webkit-transform:scale(.5) rotate(0deg);transform:scale(.5) rotate(0deg)}to{-webkit-transform:scale(.5) rotate(270deg);transform:scale(.5) rotate(270deg)}}@-webkit-keyframes dash-data-v-4e64c895{0%{stroke-dashoffset:126}50%{stroke-dashoffset:63;-webkit-transform:rotate(135deg);transform:rotate(135deg)}to{stroke-dashoffset:126;-webkit-transform:rotate(450deg);transform:rotate(450deg)}}@keyframes dash-data-v-4e64c895{0%{stroke-dashoffset:126}50%{stroke-dashoffset:63;-webkit-transform:rotate(135deg);transform:rotate(135deg)}to{stroke-dashoffset:126;-webkit-transform:rotate(450deg);transform:rotate(450deg)}}",""])},"Irp/":function(e,t,n){"use strict";function r(e){n("0VnM")}Object.defineProperty(t,"__esModule",{value:!0});var s=n("DkQ0"),i=n("qhZt"),a=n("XyMi"),o=r,l=Object(a.a)(s.a,i.a,i.b,!1,o,"data-v-7d1e7f11",null);t.default=l.exports},WU1C:function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return s});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"rut-sum"},[n("router-link",{attrs:{to:"/readuplist/"+e.rut.id}},[n("span",[n("img",{staticClass:"cover",staticStyle:{width:"80px",height:"100px"},attrs:{src:e.cover,alt:"Cover"}})]),e._v(" "),n("span",{staticClass:"title"},[n("router-link",{attrs:{to:"/readuplist/"+e.rut.id}},[e._v(" "+e._s(e.rut.title))])],1),e._v(" "),n("div",{staticClass:"intro",domProps:{innerHTML:e._s(e.intro)}})]),e._v(" "),n("span",{staticClass:"meta"},[n("span",[e._v("  including "+e._s(e._f("pluralise")(e.rut.itemcount,"item"))+"  \n            | "),n("router-link",{attrs:{to:"/readuplist/"+e.rut.id}},[e._v("...See Detail")])],1)])],1)},s=[]},YBlJ:function(e,t,n){var r=n("HTl0");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);var s=n("rjj0").default;s("965f2890",r,!0,{})},Yl6R:function(e,t,n){"use strict";t.a={name:"spinner",props:["show"]}},bgTS:function(e,t,n){var r=n("zcFI");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);var s=n("rjj0").default;s("d48922c2",r,!0,{})},cgFa:function(e,t,n){"use strict";function r(e){n("bgTS")}var s=n("D3Jz"),i=n("WU1C"),a=n("XyMi"),o=r,l=Object(a.a)(s.a,i.a,i.b,!1,o,"data-v-54777a0e",null);t.a=l.exports},haTO:function(e,t,n){"use strict";function r(e){n("YBlJ")}var s=n("Yl6R"),i=n("B88Q"),a=n("XyMi"),o=r,l=Object(a.a)(s.a,i.a,i.b,!1,o,"data-v-4e64c895",null);t.a=l.exports},"p+vJ":function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".home-page[data-v-7d1e7f11]{padding:10px 230px 10px 0;position:relative}.home-page .rut-list[data-v-7d1e7f11]{padding:auto}.home-page .home-side[data-v-7d1e7f11]{position:absolute;top:10px;right:0;width:220px;background-color:#fafbfa}.home-page .home-side .right-title[data-v-7d1e7f11]{background-color:#e5ebe4;padding:10px 15px}.home-page .home-side .right-body[data-v-7d1e7f11]{padding:5px 20px}.home-page .home-side .right-body a[data-v-7d1e7f11]:hover{color:#f60}",""])},qhZt:function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return s});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("div",{staticClass:"home-page"},[n("div",{staticClass:"rut-list"},e._l(e.indexRuts,function(e){return n("rut-sum",{key:e.id,attrs:{rut:e}})})),e._v(" "),n("spinner",{attrs:{show:e.loading}}),e._v(" "),n("div",{staticClass:"home-side"},[n("h4",{staticClass:"right-title"},[e._v("Top Topics")]),e._v(" "),e._l(e.showTags,function(t,r){return n("div",{key:r,staticClass:"right-body"},[n("router-link",{attrs:{to:"/tag/"+t.tagid}},[e._v(e._s(t.tagname))])],1)})],2)],1)])},s=[]},zcFI:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".rut-sum[data-v-54777a0e]{background-color:#fcfdfc;min-height:120px;padding:10px 30px 10px 100px;border-bottom:2px solid #eee;position:relative}.rut-sum[data-v-54777a0e]:hover{background-color:#fafaf8}.rut-sum .cover[data-v-54777a0e]{position:absolute;top:10px;left:5px}.rut-sum .title[data-v-54777a0e]{font-size:1.2em;font-weight:700;padding-top:10px}.rut-sum .title a[data-v-54777a0e]:hover{color:#f60}.rut-sum .intro[data-v-54777a0e]{color:#828282}.rut-sum .meta[data-v-54777a0e]{font-size:.85em;color:#337ab7}",""])}});
webpackJsonp([4],{"12NI":function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".comment[data-v-0e413581]{border-top:1px solid #eee;padding:.2em 1em;background-color:#fafaf8;position:relative}.comment .by[data-v-0e413581],.comment .toggle[data-v-0e413581]{font-size:.7em;margin:.2em 0}.comment .by[data-v-0e413581]{color:#828282}.comment .by a[data-v-0e413581]{color:#828282;text-decoration:underline}.comment .content[data-v-0e413581]{font-size:1.1em;margin:.2em 0}.comment .content a[data-v-0e413581]:hover{color:#f60}.comment .toggle[data-v-0e413581]{background-color:#eef2f5;padding:.1em .5em;border-radius:4px}.comment .toggle a[data-v-0e413581]{color:#828282;cursor:pointer}.comment .toggle.open[data-v-0e413581]{padding:0;background-color:transparent;margin-bottom:-.5em}.comment .comment-children[data-v-0e413581]{margin-left:1.5em}",""])},"4kAa":function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return i});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return e.creator?n("div",{staticClass:"review-main"},[n("h3",{staticClass:"title"},[n("router-link",{attrs:{to:"/review/"+e.review.id}},[e._v(e._s(e.review.heading))])],1),e._v(" "),n("p",{staticClass:"meta"},[e._v("\n    By "),n("router-link",{attrs:{to:"/profile/"+e.creator.id}},[e._v(e._s(e.creator.name))]),e._v("\n    | "+e._s(e._f("toMDY")(e.review.timestamp))+"\n    | on \n      "),n("router-link",{attrs:{to:"/item/"+e.review.item.id}},[e._v("\n        "+e._s(e.review.item.title.slice(0,42))+"...\n      ")])],1),e._v(" "),n("div",{staticClass:"review-body"},[n("div",{domProps:{innerHTML:e._s(e.reviewContent)}}),e._v(" "),e.spoiler||e.short?n("el-button",{attrs:{type:"text",size:"mini"},on:{click:e.showFull}},[e._v("\n               "+e._s(e.readMore)+"\n    ")]):e._e()],1),e._v(" "),n("div",{staticClass:"bar"},[e.canEdit?n("router-link",{attrs:{to:"/editreview/"+e.review.id}},[e._v("\n                 ...Edit |\n    ")]):e._e(),e._v(" "),n("el-button",{attrs:{type:"text"},on:{click:e.upReview}},[e._v("Helpful")]),e._v(" "+e._s(e.vote)+"\n  ")],1)]):e._e()},i=[]},CNqu:function(e,t,n){var r=n("G2nt");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);n("rjj0")("3b3e72d2",r,!0,{})},CnHd:function(e,t,n){var r=n("12NI");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);n("rjj0")("8c41a5fe",r,!0,{})},EFqf:function(e,t,n){(function(t){(function(){"use strict";function t(e){this.tokens=[],this.tokens.links={},this.options=e||u.defaults,this.rules=p.normal,this.options.gfm&&(this.options.tables?this.rules=p.tables:this.rules=p.gfm)}function n(e,t){if(this.options=t||u.defaults,this.links=e,this.rules=d.normal,this.renderer=this.options.renderer||new r,this.renderer.options=this.options,!this.links)throw new Error("Tokens array requires a `links` property.");this.options.gfm?this.options.breaks?this.rules=d.breaks:this.rules=d.gfm:this.options.pedantic&&(this.rules=d.pedantic)}function r(e){this.options=e||{}}function i(e){this.tokens=[],this.token=null,this.options=e||u.defaults,this.options.renderer=this.options.renderer||new r,this.renderer=this.options.renderer,this.renderer.options=this.options}function s(e,t){return e.replace(t?/&/g:/&(?!#?\w+;)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}function o(e){return e.replace(/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/gi,function(e,t){return t=t.toLowerCase(),"colon"===t?":":"#"===t.charAt(0)?"x"===t.charAt(1)?String.fromCharCode(parseInt(t.substring(2),16)):String.fromCharCode(+t.substring(1)):""})}function a(e,t){return e=e.source,t=t||"",function n(r,i){return r?(i=i.source||i,i=i.replace(/(^|[^\[])\^/g,"$1"),e=e.replace(r,i),n):new RegExp(e,t)}}function l(e,t){return f[" "+e]||(/^[^:]+:\/*[^\/]*$/.test(e)?f[" "+e]=e+"/":f[" "+e]=e.replace(/[^\/]*$/,"")),e=f[" "+e],"//"===t.slice(0,2)?e.replace(/:[\s\S]*/,":")+t:"/"===t.charAt(0)?e.replace(/(:\/*[^\/]*)[\s\S]*/,"$1")+t:e+t}function c(){}function h(e){for(var t,n,r=1;r<arguments.length;r++){t=arguments[r];for(n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e}function u(e,n,r){if(r||"function"==typeof n){r||(r=n,n=null),n=h({},u.defaults,n||{});var o,a,l=n.highlight,c=0;try{o=t.lex(e,n)}catch(e){return r(e)}a=o.length;var p=function(e){if(e)return n.highlight=l,r(e);var t;try{t=i.parse(o,n)}catch(t){e=t}return n.highlight=l,e?r(e):r(null,t)};if(!l||l.length<3)return p();if(delete n.highlight,!a)return p();for(;c<o.length;c++)!function(e){"code"!==e.type?--a||p():l(e.text,e.lang,function(t,n){return t?p(t):null==n||n===e.text?--a||p():(e.text=n,e.escaped=!0,void(--a||p()))})}(o[c])}else try{return n&&(n=h({},u.defaults,n)),i.parse(t.lex(e,n),n)}catch(e){if(e.message+="\nPlease report this to https://github.com/chjj/marked.",(n||u.defaults).silent)return"<p>An error occurred:</p><pre>"+s(e.message+"",!0)+"</pre>";throw e}}var p={newline:/^\n+/,code:/^( {4}[^\n]+\n*)+/,fences:c,hr:/^( *[-*_]){3,} *(?:\n+|$)/,heading:/^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)/,nptable:c,lheading:/^([^\n]+)\n *(=|-){2,} *(?:\n+|$)/,blockquote:/^( *>[^\n]+(\n(?!def)[^\n]+)*\n*)+/,list:/^( *)(bull) [\s\S]+?(?:hr|def|\n{2,}(?! )(?!\1bull )\n*|\s*$)/,html:/^ *(?:comment *(?:\n|\s*$)|closed *(?:\n{2,}|\s*$)|closing *(?:\n{2,}|\s*$))/,def:/^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +["(]([^\n]+)[")])? *(?:\n+|$)/,table:c,paragraph:/^((?:[^\n]+\n?(?!hr|heading|lheading|blockquote|tag|def))+)\n*/,text:/^[^\n]+/};p.bullet=/(?:[*+-]|\d+\.)/,p.item=/^( *)(bull) [^\n]*(?:\n(?!\1bull )[^\n]*)*/,p.item=a(p.item,"gm")(/bull/g,p.bullet)(),p.list=a(p.list)(/bull/g,p.bullet)("hr","\\n+(?=\\1?(?:[-*_] *){3,}(?:\\n+|$))")("def","\\n+(?="+p.def.source+")")(),p.blockquote=a(p.blockquote)("def",p.def)(),p._tag="(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:/|[^\\w\\s@]*@)\\b",p.html=a(p.html)("comment",/<!--[\s\S]*?-->/)("closed",/<(tag)[\s\S]+?<\/\1>/)("closing",/<tag(?:"[^"]*"|'[^']*'|[^'">])*?>/)(/tag/g,p._tag)(),p.paragraph=a(p.paragraph)("hr",p.hr)("heading",p.heading)("lheading",p.lheading)("blockquote",p.blockquote)("tag","<"+p._tag)("def",p.def)(),p.normal=h({},p),p.gfm=h({},p.normal,{fences:/^ *(`{3,}|~{3,})[ \.]*(\S+)? *\n([\s\S]*?)\s*\1 *(?:\n+|$)/,paragraph:/^/,heading:/^ *(#{1,6}) +([^\n]+?) *#* *(?:\n+|$)/}),p.gfm.paragraph=a(p.paragraph)("(?!","(?!"+p.gfm.fences.source.replace("\\1","\\2")+"|"+p.list.source.replace("\\1","\\3")+"|")(),p.tables=h({},p.gfm,{nptable:/^ *(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)\n*/,table:/^ *\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*/}),t.rules=p,t.lex=function(e,n){return new t(n).lex(e)},t.prototype.lex=function(e){return e=e.replace(/\r\n|\r/g,"\n").replace(/\t/g,"    ").replace(/\u00a0/g," ").replace(/\u2424/g,"\n"),this.token(e,!0)},t.prototype.token=function(e,t,n){for(var r,i,s,o,a,l,c,h,u,e=e.replace(/^ +$/gm,"");e;)if((s=this.rules.newline.exec(e))&&(e=e.substring(s[0].length),s[0].length>1&&this.tokens.push({type:"space"})),s=this.rules.code.exec(e))e=e.substring(s[0].length),s=s[0].replace(/^ {4}/gm,""),this.tokens.push({type:"code",text:this.options.pedantic?s:s.replace(/\n+$/,"")});else if(s=this.rules.fences.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"code",lang:s[2],text:s[3]||""});else if(s=this.rules.heading.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"heading",depth:s[1].length,text:s[2]});else if(t&&(s=this.rules.nptable.exec(e))){for(e=e.substring(s[0].length),l={type:"table",header:s[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:s[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:s[3].replace(/\n$/,"").split("\n")},h=0;h<l.align.length;h++)/^ *-+: *$/.test(l.align[h])?l.align[h]="right":/^ *:-+: *$/.test(l.align[h])?l.align[h]="center":/^ *:-+ *$/.test(l.align[h])?l.align[h]="left":l.align[h]=null;for(h=0;h<l.cells.length;h++)l.cells[h]=l.cells[h].split(/ *\| */);this.tokens.push(l)}else if(s=this.rules.lheading.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"heading",depth:"="===s[2]?1:2,text:s[1]});else if(s=this.rules.hr.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"hr"});else if(s=this.rules.blockquote.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"blockquote_start"}),s=s[0].replace(/^ *> ?/gm,""),this.token(s,t,!0),this.tokens.push({type:"blockquote_end"});else if(s=this.rules.list.exec(e)){for(e=e.substring(s[0].length),o=s[2],this.tokens.push({type:"list_start",ordered:o.length>1}),s=s[0].match(this.rules.item),r=!1,u=s.length,h=0;h<u;h++)l=s[h],c=l.length,l=l.replace(/^ *([*+-]|\d+\.) +/,""),~l.indexOf("\n ")&&(c-=l.length,l=this.options.pedantic?l.replace(/^ {1,4}/gm,""):l.replace(new RegExp("^ {1,"+c+"}","gm"),"")),this.options.smartLists&&h!==u-1&&(a=p.bullet.exec(s[h+1])[0],o===a||o.length>1&&a.length>1||(e=s.slice(h+1).join("\n")+e,h=u-1)),i=r||/\n\n(?!\s*$)/.test(l),h!==u-1&&(r="\n"===l.charAt(l.length-1),i||(i=r)),this.tokens.push({type:i?"loose_item_start":"list_item_start"}),this.token(l,!1,n),this.tokens.push({type:"list_item_end"});this.tokens.push({type:"list_end"})}else if(s=this.rules.html.exec(e))e=e.substring(s[0].length),this.tokens.push({type:this.options.sanitize?"paragraph":"html",pre:!this.options.sanitizer&&("pre"===s[1]||"script"===s[1]||"style"===s[1]),text:s[0]});else if(!n&&t&&(s=this.rules.def.exec(e)))e=e.substring(s[0].length),this.tokens.links[s[1].toLowerCase()]={href:s[2],title:s[3]};else if(t&&(s=this.rules.table.exec(e))){for(e=e.substring(s[0].length),l={type:"table",header:s[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:s[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:s[3].replace(/(?: *\| *)?\n$/,"").split("\n")},h=0;h<l.align.length;h++)/^ *-+: *$/.test(l.align[h])?l.align[h]="right":/^ *:-+: *$/.test(l.align[h])?l.align[h]="center":/^ *:-+ *$/.test(l.align[h])?l.align[h]="left":l.align[h]=null;for(h=0;h<l.cells.length;h++)l.cells[h]=l.cells[h].replace(/^ *\| *| *\| *$/g,"").split(/ *\| */);this.tokens.push(l)}else if(t&&(s=this.rules.paragraph.exec(e)))e=e.substring(s[0].length),this.tokens.push({type:"paragraph",text:"\n"===s[1].charAt(s[1].length-1)?s[1].slice(0,-1):s[1]});else if(s=this.rules.text.exec(e))e=e.substring(s[0].length),this.tokens.push({type:"text",text:s[0]});else if(e)throw new Error("Infinite loop on byte: "+e.charCodeAt(0));return this.tokens};var d={escape:/^\\([\\`*{}\[\]()#+\-.!_>])/,autolink:/^<([^ <>]+(@|:\/)[^ <>]+)>/,url:c,tag:/^<!--[\s\S]*?-->|^<\/?\w+(?:"[^"]*"|'[^']*'|[^<'">])*?>/,link:/^!?\[(inside)\]\(href\)/,reflink:/^!?\[(inside)\]\s*\[([^\]]*)\]/,nolink:/^!?\[((?:\[[^\]]*\]|[^\[\]])*)\]/,strong:/^__([\s\S]+?)__(?!_)|^\*\*([\s\S]+?)\*\*(?!\*)/,em:/^\b_((?:[^_]|__)+?)_\b|^\*((?:\*\*|[\s\S])+?)\*(?!\*)/,code:/^(`+)([\s\S]*?[^`])\1(?!`)/,br:/^ {2,}\n(?!\s*$)/,del:c,text:/^[\s\S]+?(?=[\\<!\[_*`]| {2,}\n|$)/};d._inside=/(?:\[[^\]]*\]|\\[\[\]]|[^\[\]]|\](?=[^\[]*\]))*/,d._href=/\s*<?([\s\S]*?)>?(?:\s+['"]([\s\S]*?)['"])?\s*/,d.link=a(d.link)("inside",d._inside)("href",d._href)(),d.reflink=a(d.reflink)("inside",d._inside)(),d.normal=h({},d),d.pedantic=h({},d.normal,{strong:/^__(?=\S)([\s\S]*?\S)__(?!_)|^\*\*(?=\S)([\s\S]*?\S)\*\*(?!\*)/,em:/^_(?=\S)([\s\S]*?\S)_(?!_)|^\*(?=\S)([\s\S]*?\S)\*(?!\*)/}),d.gfm=h({},d.normal,{escape:a(d.escape)("])","~|])")(),url:/^(https?:\/\/[^\s<]+[^<.,:;"')\]\s])/,del:/^~~(?=\S)([\s\S]*?\S)~~/,text:a(d.text)("]|","~]|")("|","|https?://|")()}),d.breaks=h({},d.gfm,{br:a(d.br)("{2,}","*")(),text:a(d.gfm.text)("{2,}","*")()}),n.rules=d,n.output=function(e,t,r){return new n(t,r).output(e)},n.prototype.output=function(e){for(var t,n,r,i,o="";e;)if(i=this.rules.escape.exec(e))e=e.substring(i[0].length),o+=i[1];else if(i=this.rules.autolink.exec(e))e=e.substring(i[0].length),"@"===i[2]?(n=s(":"===i[1].charAt(6)?this.mangle(i[1].substring(7)):this.mangle(i[1])),r=this.mangle("mailto:")+n):(n=s(i[1]),r=n),o+=this.renderer.link(r,null,n);else if(this.inLink||!(i=this.rules.url.exec(e))){if(i=this.rules.tag.exec(e))!this.inLink&&/^<a /i.test(i[0])?this.inLink=!0:this.inLink&&/^<\/a>/i.test(i[0])&&(this.inLink=!1),e=e.substring(i[0].length),o+=this.options.sanitize?this.options.sanitizer?this.options.sanitizer(i[0]):s(i[0]):i[0];else if(i=this.rules.link.exec(e))e=e.substring(i[0].length),this.inLink=!0,o+=this.outputLink(i,{href:i[2],title:i[3]}),this.inLink=!1;else if((i=this.rules.reflink.exec(e))||(i=this.rules.nolink.exec(e))){if(e=e.substring(i[0].length),t=(i[2]||i[1]).replace(/\s+/g," "),!(t=this.links[t.toLowerCase()])||!t.href){o+=i[0].charAt(0),e=i[0].substring(1)+e;continue}this.inLink=!0,o+=this.outputLink(i,t),this.inLink=!1}else if(i=this.rules.strong.exec(e))e=e.substring(i[0].length),o+=this.renderer.strong(this.output(i[2]||i[1]));else if(i=this.rules.em.exec(e))e=e.substring(i[0].length),o+=this.renderer.em(this.output(i[2]||i[1]));else if(i=this.rules.code.exec(e))e=e.substring(i[0].length),o+=this.renderer.codespan(s(i[2].trim(),!0));else if(i=this.rules.br.exec(e))e=e.substring(i[0].length),o+=this.renderer.br();else if(i=this.rules.del.exec(e))e=e.substring(i[0].length),o+=this.renderer.del(this.output(i[1]));else if(i=this.rules.text.exec(e))e=e.substring(i[0].length),o+=this.renderer.text(s(this.smartypants(i[0])));else if(e)throw new Error("Infinite loop on byte: "+e.charCodeAt(0))}else e=e.substring(i[0].length),n=s(i[1]),r=n,o+=this.renderer.link(r,null,n);return o},n.prototype.outputLink=function(e,t){var n=s(t.href),r=t.title?s(t.title):null;return"!"!==e[0].charAt(0)?this.renderer.link(n,r,this.output(e[1])):this.renderer.image(n,r,s(e[1]))},n.prototype.smartypants=function(e){return this.options.smartypants?e.replace(/---/g,"—").replace(/--/g,"–").replace(/(^|[-\u2014\/(\[{"\s])'/g,"$1‘").replace(/'/g,"’").replace(/(^|[-\u2014\/(\[{\u2018\s])"/g,"$1“").replace(/"/g,"”").replace(/\.{3}/g,"…"):e},n.prototype.mangle=function(e){if(!this.options.mangle)return e;for(var t,n="",r=e.length,i=0;i<r;i++)t=e.charCodeAt(i),Math.random()>.5&&(t="x"+t.toString(16)),n+="&#"+t+";";return n},r.prototype.code=function(e,t,n){if(this.options.highlight){var r=this.options.highlight(e,t);null!=r&&r!==e&&(n=!0,e=r)}return t?'<pre><code class="'+this.options.langPrefix+s(t,!0)+'">'+(n?e:s(e,!0))+"\n</code></pre>\n":"<pre><code>"+(n?e:s(e,!0))+"\n</code></pre>"},r.prototype.blockquote=function(e){return"<blockquote>\n"+e+"</blockquote>\n"},r.prototype.html=function(e){return e},r.prototype.heading=function(e,t,n){return"<h"+t+' id="'+this.options.headerPrefix+n.toLowerCase().replace(/[^\w]+/g,"-")+'">'+e+"</h"+t+">\n"},r.prototype.hr=function(){return this.options.xhtml?"<hr/>\n":"<hr>\n"},r.prototype.list=function(e,t){var n=t?"ol":"ul";return"<"+n+">\n"+e+"</"+n+">\n"},r.prototype.listitem=function(e){return"<li>"+e+"</li>\n"},r.prototype.paragraph=function(e){return"<p>"+e+"</p>\n"},r.prototype.table=function(e,t){return"<table>\n<thead>\n"+e+"</thead>\n<tbody>\n"+t+"</tbody>\n</table>\n"},r.prototype.tablerow=function(e){return"<tr>\n"+e+"</tr>\n"},r.prototype.tablecell=function(e,t){var n=t.header?"th":"td";return(t.align?"<"+n+' style="text-align:'+t.align+'">':"<"+n+">")+e+"</"+n+">\n"},r.prototype.strong=function(e){return"<strong>"+e+"</strong>"},r.prototype.em=function(e){return"<em>"+e+"</em>"},r.prototype.codespan=function(e){return"<code>"+e+"</code>"},r.prototype.br=function(){return this.options.xhtml?"<br/>":"<br>"},r.prototype.del=function(e){return"<del>"+e+"</del>"},r.prototype.link=function(e,t,n){if(this.options.sanitize){try{var r=decodeURIComponent(o(e)).replace(/[^\w:]/g,"").toLowerCase()}catch(e){return n}if(0===r.indexOf("javascript:")||0===r.indexOf("vbscript:")||0===r.indexOf("data:"))return n}this.options.baseUrl&&!m.test(e)&&(e=l(this.options.baseUrl,e));var i='<a href="'+e+'"';return t&&(i+=' title="'+t+'"'),i+=">"+n+"</a>"},r.prototype.image=function(e,t,n){this.options.baseUrl&&!m.test(e)&&(e=l(this.options.baseUrl,e));var r='<img src="'+e+'" alt="'+n+'"';return t&&(r+=' title="'+t+'"'),r+=this.options.xhtml?"/>":">"},r.prototype.text=function(e){return e},i.parse=function(e,t,n){return new i(t,n).parse(e)},i.prototype.parse=function(e){this.inline=new n(e.links,this.options,this.renderer),this.tokens=e.reverse();for(var t="";this.next();)t+=this.tok();return t},i.prototype.next=function(){return this.token=this.tokens.pop()},i.prototype.peek=function(){return this.tokens[this.tokens.length-1]||0},i.prototype.parseText=function(){for(var e=this.token.text;"text"===this.peek().type;)e+="\n"+this.next().text;return this.inline.output(e)},i.prototype.tok=function(){switch(this.token.type){case"space":return"";case"hr":return this.renderer.hr();case"heading":return this.renderer.heading(this.inline.output(this.token.text),this.token.depth,this.token.text);case"code":return this.renderer.code(this.token.text,this.token.lang,this.token.escaped);case"table":var e,t,n,r,i="",s="";for(n="",e=0;e<this.token.header.length;e++)({header:!0,align:this.token.align[e]}),n+=this.renderer.tablecell(this.inline.output(this.token.header[e]),{header:!0,align:this.token.align[e]});for(i+=this.renderer.tablerow(n),e=0;e<this.token.cells.length;e++){for(t=this.token.cells[e],n="",r=0;r<t.length;r++)n+=this.renderer.tablecell(this.inline.output(t[r]),{header:!1,align:this.token.align[r]});s+=this.renderer.tablerow(n)}return this.renderer.table(i,s);case"blockquote_start":for(var s="";"blockquote_end"!==this.next().type;)s+=this.tok();return this.renderer.blockquote(s);case"list_start":for(var s="",o=this.token.ordered;"list_end"!==this.next().type;)s+=this.tok();return this.renderer.list(s,o);case"list_item_start":for(var s="";"list_item_end"!==this.next().type;)s+="text"===this.token.type?this.parseText():this.tok();return this.renderer.listitem(s);case"loose_item_start":for(var s="";"list_item_end"!==this.next().type;)s+=this.tok();return this.renderer.listitem(s);case"html":var a=this.token.pre||this.options.pedantic?this.token.text:this.inline.output(this.token.text);return this.renderer.html(a);case"paragraph":return this.renderer.paragraph(this.inline.output(this.token.text));case"text":return this.renderer.paragraph(this.parseText())}};var f={},m=/^$|^[a-z][a-z0-9+.-]*:|^[?#]/i;c.exec=c,u.options=u.setOptions=function(e){return h(u.defaults,e),u},u.defaults={gfm:!0,tables:!0,breaks:!1,pedantic:!1,sanitize:!1,sanitizer:null,mangle:!0,smartLists:!1,silent:!1,highlight:null,langPrefix:"lang-",smartypants:!1,headerPrefix:"",renderer:new r,xhtml:!1,baseUrl:null},u.Parser=i,u.parser=i.parse,u.Renderer=r,u.Lexer=t,u.lexer=t.lex,u.InlineLexer=n,u.inlineLexer=n.output,u.parse=u,e.exports=u}).call(function(){return this||("undefined"!=typeof window?window:t)}())}).call(t,n("DuR2"))},G2nt:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,"#social-share-bar[data-v-755a1738]{text-align:right}#social-share-bar>.share-link[data-v-755a1738]{cursor:pointer;display:inline-block;text-align:center}#social-share-bar>.share-link.evernote[data-v-755a1738]:hover{background-color:#8be056}#social-share-bar>.share-link.twitter[data-v-755a1738]:hover{background-color:#55acee}#social-share-bar>.share-link.facebook[data-v-755a1738]:hover{background-color:#3b5998}#social-share-bar>.share-link.google-plus[data-v-755a1738]:hover{background-color:#dd4b39}#social-share-bar>.share-link.linkedin[data-v-755a1738]:hover{background-color:#007bb5}#social-share-bar>.share-link .icon[data-v-755a1738]{padding:5px;width:16px;height:16px}",""])},GwPc:function(e,t,n){"use strict";var r=n("EFqf"),i=n.n(r);i.a.setOptions({renderer:new i.a.Renderer,gfm:!0,tables:!0,breaks:!0,pedantic:!1,sanitize:!1,smartLists:!0,smartypants:!1});var s=new i.a.Renderer,o=function(e){return"<p>"+e+"</p>"},a=function(e,t,n){var r=e.includes("readup.tips"),i=n.includes("<img");return('<a href="'+e+'" \n             target="_blank"\n             title="'+(t||(i?e:n))+'" \n             '+(r?"":'rel="external nofollow noopener noreferrer"')+">"+n+"\n          </a>").replace(/\s+/g," ").replace("\n","")},l=function(e,t,n){return('<a href="'+e+'" \n             target="_blank" rel="nofollow noopener noreferrer">\n            <img src="'+e+'" \n                title="'+(t||n||"readup.tips")+'" \n                style="width:10%; height:15%"\n                alt="'+(n||t||e)+'"/>\n          </a>').replace(/\s+/g," ").replace("\n","")};s.link=a,s.image=l,s.paragraph=o,t.a=function(e){return"string"!=typeof e?"":i()(e,{renderer:s})}},I9M3:function(e,t,n){"use strict";var r=n("Gu7T"),i=n.n(r),s=n("P9l9"),o=n("IAun"),a=n("reXA"),l=n("kRrK"),c=n("ZCVe");t.a={name:"review-view",title:function(){return this.review.heading},components:{ReviewSum:o.a,Comment:a.a,Reply:l.a,ShareBar:c.a},data:function(){return{review:{},comments:[],commentCount:0,currentPage:1,refer:{re:"review",id:this.$route.params.id}}},computed:{hasMoreComment:function(){return this.comments.length<this.commentCount}},methods:{loadReviewData:function(){var e=this,t=this.$route.params.id;this.$store.dispatch("getReview",t).then(function(t){var n=t.data;e.review=n,e.comments=n.comments,e.commentCount=n.commentcount})},loadmoreComment:function(){var e=this,t=this.$route.params.id,n={page:this.currentPage};Object(s.V)(t,n).then(function(t){var n;(n=e.comments).push.apply(n,i()(t.data)),e.currentPage+=1})},updateNew:function(e){this.comments.unshift(e)}},created:function(){this.loadReviewData()}}},IAun:function(e,t,n){"use strict";function r(e){n("uRGj")}var i=n("tm0w"),s=n("4kAa"),o=n("XyMi"),a=r,l=Object(o.a)(i.a,s.a,s.b,!1,a,"data-v-1b4cb4d7",null);t.a=l.exports},"MRW/":function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return i});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"review-page"},[n("div",{staticClass:"review-main"},[n("review-sum",{key:e.review.id,attrs:{review:e.review}})],1),e._v(" "),n("div",{staticClass:"share"},[n("share-bar")],1),e._v(" "),e._l(e.comments,function(e){return n("div",{key:e.id},[n("comment",{attrs:{comment:e}})],1)}),e._v(" "),e.hasMoreComment?n("div",[n("el-button",{staticClass:"blockbtn",attrs:{size:"mini",disabled:!e.hasMoreComment},on:{click:e.loadmoreComment}},[e._v("\n               Show More Comments\n    ")])],1):e._e(),e._v(" "),n("div",{staticClass:"comment"},[n("reply",{staticClass:"reply",attrs:{refer:e.refer,show:!0},on:{newreply:e.updateNew}})],1)],2)},i=[]},Nucc:function(e,t,n){"use strict";var r=n("kRrK"),i=n("GwPc");t.a={name:"comment",props:["comment"],components:{Reply:r.a},data:function(){return{open:!1,showRe:!1,hasChild:this.comment.children.length>0,childComments:this.comment.children,refer:{re:"comment",id:this.comment.id}}},computed:{creator:function(){return this.comment.creator},commentContent:function(){return Object(i.a)(this.comment.body)}},methods:{updateNew:function(e){this.open=!0,this.childComments.unshift(e)}}}},PEd3:function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return i});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{attrs:{id:"social-share-bar"}},[n("a",{staticClass:"share-link twitter",attrs:{title:"Twitter",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://twitter.com/share?text="+e.title()+"&url="+e.url)}}},[n("img",{staticClass:"icon",attrs:{alt:"TW",src:"/static/pic/twitter.svg"}})]),e._v(" "),n("a",{staticClass:"share-link facebook",attrs:{title:"Facebook",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://www.facebook.com/sharer/sharer.php?u="+e.url)}}},[n("img",{staticClass:"icon",attrs:{alt:"FB",src:"/static/pic/facebook.svg"}})]),e._v(" "),n("a",{staticClass:"share-link linkedin",attrs:{title:"Linkedin",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://www.linkedin.com/shareArticle?mini=true&url="+e.url+"&title="+e.title())}}},[n("img",{staticClass:"icon",attrs:{alt:"Linkedin",src:"/static/pic/linkedin.svg"}})]),e._v(" "),n("a",{staticClass:"share-link google-plus",attrs:{title:"Google+",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://plus.google.com/share?url="+e.url)}}},[n("img",{staticClass:"icon",attrs:{alt:"G+",src:"/static/pic/gplus.svg"}})]),e._v(" "),n("a",{staticClass:"share-link evernote",attrs:{title:"Evernote",rel:"nofollow noopener noreferrer"},on:{click:function(t){t.preventDefault(),e.shareWindow("https://www.evernote.com/clip.action?url="+e.url+"&title="+e.title())}}},[n("img",{staticClass:"icon",attrs:{alt:"Evernote",src:"/static/pic/evernote.svg"}})])])},i=[]},S4U7:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".review-main[data-v-1b4cb4d7]{background-color:#fafbf9;padding:5px;border-bottom:1px solid #eee;position:relative}.review-main .title[data-v-1b4cb4d7]{font-weight:700}.review-main .title a[data-v-1b4cb4d7]:hover{color:#f60}.review-main .meta[data-v-1b4cb4d7]{font-size:.75em}.review-main .bar[data-v-1b4cb4d7]{font-size:.7em;text-align:right}.review-main .review-body[data-v-1b4cb4d7]{background-color:#f4f7f3;padding:0 5px;font-size:1.05em}",""])},ZCVe:function(e,t,n){"use strict";function r(e){n("CNqu")}var i=n("r8Lr"),s=n("PEd3"),o=n("XyMi"),a=r,l=Object(o.a)(i.a,s.a,s.b,!1,a,"data-v-755a1738",null);t.a=l.exports},b1B2:function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".review-page[data-v-8cf292e0]{padding:10px 235px 10px 0;position:relative}.review-page .review-main[data-v-8cf292e0]{padding:auto}.review-page .review-side[data-v-8cf292e0]{position:absolute;top:10px;right:0;width:225px}",""])},b2JC:function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return i});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return e.comment?n("div",{staticClass:"comment"},[n("div",{staticClass:"by"},[n("router-link",{attrs:{to:"/profile/"+e.creator.id}},[e._v(e._s(e.creator.name))]),e._v("\n    ~ "+e._s(e._f("timeAgo")(e.comment.timestamp))+"\n  ")],1),e._v(" "),n("div",{staticClass:"content",domProps:{innerHTML:e._s(e.commentContent)}}),e._v(" "),n("el-button",{attrs:{type:"text",size:"mini"},on:{click:function(t){e.showRe=!e.showRe}}},[e._v("\n    "+e._s(e.showRe?"Hide":"Reply")+"\n  ")]),e._v(" "),e.hasChild?n("span",{staticClass:"toggle",class:{open:e.open}},[n("a",{on:{click:function(t){e.open=!e.open}}},[e._v("\n      "+e._s(e.open?"[-]":"[+] "+e.childComments.length+" collapsed")+" \n    ")])]):e._e(),e._v(" "),n("reply",{staticClass:"reply",attrs:{refer:e.refer,show:e.showRe},on:{"update:show":function(t){e.showRe=t},newreply:e.updateNew}}),e._v(" "),n("div",{directives:[{name:"show",rawName:"v-show",value:e.open,expression:"open"}],staticClass:"comment-children"},e._l(e.childComments,function(e){return n("comment",{key:e.id,attrs:{comment:e}})}))],1):e._e()},i=[]},bVqk:function(e,t,n){var r=n("b1B2");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);n("rjj0")("046962c6",r,!0,{})},cyWQ:function(e,t,n){"use strict";n.d(t,"a",function(){return r}),n.d(t,"b",function(){return i});var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{directives:[{name:"show",rawName:"v-show",value:e.show,expression:"show"}],staticClass:"reply"},[n("el-form",{ref:"commentForm",attrs:{model:e.commentForm,rules:e.rules}},[n("el-form-item",{staticStyle:{"margin-bottom":"4px"},attrs:{prop:"comment"}},[n("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"Post a Comment"},model:{value:e.commentForm.comment,callback:function(t){e.$set(e.commentForm,"comment",t)},expression:"commentForm.comment"}})],1),e._v(" "),n("el-form-item",[n("el-button",{attrs:{size:"mini",disabled:!e.commentForm.comment.trim()},on:{click:function(t){e.reply("commentForm",e.commentForm)}}},[e._v("\n                 Submit\n      ")])],1)],1)],1)},i=[]},dn1P:function(e,t,n){"use strict";var r=n("P9l9"),i=n("iF09");t.a={name:"reply",props:{refer:Object,show:{default:!1}},data:function(){return{commentForm:{comment:""},rules:{comment:[{min:1,max:500,message:"Required, Max 500 Characters",trigger:"blur"}]}}},methods:{reply:function(e,t){var n=this;this.$refs[e].validate(function(s){if(s&&t.comment.trim()&&Object(i.a)()){var o={comment:t.comment.trim()},a=n.refer.re,l=n.refer.id;Object(r._13)(a,l,o).then(function(e){n.$emit("newreply",e.data)}),n.resetForm(e),n.$emit("update:show",!1)}else Object(i.a)()||(n.$message({showClose:!0,message:"Should Log in to post Comment"}),n.$router.push({path:"/login",query:{redirect:n.$route.fullPath}}))})},resetForm:function(e){this.$refs[e].resetFields()}}}},"ieF/":function(e,t,n){t=e.exports=n("FZ+f")(!1),t.push([e.i,".reply[data-v-1f45d910]{padding:5px 0}",""])},kRrK:function(e,t,n){"use strict";function r(e){n("nWx4")}var i=n("dn1P"),s=n("cyWQ"),o=n("XyMi"),a=r,l=Object(o.a)(i.a,s.a,s.b,!1,a,"data-v-1f45d910",null);t.a=l.exports},nWx4:function(e,t,n){var r=n("ieF/");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);n("rjj0")("6a953f9e",r,!0,{})},r8Lr:function(e,t,n){"use strict";t.a={name:"share-bar",props:{passUrl:String,passTitle:String,prefix:{type:String,default:""}},computed:{url:function(){return this.passUrl||"https://readup.tips"+this.$route.fullPath}},methods:{title:function(){try{if(document)return this.prefix+(this.passTitle||document.title)}catch(e){return"Readup.Tips"}},shareWindow:function(e){e=encodeURI(e),console.log(e);var t=screen.availWidth/2,n=screen.availHeight/5*2,r=(screen.availHeight-n)/2,i=(screen.availWidth-t)/2,s="top="+r+",left="+i+",width="+t+",height="+n+",scrollbars=0,status=0,menubar=0,resizable=2,location=0";window.open(e,"newWin",s).focus()}}}},reXA:function(e,t,n){"use strict";function r(e){n("CnHd")}var i=n("Nucc"),s=n("b2JC"),o=n("XyMi"),a=r,l=Object(o.a)(i.a,s.a,s.b,!1,a,"data-v-0e413581",null);t.a=l.exports},tm0w:function(e,t,n){"use strict";var r=n("P9l9"),i=n("iF09"),s=n("6aq2"),o=n("GwPc");t.a={name:"review-sum",props:{review:Object,less:Boolean},data:function(){return{vote:this.review.vote,spoiler:this.review.spoiler,short:this.less}},computed:{creator:function(){return this.review.creator},reviewContent:function(){var e=Object(o.a)(this.review.body),t=this.spoiler?0:255;return this.short||this.spoiler?Object(s.showLess)(e,t):e},readMore:function(){return this.spoiler?"Spoilers Ahead! Continue?":"Read More ..."},canEdit:function(){return Number(this.review.creator.id)===Number(this.$store.getters.currentUserID)}},methods:{showFull:function(){this.spoiler=!1,this.short=!1},upReview:function(){var e=this;if(Object(i.a)()){var t=this.review.id;Object(r._35)(t).then(function(t){e.vote=t.data})}}}}},uRGj:function(e,t,n){var r=n("S4U7");"string"==typeof r&&(r=[[e.i,r,""]]),r.locals&&(e.exports=r.locals);n("rjj0")("4c662a91",r,!0,{})},z57P:function(e,t,n){"use strict";function r(e){n("bVqk")}Object.defineProperty(t,"__esModule",{value:!0});var i=n("I9M3"),s=n("MRW/"),o=n("XyMi"),a=r,l=Object(o.a)(i.a,s.a,s.b,!1,a,"data-v-8cf292e0",null);t.default=l.exports}});
webpackJsonp([21],{"+SxW":function(t,e,n){"use strict";function r(t){n("EIGv")}var i=n("ByB/"),s=n("Y/D9"),o=n("XyMi"),l=r,a=Object(o.a)(i.a,s.a,s.b,!1,l,"data-v-59f81342",null);e.a=a.exports},"ByB/":function(t,e,n){"use strict";var r=n("P9l9"),i=n("iF09"),s=n("GwPc");e.a={name:"clip",props:["clip"],data:function(){return{vote:this.clip.vote}},computed:{creator:function(){return this.clip.creator},fromitem:function(){return this.clip.fromitem},clipContent:function(){return Object(s.a)(this.clip.body)}},methods:{upClip:function(){var t=this;if(Object(i.a)()){var e=this.clip.id;Object(r._32)(e).then(function(e){t.vote=e.data})}}}}},EFqf:function(t,e,n){(function(e){(function(){"use strict";function e(t){this.tokens=[],this.tokens.links={},this.options=t||u.defaults,this.rules=c.normal,this.options.gfm&&(this.options.tables?this.rules=c.tables:this.rules=c.gfm)}function n(t,e){if(this.options=e||u.defaults,this.links=t,this.rules=g.normal,this.renderer=this.options.renderer||new r,this.renderer.options=this.options,!this.links)throw new Error("Tokens array requires a `links` property.");this.options.gfm?this.options.breaks?this.rules=g.breaks:this.rules=g.gfm:this.options.pedantic&&(this.rules=g.pedantic)}function r(t){this.options=t||{}}function i(t){this.tokens=[],this.token=null,this.options=t||u.defaults,this.options.renderer=this.options.renderer||new r,this.renderer=this.options.renderer,this.renderer.options=this.options}function s(t,e){return t.replace(e?/&/g:/&(?!#?\w+;)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}function o(t){return t.replace(/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/gi,function(t,e){return e=e.toLowerCase(),"colon"===e?":":"#"===e.charAt(0)?"x"===e.charAt(1)?String.fromCharCode(parseInt(e.substring(2),16)):String.fromCharCode(+e.substring(1)):""})}function l(t,e){return t=t.source,e=e||"",function n(r,i){return r?(i=i.source||i,i=i.replace(/(^|[^\[])\^/g,"$1"),t=t.replace(r,i),n):new RegExp(t,e)}}function a(t,e){return f[" "+t]||(/^[^:]+:\/*[^\/]*$/.test(t)?f[" "+t]=t+"/":f[" "+t]=t.replace(/[^\/]*$/,"")),t=f[" "+t],"//"===e.slice(0,2)?t.replace(/:[\s\S]*/,":")+e:"/"===e.charAt(0)?t.replace(/(:\/*[^\/]*)[\s\S]*/,"$1")+e:t+e}function h(){}function p(t){for(var e,n,r=1;r<arguments.length;r++){e=arguments[r];for(n in e)Object.prototype.hasOwnProperty.call(e,n)&&(t[n]=e[n])}return t}function u(t,n,r){if(r||"function"==typeof n){r||(r=n,n=null),n=p({},u.defaults,n||{});var o,l,a=n.highlight,h=0;try{o=e.lex(t,n)}catch(t){return r(t)}l=o.length;var c=function(t){if(t)return n.highlight=a,r(t);var e;try{e=i.parse(o,n)}catch(e){t=e}return n.highlight=a,t?r(t):r(null,e)};if(!a||a.length<3)return c();if(delete n.highlight,!l)return c();for(;h<o.length;h++)!function(t){"code"!==t.type?--l||c():a(t.text,t.lang,function(e,n){return e?c(e):null==n||n===t.text?--l||c():(t.text=n,t.escaped=!0,void(--l||c()))})}(o[h])}else try{return n&&(n=p({},u.defaults,n)),i.parse(e.lex(t,n),n)}catch(t){if(t.message+="\nPlease report this to https://github.com/chjj/marked.",(n||u.defaults).silent)return"<p>An error occurred:</p><pre>"+s(t.message+"",!0)+"</pre>";throw t}}var c={newline:/^\n+/,code:/^( {4}[^\n]+\n*)+/,fences:h,hr:/^( *[-*_]){3,} *(?:\n+|$)/,heading:/^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)/,nptable:h,lheading:/^([^\n]+)\n *(=|-){2,} *(?:\n+|$)/,blockquote:/^( *>[^\n]+(\n(?!def)[^\n]+)*\n*)+/,list:/^( *)(bull) [\s\S]+?(?:hr|def|\n{2,}(?! )(?!\1bull )\n*|\s*$)/,html:/^ *(?:comment *(?:\n|\s*$)|closed *(?:\n{2,}|\s*$)|closing *(?:\n{2,}|\s*$))/,def:/^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +["(]([^\n]+)[")])? *(?:\n+|$)/,table:h,paragraph:/^((?:[^\n]+\n?(?!hr|heading|lheading|blockquote|tag|def))+)\n*/,text:/^[^\n]+/};c.bullet=/(?:[*+-]|\d+\.)/,c.item=/^( *)(bull) [^\n]*(?:\n(?!\1bull )[^\n]*)*/,c.item=l(c.item,"gm")(/bull/g,c.bullet)(),c.list=l(c.list)(/bull/g,c.bullet)("hr","\\n+(?=\\1?(?:[-*_] *){3,}(?:\\n+|$))")("def","\\n+(?="+c.def.source+")")(),c.blockquote=l(c.blockquote)("def",c.def)(),c._tag="(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:/|[^\\w\\s@]*@)\\b",c.html=l(c.html)("comment",/<!--[\s\S]*?-->/)("closed",/<(tag)[\s\S]+?<\/\1>/)("closing",/<tag(?:"[^"]*"|'[^']*'|[^'">])*?>/)(/tag/g,c._tag)(),c.paragraph=l(c.paragraph)("hr",c.hr)("heading",c.heading)("lheading",c.lheading)("blockquote",c.blockquote)("tag","<"+c._tag)("def",c.def)(),c.normal=p({},c),c.gfm=p({},c.normal,{fences:/^ *(`{3,}|~{3,})[ \.]*(\S+)? *\n([\s\S]*?)\s*\1 *(?:\n+|$)/,paragraph:/^/,heading:/^ *(#{1,6}) +([^\n]+?) *#* *(?:\n+|$)/}),c.gfm.paragraph=l(c.paragraph)("(?!","(?!"+c.gfm.fences.source.replace("\\1","\\2")+"|"+c.list.source.replace("\\1","\\3")+"|")(),c.tables=p({},c.gfm,{nptable:/^ *(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)\n*/,table:/^ *\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*/}),e.rules=c,e.lex=function(t,n){return new e(n).lex(t)},e.prototype.lex=function(t){return t=t.replace(/\r\n|\r/g,"\n").replace(/\t/g,"    ").replace(/\u00a0/g," ").replace(/\u2424/g,"\n"),this.token(t,!0)},e.prototype.token=function(t,e,n){for(var r,i,s,o,l,a,h,p,u,t=t.replace(/^ +$/gm,"");t;)if((s=this.rules.newline.exec(t))&&(t=t.substring(s[0].length),s[0].length>1&&this.tokens.push({type:"space"})),s=this.rules.code.exec(t))t=t.substring(s[0].length),s=s[0].replace(/^ {4}/gm,""),this.tokens.push({type:"code",text:this.options.pedantic?s:s.replace(/\n+$/,"")});else if(s=this.rules.fences.exec(t))t=t.substring(s[0].length),this.tokens.push({type:"code",lang:s[2],text:s[3]||""});else if(s=this.rules.heading.exec(t))t=t.substring(s[0].length),this.tokens.push({type:"heading",depth:s[1].length,text:s[2]});else if(e&&(s=this.rules.nptable.exec(t))){for(t=t.substring(s[0].length),a={type:"table",header:s[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:s[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:s[3].replace(/\n$/,"").split("\n")},p=0;p<a.align.length;p++)/^ *-+: *$/.test(a.align[p])?a.align[p]="right":/^ *:-+: *$/.test(a.align[p])?a.align[p]="center":/^ *:-+ *$/.test(a.align[p])?a.align[p]="left":a.align[p]=null;for(p=0;p<a.cells.length;p++)a.cells[p]=a.cells[p].split(/ *\| */);this.tokens.push(a)}else if(s=this.rules.lheading.exec(t))t=t.substring(s[0].length),this.tokens.push({type:"heading",depth:"="===s[2]?1:2,text:s[1]});else if(s=this.rules.hr.exec(t))t=t.substring(s[0].length),this.tokens.push({type:"hr"});else if(s=this.rules.blockquote.exec(t))t=t.substring(s[0].length),this.tokens.push({type:"blockquote_start"}),s=s[0].replace(/^ *> ?/gm,""),this.token(s,e,!0),this.tokens.push({type:"blockquote_end"});else if(s=this.rules.list.exec(t)){for(t=t.substring(s[0].length),o=s[2],this.tokens.push({type:"list_start",ordered:o.length>1}),s=s[0].match(this.rules.item),r=!1,u=s.length,p=0;p<u;p++)a=s[p],h=a.length,a=a.replace(/^ *([*+-]|\d+\.) +/,""),~a.indexOf("\n ")&&(h-=a.length,a=this.options.pedantic?a.replace(/^ {1,4}/gm,""):a.replace(new RegExp("^ {1,"+h+"}","gm"),"")),this.options.smartLists&&p!==u-1&&(l=c.bullet.exec(s[p+1])[0],o===l||o.length>1&&l.length>1||(t=s.slice(p+1).join("\n")+t,p=u-1)),i=r||/\n\n(?!\s*$)/.test(a),p!==u-1&&(r="\n"===a.charAt(a.length-1),i||(i=r)),this.tokens.push({type:i?"loose_item_start":"list_item_start"}),this.token(a,!1,n),this.tokens.push({type:"list_item_end"});this.tokens.push({type:"list_end"})}else if(s=this.rules.html.exec(t))t=t.substring(s[0].length),this.tokens.push({type:this.options.sanitize?"paragraph":"html",pre:!this.options.sanitizer&&("pre"===s[1]||"script"===s[1]||"style"===s[1]),text:s[0]});else if(!n&&e&&(s=this.rules.def.exec(t)))t=t.substring(s[0].length),this.tokens.links[s[1].toLowerCase()]={href:s[2],title:s[3]};else if(e&&(s=this.rules.table.exec(t))){for(t=t.substring(s[0].length),a={type:"table",header:s[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:s[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:s[3].replace(/(?: *\| *)?\n$/,"").split("\n")},p=0;p<a.align.length;p++)/^ *-+: *$/.test(a.align[p])?a.align[p]="right":/^ *:-+: *$/.test(a.align[p])?a.align[p]="center":/^ *:-+ *$/.test(a.align[p])?a.align[p]="left":a.align[p]=null;for(p=0;p<a.cells.length;p++)a.cells[p]=a.cells[p].replace(/^ *\| *| *\| *$/g,"").split(/ *\| */);this.tokens.push(a)}else if(e&&(s=this.rules.paragraph.exec(t)))t=t.substring(s[0].length),this.tokens.push({type:"paragraph",text:"\n"===s[1].charAt(s[1].length-1)?s[1].slice(0,-1):s[1]});else if(s=this.rules.text.exec(t))t=t.substring(s[0].length),this.tokens.push({type:"text",text:s[0]});else if(t)throw new Error("Infinite loop on byte: "+t.charCodeAt(0));return this.tokens};var g={escape:/^\\([\\`*{}\[\]()#+\-.!_>])/,autolink:/^<([^ <>]+(@|:\/)[^ <>]+)>/,url:h,tag:/^<!--[\s\S]*?-->|^<\/?\w+(?:"[^"]*"|'[^']*'|[^<'">])*?>/,link:/^!?\[(inside)\]\(href\)/,reflink:/^!?\[(inside)\]\s*\[([^\]]*)\]/,nolink:/^!?\[((?:\[[^\]]*\]|[^\[\]])*)\]/,strong:/^__([\s\S]+?)__(?!_)|^\*\*([\s\S]+?)\*\*(?!\*)/,em:/^\b_((?:[^_]|__)+?)_\b|^\*((?:\*\*|[\s\S])+?)\*(?!\*)/,code:/^(`+)([\s\S]*?[^`])\1(?!`)/,br:/^ {2,}\n(?!\s*$)/,del:h,text:/^[\s\S]+?(?=[\\<!\[_*`]| {2,}\n|$)/};g._inside=/(?:\[[^\]]*\]|\\[\[\]]|[^\[\]]|\](?=[^\[]*\]))*/,g._href=/\s*<?([\s\S]*?)>?(?:\s+['"]([\s\S]*?)['"])?\s*/,g.link=l(g.link)("inside",g._inside)("href",g._href)(),g.reflink=l(g.reflink)("inside",g._inside)(),g.normal=p({},g),g.pedantic=p({},g.normal,{strong:/^__(?=\S)([\s\S]*?\S)__(?!_)|^\*\*(?=\S)([\s\S]*?\S)\*\*(?!\*)/,em:/^_(?=\S)([\s\S]*?\S)_(?!_)|^\*(?=\S)([\s\S]*?\S)\*(?!\*)/}),g.gfm=p({},g.normal,{escape:l(g.escape)("])","~|])")(),url:/^(https?:\/\/[^\s<]+[^<.,:;"')\]\s])/,del:/^~~(?=\S)([\s\S]*?\S)~~/,text:l(g.text)("]|","~]|")("|","|https?://|")()}),g.breaks=p({},g.gfm,{br:l(g.br)("{2,}","*")(),text:l(g.gfm.text)("{2,}","*")()}),n.rules=g,n.output=function(t,e,r){return new n(e,r).output(t)},n.prototype.output=function(t){for(var e,n,r,i,o="";t;)if(i=this.rules.escape.exec(t))t=t.substring(i[0].length),o+=i[1];else if(i=this.rules.autolink.exec(t))t=t.substring(i[0].length),"@"===i[2]?(n=s(":"===i[1].charAt(6)?this.mangle(i[1].substring(7)):this.mangle(i[1])),r=this.mangle("mailto:")+n):(n=s(i[1]),r=n),o+=this.renderer.link(r,null,n);else if(this.inLink||!(i=this.rules.url.exec(t))){if(i=this.rules.tag.exec(t))!this.inLink&&/^<a /i.test(i[0])?this.inLink=!0:this.inLink&&/^<\/a>/i.test(i[0])&&(this.inLink=!1),t=t.substring(i[0].length),o+=this.options.sanitize?this.options.sanitizer?this.options.sanitizer(i[0]):s(i[0]):i[0];else if(i=this.rules.link.exec(t))t=t.substring(i[0].length),this.inLink=!0,o+=this.outputLink(i,{href:i[2],title:i[3]}),this.inLink=!1;else if((i=this.rules.reflink.exec(t))||(i=this.rules.nolink.exec(t))){if(t=t.substring(i[0].length),e=(i[2]||i[1]).replace(/\s+/g," "),!(e=this.links[e.toLowerCase()])||!e.href){o+=i[0].charAt(0),t=i[0].substring(1)+t;continue}this.inLink=!0,o+=this.outputLink(i,e),this.inLink=!1}else if(i=this.rules.strong.exec(t))t=t.substring(i[0].length),o+=this.renderer.strong(this.output(i[2]||i[1]));else if(i=this.rules.em.exec(t))t=t.substring(i[0].length),o+=this.renderer.em(this.output(i[2]||i[1]));else if(i=this.rules.code.exec(t))t=t.substring(i[0].length),o+=this.renderer.codespan(s(i[2].trim(),!0));else if(i=this.rules.br.exec(t))t=t.substring(i[0].length),o+=this.renderer.br();else if(i=this.rules.del.exec(t))t=t.substring(i[0].length),o+=this.renderer.del(this.output(i[1]));else if(i=this.rules.text.exec(t))t=t.substring(i[0].length),o+=this.renderer.text(s(this.smartypants(i[0])));else if(t)throw new Error("Infinite loop on byte: "+t.charCodeAt(0))}else t=t.substring(i[0].length),n=s(i[1]),r=n,o+=this.renderer.link(r,null,n);return o},n.prototype.outputLink=function(t,e){var n=s(e.href),r=e.title?s(e.title):null;return"!"!==t[0].charAt(0)?this.renderer.link(n,r,this.output(t[1])):this.renderer.image(n,r,s(t[1]))},n.prototype.smartypants=function(t){return this.options.smartypants?t.replace(/---/g,"—").replace(/--/g,"–").replace(/(^|[-\u2014\/(\[{"\s])'/g,"$1‘").replace(/'/g,"’").replace(/(^|[-\u2014\/(\[{\u2018\s])"/g,"$1“").replace(/"/g,"”").replace(/\.{3}/g,"…"):t},n.prototype.mangle=function(t){if(!this.options.mangle)return t;for(var e,n="",r=t.length,i=0;i<r;i++)e=t.charCodeAt(i),Math.random()>.5&&(e="x"+e.toString(16)),n+="&#"+e+";";return n},r.prototype.code=function(t,e,n){if(this.options.highlight){var r=this.options.highlight(t,e);null!=r&&r!==t&&(n=!0,t=r)}return e?'<pre><code class="'+this.options.langPrefix+s(e,!0)+'">'+(n?t:s(t,!0))+"\n</code></pre>\n":"<pre><code>"+(n?t:s(t,!0))+"\n</code></pre>"},r.prototype.blockquote=function(t){return"<blockquote>\n"+t+"</blockquote>\n"},r.prototype.html=function(t){return t},r.prototype.heading=function(t,e,n){return"<h"+e+' id="'+this.options.headerPrefix+n.toLowerCase().replace(/[^\w]+/g,"-")+'">'+t+"</h"+e+">\n"},r.prototype.hr=function(){return this.options.xhtml?"<hr/>\n":"<hr>\n"},r.prototype.list=function(t,e){var n=e?"ol":"ul";return"<"+n+">\n"+t+"</"+n+">\n"},r.prototype.listitem=function(t){return"<li>"+t+"</li>\n"},r.prototype.paragraph=function(t){return"<p>"+t+"</p>\n"},r.prototype.table=function(t,e){return"<table>\n<thead>\n"+t+"</thead>\n<tbody>\n"+e+"</tbody>\n</table>\n"},r.prototype.tablerow=function(t){return"<tr>\n"+t+"</tr>\n"},r.prototype.tablecell=function(t,e){var n=e.header?"th":"td";return(e.align?"<"+n+' style="text-align:'+e.align+'">':"<"+n+">")+t+"</"+n+">\n"},r.prototype.strong=function(t){return"<strong>"+t+"</strong>"},r.prototype.em=function(t){return"<em>"+t+"</em>"},r.prototype.codespan=function(t){return"<code>"+t+"</code>"},r.prototype.br=function(){return this.options.xhtml?"<br/>":"<br>"},r.prototype.del=function(t){return"<del>"+t+"</del>"},r.prototype.link=function(t,e,n){if(this.options.sanitize){try{var r=decodeURIComponent(o(t)).replace(/[^\w:]/g,"").toLowerCase()}catch(t){return n}if(0===r.indexOf("javascript:")||0===r.indexOf("vbscript:")||0===r.indexOf("data:"))return n}this.options.baseUrl&&!d.test(t)&&(t=a(this.options.baseUrl,t));var i='<a href="'+t+'"';return e&&(i+=' title="'+e+'"'),i+=">"+n+"</a>"},r.prototype.image=function(t,e,n){this.options.baseUrl&&!d.test(t)&&(t=a(this.options.baseUrl,t));var r='<img src="'+t+'" alt="'+n+'"';return e&&(r+=' title="'+e+'"'),r+=this.options.xhtml?"/>":">"},r.prototype.text=function(t){return t},i.parse=function(t,e,n){return new i(e,n).parse(t)},i.prototype.parse=function(t){this.inline=new n(t.links,this.options,this.renderer),this.tokens=t.reverse();for(var e="";this.next();)e+=this.tok();return e},i.prototype.next=function(){return this.token=this.tokens.pop()},i.prototype.peek=function(){return this.tokens[this.tokens.length-1]||0},i.prototype.parseText=function(){for(var t=this.token.text;"text"===this.peek().type;)t+="\n"+this.next().text;return this.inline.output(t)},i.prototype.tok=function(){switch(this.token.type){case"space":return"";case"hr":return this.renderer.hr();case"heading":return this.renderer.heading(this.inline.output(this.token.text),this.token.depth,this.token.text);case"code":return this.renderer.code(this.token.text,this.token.lang,this.token.escaped);case"table":var t,e,n,r,i="",s="";for(n="",t=0;t<this.token.header.length;t++)({header:!0,align:this.token.align[t]}),n+=this.renderer.tablecell(this.inline.output(this.token.header[t]),{header:!0,align:this.token.align[t]});for(i+=this.renderer.tablerow(n),t=0;t<this.token.cells.length;t++){for(e=this.token.cells[t],n="",r=0;r<e.length;r++)n+=this.renderer.tablecell(this.inline.output(e[r]),{header:!1,align:this.token.align[r]});s+=this.renderer.tablerow(n)}return this.renderer.table(i,s);case"blockquote_start":for(var s="";"blockquote_end"!==this.next().type;)s+=this.tok();return this.renderer.blockquote(s);case"list_start":for(var s="",o=this.token.ordered;"list_end"!==this.next().type;)s+=this.tok();return this.renderer.list(s,o);case"list_item_start":for(var s="";"list_item_end"!==this.next().type;)s+="text"===this.token.type?this.parseText():this.tok();return this.renderer.listitem(s);case"loose_item_start":for(var s="";"list_item_end"!==this.next().type;)s+=this.tok();return this.renderer.listitem(s);case"html":var l=this.token.pre||this.options.pedantic?this.token.text:this.inline.output(this.token.text);return this.renderer.html(l);case"paragraph":return this.renderer.paragraph(this.inline.output(this.token.text));case"text":return this.renderer.paragraph(this.parseText())}};var f={},d=/^$|^[a-z][a-z0-9+.-]*:|^[?#]/i;h.exec=h,u.options=u.setOptions=function(t){return p(u.defaults,t),u},u.defaults={gfm:!0,tables:!0,breaks:!1,pedantic:!1,sanitize:!1,sanitizer:null,mangle:!0,smartLists:!1,silent:!1,highlight:null,langPrefix:"lang-",smartypants:!1,headerPrefix:"",renderer:new r,xhtml:!1,baseUrl:null},u.Parser=i,u.parser=i.parse,u.Renderer=r,u.Lexer=e,u.lexer=e.lex,u.InlineLexer=n,u.inlineLexer=n.output,u.parse=u,t.exports=u}).call(function(){return this||("undefined"!=typeof window?window:e)}())}).call(e,n("DuR2"))},EIGv:function(t,e,n){var r=n("glwu");"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);n("rjj0")("409e1b6e",r,!0,{})},GwPc:function(t,e,n){"use strict";var r=n("EFqf"),i=n.n(r);i.a.setOptions({renderer:new i.a.Renderer,gfm:!0,tables:!0,breaks:!0,pedantic:!1,sanitize:!1,smartLists:!0,smartypants:!1});var s=new i.a.Renderer,o=function(t){return"<p>"+t+"</p>"},l=function(t,e,n){var r=t.includes("readup.tips"),i=n.includes("<img");return('<a href="'+t+'" \n             target="_blank"\n             title="'+(e||(i?t:n))+'" \n             '+(r?"":'rel="external nofollow noopener noreferrer"')+">"+n+"\n          </a>").replace(/\s+/g," ").replace("\n","")},a=function(t,e,n){return('<a href="'+t+'" \n             target="_blank" rel="nofollow noopener noreferrer">\n            <img src="'+t+'" \n                title="'+(e||n||"readup.tips")+'" \n                style="width:10%; height:15%"\n                alt="'+(n||e||t)+'"/>\n          </a>').replace(/\s+/g," ").replace("\n","")};s.link=l,s.image=a,s.paragraph=o,e.a=function(t){return"string"!=typeof t?"":i()(t,{renderer:s})}},JARo:function(t,e,n){"use strict";var r=n("Gu7T"),i=n.n(r),s=n("+SxW"),o=n("P9l9");e.a={name:"profile-clip",components:{Clip:s.a},data:function(){return{clips:[],currentPage:1,clipCount:0}},computed:{hasMore:function(){return this.clips.length<this.clipCount}},created:function(){this.loadClips()},methods:{loadmoreClip:function(){var t=this,e=this.$route.params.id,n={userid:e,page:this.currentPage};Object(o.J)(n).then(function(e){var n;(n=t.clips).push.apply(n,i()(e.data.clips)),t.currentPage+=1})},loadClips:function(){var t=this,e=this.$route.params.id,n={userid:e};Object(o.J)(n).then(function(e){var n=e.data;t.clips=n.clips,t.clipCount=n.total})}}}},N0sn:function(t,e,n){"use strict";n.d(e,"a",function(){return r}),n.d(e,"b",function(){return i});var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"clip-list"},[n("b",[t._v("CLIPS "+t._s(t.clipCount))]),t._v(" "),t._l(t.clips,function(t){return n("clip",{key:t.id,attrs:{clip:t}})}),t._v(" "),t.hasMore?n("div",[n("el-button",{staticClass:"blockbtn",attrs:{size:"mini",disabled:!t.hasMore},on:{click:t.loadmoreClip}},[t._v("\n               Show More\n    ")])],1):t._e()],2)},i=[]},Ti2K:function(t,e,n){"use strict";function r(t){n("x7Yh")}Object.defineProperty(e,"__esModule",{value:!0});var i=n("JARo"),s=n("N0sn"),o=n("XyMi"),l=r,a=Object(o.a)(i.a,s.a,s.b,!1,l,"data-v-37037c58",null);e.default=a.exports},"Y/D9":function(t,e,n){"use strict";n.d(e,"a",function(){return r}),n.d(e,"b",function(){return i});var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"clip-main"},[n("div",{staticClass:"clipbody"},[n("span",{staticClass:"quoteleft"},[t._v("“")]),t._v(" "),n("span",{domProps:{innerHTML:t._s(t.clipContent)}})]),t._v(" "),n("div",{staticClass:"meta"},[t._v("\n    From \n    "),n("router-link",{attrs:{to:"/item/"+t.fromitem.id,title:t.fromitem.title}},[t._v("\n      "+t._s(t.fromitem.title.slice(0,42))+"...\n    ")]),t._v("\n    via \n    "),n("router-link",{attrs:{to:"/profile/"+t.creator.id}},[t._v("\n      "+t._s(t.creator.name.slice(0,15))+"\n    ")]),t._v("\n    | "+t._s(t._f("toMDY")(t.clip.timestamp))+"\n    | "+t._s(t.vote)+" "),n("el-button",{attrs:{type:"text"},on:{click:t.upClip}},[t._v("Like")])],1)])},i=[]},glwu:function(t,e,n){e=t.exports=n("FZ+f")(!1),e.push([t.i,".clip-main[data-v-59f81342]{background-color:#fbfbf9;padding:5px;border-bottom:1px solid #eee;position:relative}.clip-main .meta[data-v-59f81342]{font-size:.75em;text-align:right}.clip-main .meta a[data-v-59f81342]:hover{color:red}.clip-main .clipbody[data-v-59f81342]{background-color:#f6f6f1;padding:8px;font-size:1.05em;color:#2b2117;position:relative}.clip-main .clipbody .quoteleft[data-v-59f81342]{position:absolute;top:10px;left:0;color:gray}",""])},uj7J:function(t,e,n){e=t.exports=n("FZ+f")(!1),e.push([t.i,".clip-list[data-v-37037c58]{padding:auto}",""])},x7Yh:function(t,e,n){var r=n("uj7J");"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);n("rjj0")("3b9b687c",r,!0,{})}});
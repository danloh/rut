webpackJsonp([6],{"+lgA":function(t,e,n){"use strict";var r=n("P9l9"),i=n("iF09");e.a={name:"demand",props:["demand"],data:function(){return{vote:this.demand.vote,answercount:this.demand.answercount}},computed:{requestor:function(){return this.demand.requestor}},methods:{upDemand:function(){var t=this;if(Object(i.a)()){var e=this.demand.id;Object(r._44)(e).then(function(e){t.vote=e.data})}}}}},AWnP:function(t,e,n){e=t.exports=n("FZ+f")(!1),e.push([t.i,".demand-list[data-v-eb82bcd6]{padding:auto}",""])},D3Jz:function(t,e,n){"use strict";var r=n("6aq2"),i=n("GwPc");e.a={name:"rut-sum",props:["rut"],computed:{cover:function(){return this.rut.cover},intro:function(){var t=Object(i.a)(this.rut.intro);return Object(r.showLess)(t)}}}},EFqf:function(t,e,n){(function(e){!function(e){"use strict";function n(t){this.tokens=[],this.tokens.links={},this.options=t||d.defaults,this.rules=g.normal,this.options.gfm&&(this.options.tables?this.rules=g.tables:this.rules=g.gfm)}function r(t,e){if(this.options=e||d.defaults,this.links=t,this.rules=f.normal,this.renderer=this.options.renderer||new i,this.renderer.options=this.options,!this.links)throw new Error("Tokens array requires a `links` property.");this.options.gfm?this.options.breaks?this.rules=f.breaks:this.rules=f.gfm:this.options.pedantic&&(this.rules=f.pedantic)}function i(t){this.options=t||{}}function s(){}function a(t){this.tokens=[],this.token=null,this.options=t||d.defaults,this.options.renderer=this.options.renderer||new i,this.renderer=this.options.renderer,this.renderer.options=this.options}function o(t,e){return t.replace(e?/&/g:/&(?!#?\w+;)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}function l(t){return t.replace(/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/gi,function(t,e){return e=e.toLowerCase(),"colon"===e?":":"#"===e.charAt(0)?"x"===e.charAt(1)?String.fromCharCode(parseInt(e.substring(2),16)):String.fromCharCode(+e.substring(1)):""})}function u(t,e){return t=t.source,e=e||"",{replace:function(e,n){return n=n.source||n,n=n.replace(/(^|[^\[])\^/g,"$1"),t=t.replace(e,n),this},getRegex:function(){return new RegExp(t,e)}}}function c(t,e){return m[" "+t]||(/^[^:]+:\/*[^\/]*$/.test(t)?m[" "+t]=t+"/":m[" "+t]=t.replace(/[^\/]*$/,"")),t=m[" "+t],"//"===e.slice(0,2)?t.replace(/:[\s\S]*/,":")+e:"/"===e.charAt(0)?t.replace(/(:\/*[^\/]*)[\s\S]*/,"$1")+e:t+e}function p(){}function h(t){for(var e,n,r=1;r<arguments.length;r++){e=arguments[r];for(n in e)Object.prototype.hasOwnProperty.call(e,n)&&(t[n]=e[n])}return t}function d(t,e,r){if(void 0===t||null===t)throw new Error("marked(): input parameter is undefined or null");if("string"!=typeof t)throw new Error("marked(): input parameter is of type "+Object.prototype.toString.call(t)+", string expected");if(r||"function"==typeof e){r||(r=e,e=null),e=h({},d.defaults,e||{});var i,s,l=e.highlight,u=0;try{i=n.lex(t,e)}catch(t){return r(t)}s=i.length;var c=function(t){if(t)return e.highlight=l,r(t);var n;try{n=a.parse(i,e)}catch(e){t=e}return e.highlight=l,t?r(t):r(null,n)};if(!l||l.length<3)return c();if(delete e.highlight,!s)return c();for(;u<i.length;u++)!function(t){"code"!==t.type?--s||c():l(t.text,t.lang,function(e,n){return e?c(e):null==n||n===t.text?--s||c():(t.text=n,t.escaped=!0,void(--s||c()))})}(i[u])}else try{return e&&(e=h({},d.defaults,e)),a.parse(n.lex(t,e),e)}catch(t){if(t.message+="\nPlease report this to https://github.com/chjj/marked.",(e||d.defaults).silent)return"<p>An error occurred:</p><pre>"+o(t.message+"",!0)+"</pre>";throw t}}var g={newline:/^\n+/,code:/^( {4}[^\n]+\n*)+/,fences:p,hr:/^ {0,3}((?:- *){3,}|(?:_ *){3,}|(?:\* *){3,})(?:\n+|$)/,heading:/^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)/,nptable:p,blockquote:/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/,list:/^( *)(bull) [\s\S]+?(?:hr|def|\n{2,}(?! )(?!\1bull )\n*|\s*$)/,html:/^ *(?:comment *(?:\n|\s*$)|closed *(?:\n{2,}|\s*$)|closing *(?:\n{2,}|\s*$))/,def:/^ {0,3}\[(label)\]: *\n? *<?([^\s>]+)>?(?:(?: +\n? *| *\n *)(title))? *(?:\n+|$)/,table:p,lheading:/^([^\n]+)\n *(=|-){2,} *(?:\n+|$)/,paragraph:/^([^\n]+(?:\n?(?!hr|heading|lheading| {0,3}>|tag)[^\n]+)+)/,text:/^[^\n]+/};g._label=/(?:\\[\[\]]|[^\[\]])+/,g._title=/(?:"(?:\\"|[^"]|"[^"\n]*")*"|'\n?(?:[^'\n]+\n?)*'|\([^()]*\))/,g.def=u(g.def).replace("label",g._label).replace("title",g._title).getRegex(),g.bullet=/(?:[*+-]|\d+\.)/,g.item=/^( *)(bull) [^\n]*(?:\n(?!\1bull )[^\n]*)*/,g.item=u(g.item,"gm").replace(/bull/g,g.bullet).getRegex(),g.list=u(g.list).replace(/bull/g,g.bullet).replace("hr","\\n+(?=\\1?(?:(?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$))").replace("def","\\n+(?="+g.def.source+")").getRegex(),g._tag="(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b",g.html=u(g.html).replace("comment",/<!--[\s\S]*?-->/).replace("closed",/<(tag)[\s\S]+?<\/\1>/).replace("closing",/<tag(?:"[^"]*"|'[^']*'|\s[^'"\/>\s]*)*?\/?>/).replace(/tag/g,g._tag).getRegex(),g.paragraph=u(g.paragraph).replace("hr",g.hr).replace("heading",g.heading).replace("lheading",g.lheading).replace("tag","<"+g._tag).getRegex(),g.blockquote=u(g.blockquote).replace("paragraph",g.paragraph).getRegex(),g.normal=h({},g),g.gfm=h({},g.normal,{fences:/^ *(`{3,}|~{3,})[ \.]*(\S+)? *\n([\s\S]*?)\n? *\1 *(?:\n+|$)/,paragraph:/^/,heading:/^ *(#{1,6}) +([^\n]+?) *#* *(?:\n+|$)/}),g.gfm.paragraph=u(g.paragraph).replace("(?!","(?!"+g.gfm.fences.source.replace("\\1","\\2")+"|"+g.list.source.replace("\\1","\\3")+"|").getRegex(),g.tables=h({},g.gfm,{nptable:/^ *(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)\n*/,table:/^ *\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*/}),n.rules=g,n.lex=function(t,e){return new n(e).lex(t)},n.prototype.lex=function(t){return t=t.replace(/\r\n|\r/g,"\n").replace(/\t/g,"    ").replace(/\u00a0/g," ").replace(/\u2424/g,"\n"),this.token(t,!0)},n.prototype.token=function(t,e){t=t.replace(/^ +$/gm,"");for(var n,r,i,s,a,o,l,u,c,p;t;)if((i=this.rules.newline.exec(t))&&(t=t.substring(i[0].length),i[0].length>1&&this.tokens.push({type:"space"})),i=this.rules.code.exec(t))t=t.substring(i[0].length),i=i[0].replace(/^ {4}/gm,""),this.tokens.push({type:"code",text:this.options.pedantic?i:i.replace(/\n+$/,"")});else if(i=this.rules.fences.exec(t))t=t.substring(i[0].length),this.tokens.push({type:"code",lang:i[2],text:i[3]||""});else if(i=this.rules.heading.exec(t))t=t.substring(i[0].length),this.tokens.push({type:"heading",depth:i[1].length,text:i[2]});else if(e&&(i=this.rules.nptable.exec(t))){for(t=t.substring(i[0].length),o={type:"table",header:i[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:i[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:i[3].replace(/\n$/,"").split("\n")},u=0;u<o.align.length;u++)/^ *-+: *$/.test(o.align[u])?o.align[u]="right":/^ *:-+: *$/.test(o.align[u])?o.align[u]="center":/^ *:-+ *$/.test(o.align[u])?o.align[u]="left":o.align[u]=null;for(u=0;u<o.cells.length;u++)o.cells[u]=o.cells[u].split(/ *\| */);this.tokens.push(o)}else if(i=this.rules.hr.exec(t))t=t.substring(i[0].length),this.tokens.push({type:"hr"});else if(i=this.rules.blockquote.exec(t))t=t.substring(i[0].length),this.tokens.push({type:"blockquote_start"}),i=i[0].replace(/^ *> ?/gm,""),this.token(i,e),this.tokens.push({type:"blockquote_end"});else if(i=this.rules.list.exec(t)){for(t=t.substring(i[0].length),s=i[2],this.tokens.push({type:"list_start",ordered:s.length>1}),i=i[0].match(this.rules.item),n=!1,p=i.length,u=0;u<p;u++)o=i[u],l=o.length,o=o.replace(/^ *([*+-]|\d+\.) +/,""),~o.indexOf("\n ")&&(l-=o.length,o=this.options.pedantic?o.replace(/^ {1,4}/gm,""):o.replace(new RegExp("^ {1,"+l+"}","gm"),"")),this.options.smartLists&&u!==p-1&&(a=g.bullet.exec(i[u+1])[0],s===a||s.length>1&&a.length>1||(t=i.slice(u+1).join("\n")+t,u=p-1)),r=n||/\n\n(?!\s*$)/.test(o),u!==p-1&&(n="\n"===o.charAt(o.length-1),r||(r=n)),this.tokens.push({type:r?"loose_item_start":"list_item_start"}),this.token(o,!1),this.tokens.push({type:"list_item_end"});this.tokens.push({type:"list_end"})}else if(i=this.rules.html.exec(t))t=t.substring(i[0].length),this.tokens.push({type:this.options.sanitize?"paragraph":"html",pre:!this.options.sanitizer&&("pre"===i[1]||"script"===i[1]||"style"===i[1]),text:i[0]});else if(e&&(i=this.rules.def.exec(t)))t=t.substring(i[0].length),i[3]&&(i[3]=i[3].substring(1,i[3].length-1)),c=i[1].toLowerCase(),this.tokens.links[c]||(this.tokens.links[c]={href:i[2],title:i[3]});else if(e&&(i=this.rules.table.exec(t))){for(t=t.substring(i[0].length),o={type:"table",header:i[1].replace(/^ *| *\| *$/g,"").split(/ *\| */),align:i[2].replace(/^ *|\| *$/g,"").split(/ *\| */),cells:i[3].replace(/(?: *\| *)?\n$/,"").split("\n")},u=0;u<o.align.length;u++)/^ *-+: *$/.test(o.align[u])?o.align[u]="right":/^ *:-+: *$/.test(o.align[u])?o.align[u]="center":/^ *:-+ *$/.test(o.align[u])?o.align[u]="left":o.align[u]=null;for(u=0;u<o.cells.length;u++)o.cells[u]=o.cells[u].replace(/^ *\| *| *\| *$/g,"").split(/ *\| */);this.tokens.push(o)}else if(i=this.rules.lheading.exec(t))t=t.substring(i[0].length),this.tokens.push({type:"heading",depth:"="===i[2]?1:2,text:i[1]});else if(e&&(i=this.rules.paragraph.exec(t)))t=t.substring(i[0].length),this.tokens.push({type:"paragraph",text:"\n"===i[1].charAt(i[1].length-1)?i[1].slice(0,-1):i[1]});else if(i=this.rules.text.exec(t))t=t.substring(i[0].length),this.tokens.push({type:"text",text:i[0]});else if(t)throw new Error("Infinite loop on byte: "+t.charCodeAt(0));return this.tokens};var f={escape:/^\\([\\`*{}\[\]()#+\-.!_>])/,autolink:/^<(scheme:[^\s\x00-\x1f<>]*|email)>/,url:p,tag:/^<!--[\s\S]*?-->|^<\/?[a-zA-Z0-9\-]+(?:"[^"]*"|'[^']*'|\s[^<'">\/\s]*)*?\/?>/,link:/^!?\[(inside)\]\(href\)/,reflink:/^!?\[(inside)\]\s*\[([^\]]*)\]/,nolink:/^!?\[((?:\[[^\[\]]*\]|\\[\[\]]|[^\[\]])*)\]/,strong:/^__([\s\S]+?)__(?!_)|^\*\*([\s\S]+?)\*\*(?!\*)/,em:/^_([^\s_](?:[^_]|__)+?[^\s_])_\b|^\*((?:\*\*|[^*])+?)\*(?!\*)/,code:/^(`+)\s*([\s\S]*?[^`]?)\s*\1(?!`)/,br:/^ {2,}\n(?!\s*$)/,del:p,text:/^[\s\S]+?(?=[\\<!\[`*]|\b_| {2,}\n|$)/};f._scheme=/[a-zA-Z][a-zA-Z0-9+.-]{1,31}/,f._email=/[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/,f.autolink=u(f.autolink).replace("scheme",f._scheme).replace("email",f._email).getRegex(),f._inside=/(?:\[[^\[\]]*\]|\\[\[\]]|[^\[\]]|\](?=[^\[]*\]))*/,f._href=/\s*<?([\s\S]*?)>?(?:\s+['"]([\s\S]*?)['"])?\s*/,f.link=u(f.link).replace("inside",f._inside).replace("href",f._href).getRegex(),f.reflink=u(f.reflink).replace("inside",f._inside).getRegex(),f.normal=h({},f),f.pedantic=h({},f.normal,{strong:/^__(?=\S)([\s\S]*?\S)__(?!_)|^\*\*(?=\S)([\s\S]*?\S)\*\*(?!\*)/,em:/^_(?=\S)([\s\S]*?\S)_(?!_)|^\*(?=\S)([\s\S]*?\S)\*(?!\*)/}),f.gfm=h({},f.normal,{escape:u(f.escape).replace("])","~|])").getRegex(),url:u(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/).replace("email",f._email).getRegex(),_backpedal:/(?:[^?!.,:;*_~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_~)]+(?!$))+/,del:/^~~(?=\S)([\s\S]*?\S)~~/,text:u(f.text).replace("]|","~]|").replace("|","|https?://|ftp://|www\\.|[a-zA-Z0-9.!#$%&'*+/=?^_`{\\|}~-]+@|").getRegex()}),f.breaks=h({},f.gfm,{br:u(f.br).replace("{2,}","*").getRegex(),text:u(f.gfm.text).replace("{2,}","*").getRegex()}),r.rules=f,r.output=function(t,e,n){return new r(e,n).output(t)},r.prototype.output=function(t){for(var e,n,r,i,s="";t;)if(i=this.rules.escape.exec(t))t=t.substring(i[0].length),s+=i[1];else if(i=this.rules.autolink.exec(t))t=t.substring(i[0].length),"@"===i[2]?(n=o(this.mangle(i[1])),r="mailto:"+n):(n=o(i[1]),r=n),s+=this.renderer.link(r,null,n);else if(this.inLink||!(i=this.rules.url.exec(t))){if(i=this.rules.tag.exec(t))!this.inLink&&/^<a /i.test(i[0])?this.inLink=!0:this.inLink&&/^<\/a>/i.test(i[0])&&(this.inLink=!1),t=t.substring(i[0].length),s+=this.options.sanitize?this.options.sanitizer?this.options.sanitizer(i[0]):o(i[0]):i[0];else if(i=this.rules.link.exec(t))t=t.substring(i[0].length),this.inLink=!0,s+=this.outputLink(i,{href:i[2],title:i[3]}),this.inLink=!1;else if((i=this.rules.reflink.exec(t))||(i=this.rules.nolink.exec(t))){if(t=t.substring(i[0].length),e=(i[2]||i[1]).replace(/\s+/g," "),!(e=this.links[e.toLowerCase()])||!e.href){s+=i[0].charAt(0),t=i[0].substring(1)+t;continue}this.inLink=!0,s+=this.outputLink(i,e),this.inLink=!1}else if(i=this.rules.strong.exec(t))t=t.substring(i[0].length),s+=this.renderer.strong(this.output(i[2]||i[1]));else if(i=this.rules.em.exec(t))t=t.substring(i[0].length),s+=this.renderer.em(this.output(i[2]||i[1]));else if(i=this.rules.code.exec(t))t=t.substring(i[0].length),s+=this.renderer.codespan(o(i[2].trim(),!0));else if(i=this.rules.br.exec(t))t=t.substring(i[0].length),s+=this.renderer.br();else if(i=this.rules.del.exec(t))t=t.substring(i[0].length),s+=this.renderer.del(this.output(i[1]));else if(i=this.rules.text.exec(t))t=t.substring(i[0].length),s+=this.renderer.text(o(this.smartypants(i[0])));else if(t)throw new Error("Infinite loop on byte: "+t.charCodeAt(0))}else i[0]=this.rules._backpedal.exec(i[0])[0],t=t.substring(i[0].length),"@"===i[2]?(n=o(i[0]),r="mailto:"+n):(n=o(i[0]),r="www."===i[1]?"http://"+n:n),s+=this.renderer.link(r,null,n);return s},r.prototype.outputLink=function(t,e){var n=o(e.href),r=e.title?o(e.title):null;return"!"!==t[0].charAt(0)?this.renderer.link(n,r,this.output(t[1])):this.renderer.image(n,r,o(t[1]))},r.prototype.smartypants=function(t){return this.options.smartypants?t.replace(/---/g,"—").replace(/--/g,"–").replace(/(^|[-\u2014\/(\[{"\s])'/g,"$1‘").replace(/'/g,"’").replace(/(^|[-\u2014\/(\[{\u2018\s])"/g,"$1“").replace(/"/g,"”").replace(/\.{3}/g,"…"):t},r.prototype.mangle=function(t){if(!this.options.mangle)return t;for(var e,n="",r=t.length,i=0;i<r;i++)e=t.charCodeAt(i),Math.random()>.5&&(e="x"+e.toString(16)),n+="&#"+e+";";return n},i.prototype.code=function(t,e,n){if(this.options.highlight){var r=this.options.highlight(t,e);null!=r&&r!==t&&(n=!0,t=r)}return e?'<pre><code class="'+this.options.langPrefix+o(e,!0)+'">'+(n?t:o(t,!0))+"\n</code></pre>\n":"<pre><code>"+(n?t:o(t,!0))+"\n</code></pre>"},i.prototype.blockquote=function(t){return"<blockquote>\n"+t+"</blockquote>\n"},i.prototype.html=function(t){return t},i.prototype.heading=function(t,e,n){return"<h"+e+' id="'+this.options.headerPrefix+n.toLowerCase().replace(/[^\w]+/g,"-")+'">'+t+"</h"+e+">\n"},i.prototype.hr=function(){return this.options.xhtml?"<hr/>\n":"<hr>\n"},i.prototype.list=function(t,e){var n=e?"ol":"ul";return"<"+n+">\n"+t+"</"+n+">\n"},i.prototype.listitem=function(t){return"<li>"+t+"</li>\n"},i.prototype.paragraph=function(t){return"<p>"+t+"</p>\n"},i.prototype.table=function(t,e){return"<table>\n<thead>\n"+t+"</thead>\n<tbody>\n"+e+"</tbody>\n</table>\n"},i.prototype.tablerow=function(t){return"<tr>\n"+t+"</tr>\n"},i.prototype.tablecell=function(t,e){var n=e.header?"th":"td";return(e.align?"<"+n+' style="text-align:'+e.align+'">':"<"+n+">")+t+"</"+n+">\n"},i.prototype.strong=function(t){return"<strong>"+t+"</strong>"},i.prototype.em=function(t){return"<em>"+t+"</em>"},i.prototype.codespan=function(t){return"<code>"+t+"</code>"},i.prototype.br=function(){return this.options.xhtml?"<br/>":"<br>"},i.prototype.del=function(t){return"<del>"+t+"</del>"},i.prototype.link=function(t,e,n){if(this.options.sanitize){try{var r=decodeURIComponent(l(t)).replace(/[^\w:]/g,"").toLowerCase()}catch(t){return n}if(0===r.indexOf("javascript:")||0===r.indexOf("vbscript:")||0===r.indexOf("data:"))return n}this.options.baseUrl&&!b.test(t)&&(t=c(this.options.baseUrl,t));var i='<a href="'+t+'"';return e&&(i+=' title="'+e+'"'),i+=">"+n+"</a>"},i.prototype.image=function(t,e,n){this.options.baseUrl&&!b.test(t)&&(t=c(this.options.baseUrl,t));var r='<img src="'+t+'" alt="'+n+'"';return e&&(r+=' title="'+e+'"'),r+=this.options.xhtml?"/>":">"},i.prototype.text=function(t){return t},s.prototype.strong=s.prototype.em=s.prototype.codespan=s.prototype.del=s.prototype.text=function(t){return t},s.prototype.link=s.prototype.image=function(t,e,n){return""+n},s.prototype.br=function(){return""},a.parse=function(t,e){return new a(e).parse(t)},a.prototype.parse=function(t){this.inline=new r(t.links,this.options),this.inlineText=new r(t.links,h({},this.options,{renderer:new s})),this.tokens=t.reverse();for(var e="";this.next();)e+=this.tok();return e},a.prototype.next=function(){return this.token=this.tokens.pop()},a.prototype.peek=function(){return this.tokens[this.tokens.length-1]||0},a.prototype.parseText=function(){for(var t=this.token.text;"text"===this.peek().type;)t+="\n"+this.next().text;return this.inline.output(t)},a.prototype.tok=function(){switch(this.token.type){case"space":return"";case"hr":return this.renderer.hr();case"heading":return this.renderer.heading(this.inline.output(this.token.text),this.token.depth,l(this.inlineText.output(this.token.text)));case"code":return this.renderer.code(this.token.text,this.token.lang,this.token.escaped);case"table":var t,e,n,r,i="",s="";for(n="",t=0;t<this.token.header.length;t++)n+=this.renderer.tablecell(this.inline.output(this.token.header[t]),{header:!0,align:this.token.align[t]});for(i+=this.renderer.tablerow(n),t=0;t<this.token.cells.length;t++){for(e=this.token.cells[t],n="",r=0;r<e.length;r++)n+=this.renderer.tablecell(this.inline.output(e[r]),{header:!1,align:this.token.align[r]});s+=this.renderer.tablerow(n)}return this.renderer.table(i,s);case"blockquote_start":for(s="";"blockquote_end"!==this.next().type;)s+=this.tok();return this.renderer.blockquote(s);case"list_start":s="";for(var a=this.token.ordered;"list_end"!==this.next().type;)s+=this.tok();return this.renderer.list(s,a);case"list_item_start":for(s="";"list_item_end"!==this.next().type;)s+="text"===this.token.type?this.parseText():this.tok();return this.renderer.listitem(s);case"loose_item_start":for(s="";"list_item_end"!==this.next().type;)s+=this.tok();return this.renderer.listitem(s);case"html":var o=this.token.pre||this.options.pedantic?this.token.text:this.inline.output(this.token.text);return this.renderer.html(o);case"paragraph":return this.renderer.paragraph(this.inline.output(this.token.text));case"text":return this.renderer.paragraph(this.parseText())}};var m={},b=/^$|^[a-z][a-z0-9+.-]*:|^[?#]/i;p.exec=p,d.options=d.setOptions=function(t){return h(d.defaults,t),d},d.defaults={gfm:!0,tables:!0,breaks:!1,pedantic:!1,sanitize:!1,sanitizer:null,mangle:!0,smartLists:!1,silent:!1,highlight:null,langPrefix:"lang-",smartypants:!1,headerPrefix:"",renderer:new i,xhtml:!1,baseUrl:null},d.Parser=a,d.parser=a.parse,d.Renderer=i,d.TextRenderer=s,d.Lexer=n,d.lexer=n.lex,d.InlineLexer=r,d.inlineLexer=r.output,d.parse=d,t.exports=d}(this||"undefined"!=typeof window&&window)}).call(e,n("DuR2"))},GwPc:function(t,e,n){"use strict";var r=n("EFqf"),i=n.n(r);i.a.setOptions({renderer:new i.a.Renderer,gfm:!0,tables:!0,breaks:!0,pedantic:!1,sanitize:!1,smartLists:!0,smartypants:!1});var s=new i.a.Renderer,a=function(t){return"<p>"+t+"</p>"},o=function(t,e,n){var r=t.includes("readup.tips"),i=n.includes("<img");return('<a href="'+t+'" \n             target="_blank"\n             title="'+(e||(i?t:n))+'" \n             '+(r?"":'rel="external nofollow noopener noreferrer"')+">"+n+"\n          </a>").replace(/\s+/g," ").replace("\n","")},l=function(t,e,n){return('<a href="'+t+'" \n             target="_blank" rel="nofollow noopener noreferrer">\n            <img src="'+t+'" \n                title="'+(e||n||"readup.tips")+'" \n                style="width:10%; height:15%"\n                alt="'+(n||e||t)+'"/>\n          </a>').replace(/\s+/g," ").replace("\n","")};s.link=o,s.image=l,s.paragraph=a,e.a=function(t){return"string"!=typeof t?"":i()(t,{renderer:s})}},JAFF:function(t,e,n){"use strict";function r(t){n("yI0A")}var i=n("+lgA"),s=n("RaAj"),a=n("XyMi"),o=r,l=Object(a.a)(i.a,s.a,s.b,!1,o,"data-v-7efafcd7",null);e.a=l.exports},JlwC:function(t,e,n){var r=n("o9sI");"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);var i=n("rjj0").default;i("162ce1e0",r,!0,{})},RaAj:function(t,e,n){"use strict";n.d(e,"a",function(){return r}),n.d(e,"b",function(){return i});var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return t.requestor?n("div",{staticClass:"demand-main"},[n("div",{staticClass:"demand-body"},[n("router-link",{attrs:{to:"/demand/"+t.demand.id}},[n("b",[t._v(t._s(t.demand.body))])])],1),t._v(" "),n("div",{staticClass:"demand-bar"},[t._v("\n    - "),n("router-link",{attrs:{to:"/profile/"+t.requestor.id}},[t._v("\n        "+t._s(t.requestor.name)+"\n      ")]),t._v("\n    | "+t._s(t.vote)+" "),n("el-button",{attrs:{type:"text"},on:{click:t.upDemand}},[t._v("Upvote")]),t._v("\n    | "),n("router-link",{attrs:{to:"/create/"+t.demand.id}},[t._v("\n        "+t._s(t._f("pluralise")(t.answercount,"Answer"))+"  \n      ")]),t._v("\n    | "),n("router-link",{attrs:{to:"/demand/"+t.demand.id}},[t._v("\n        "+t._s(t._f("pluralise")(t.demand.commentcount,"Comment"))+"  \n      ")])],1)]):t._e()},i=[]},ao9o:function(t,e,n){"use strict";n.d(e,"a",function(){return r}),n.d(e,"b",function(){return i});var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"rut-sum"},[n("router-link",{attrs:{to:"/readuplist/"+t.rut.id}},[n("span",[n("img",{staticClass:"cover",staticStyle:{width:"80px",height:"100px"},attrs:{src:t.cover,alt:"Cover"}})]),t._v(" "),n("span",{staticClass:"title"},[n("router-link",{attrs:{to:"/readuplist/"+t.rut.id}},[t._v(" "+t._s(t.rut.title))])],1),t._v(" "),n("div",{staticClass:"intro",domProps:{innerHTML:t._s(t.intro)}})]),t._v(" "),n("span",{staticClass:"meta"},[n("span",[t._v(" ~| including "+t._s(t._f("pluralise")(t.rut.itemcount,"item"))+"  \n            | "),n("router-link",{attrs:{to:"/readuplist/"+t.rut.id}},[t._v("...See Detail")])],1)])],1)},i=[]},bhLB:function(t,e,n){e=t.exports=n("FZ+f")(!1),e.push([t.i,".rut-sum[data-v-5dbfa6f7]{background-color:#fcfdfc;min-height:120px;padding:10px 30px 10px 100px;border-bottom:2px solid #eee;position:relative}.rut-sum[data-v-5dbfa6f7]:hover{background-color:#fafaf8}.rut-sum .cover[data-v-5dbfa6f7]{position:absolute;top:10px;left:5px}.rut-sum .title[data-v-5dbfa6f7]{font-size:1.2em;font-weight:700;padding-top:10px}.rut-sum .title a[data-v-5dbfa6f7]:hover{color:#f60}.rut-sum .intro[data-v-5dbfa6f7]{color:#828282}.rut-sum .meta[data-v-5dbfa6f7]{font-size:.85em;color:#337ab7}",""])},"c/4n":function(t,e,n){var r=n("AWnP");"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);var i=n("rjj0").default;i("3eb0f5db",r,!0,{})},cgFa:function(t,e,n){"use strict";function r(t){n("i+C3")}var i=n("D3Jz"),s=n("ao9o"),a=n("XyMi"),o=r,l=Object(a.a)(i.a,s.a,s.b,!1,o,"data-v-5dbfa6f7",null);e.a=l.exports},emn9:function(t,e,n){"use strict";var r=n("Gu7T"),i=n.n(r),s=n("cgFa"),a=n("pxgU"),o=n("P9l9"),l=n("iF09"),u=n("6aq2");e.a={name:"tag-view",title:function(){return this.tagDetail.tagname},components:{RutSum:s.a,DemandList:a.a},data:function(){return{action:"Follow",favCount:0,openDialog:!1,tagDetail:{},tagForm:{name:"",parent:"",description:""},rules:{name:[{required:!0,validator:u.trimValid,message:"Need a Tag Name",trigger:"blur"},{max:120,message:"Max Length should be 120",trigger:"blur"}],parent:[{max:120,message:"Max Length should be 120",trigger:"blur"}],description:[{required:!0,validator:u.trimValid,message:"Please Descript it",trigger:"blur"},{max:500,message:"Max Length should be 500",trigger:"blur"}]},currentRuts:[],currentPage:0,totalRuts:0,relatedTags:[]}},computed:{tagid:function(){return this.tagDetail.id},tagName:function(){return this.tagDetail.tagname},hasMore:function(){return this.currentRuts.length<this.totalRuts}},methods:{loadmoreRuts:function(){var t=this;Object(o._10)(this.tagDetail.id,{page:this.currentPage}).then(function(e){var n;(n=t.currentRuts).push.apply(n,i()(e.data)),t.currentPage+=1})},loadData:function(){var t=this,e=this.$route.params.id;Object(o._9)(e).then(function(e){var n=e.data;t.currentRuts=n.ruts,t.totalRuts=n.total,t.currentPage=1,t.relatedTags=n.tags.slice(0,16),t.tagDetail=n,t.tagForm.name=n.tagname,t.tagForm.description=n.descript,t.favCount=n.favcount,t.action=t.checkFavor()})},toEditTag:function(){var t=this,e=this.$store.getters.currentUserID;e&&Object(l.a)()?Object(o.l)(e,this.tagid).then(function(e){e.data?t.$message("in Editing...Please Try Later"):(t.openDialog=!0,Object(o._18)(t.tagid))}):(this.openDialog=!1,this.$message("Please Log in to Continue"),this.$router.push({path:"/login",query:{redirect:this.$route.fullPath}}))},cancelEditTag:function(){this.openDialog=!1,Object(o._42)(this.tagid)},cancelOnClose:function(t){this.cancelEditTag(),t()},editTag:function(t,e){var n=this;this.$refs[t].validate(function(t){if(t&&Object(l.a)()){var r={name:e.name.trim(),parent:e.parent.trim(),description:e.description.trim()},i=n.tagDetail.id;Object(o.y)(i,r).then(function(t){n.openDialog=!1,Object(o._42)(n.tagid),n.loadData(),n.$message({showClose:!0,message:t.data,type:"success"})})}else Object(l.a)()||(n.$message({showClose:!0,message:"Please Log in to Continue"}),n.$router.push({path:"/login",query:{redirect:n.$route.fullPath}}))})},checkFavor:function(){var t=this;if(!Object(l.a)())return"Follow";var e=this.$route.params.id;Object(o.e)(e).then(function(e){t.action=e.data})},favTag:function(){var t=this;if(Object(l.a)()){var e=this.$route.params.id;"Follow"===this.action?Object(o.B)("fav",e).then(function(){t.action="UnFollow",t.favCount+=1}):Object(o.B)("unfav",e).then(function(){t.action="Follow",t.favCount-=1})}else this.$message({showClose:!0,message:"Should Log in to Continue"}),this.$router.push({path:"/login",query:{redirect:this.$route.fullPath}})}},watch:{$route:"loadData"},created:function(){this.loadData()}}},"i+C3":function(t,e,n){var r=n("bhLB");"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);var i=n("rjj0").default;i("cd54f28c",r,!0,{})},ma6q:function(t,e,n){"use strict";function r(t){n("JlwC")}Object.defineProperty(e,"__esModule",{value:!0});var i=n("emn9"),s=n("wn3H"),a=n("XyMi"),o=r,l=Object(a.a)(i.a,s.a,s.b,!1,o,"data-v-727d21a0",null);e.default=l.exports},o23n:function(t,e,n){"use strict";var r=n("Dd8w"),i=n.n(r),s=n("NYxO"),a=n("JAFF");e.a={name:"demand-list",components:{Demand:a.a},props:{type:String,userid:null,tag:String},computed:i()({},Object(s.b)(["currentDemands","currentD","maxD"]),{hasMore:function(){return this.currentD<this.maxD}}),methods:{initData:function(){var t={type:this.type,userid:this.userid,tag:this.tag};this.$store.dispatch("getDemands",t)},loadmoreDemand:function(){var t={type:this.type,userid:this.userid,tag:this.tag,page:this.currentD};this.$store.dispatch("moreDemands",t)}},created:function(){this.initData()}}},o9sI:function(t,e,n){e=t.exports=n("FZ+f")(!1),e.push([t.i,".tag-page[data-v-727d21a0]{padding:10px 230px 10px 0;position:relative}.tag-page .tag-side[data-v-727d21a0]{position:absolute;right:0;width:220px;background-color:#fafbfa}.tag-page .tag-side .sidetitle[data-v-727d21a0]{background-color:#e5ebe4;padding:5px 10px}.tag-page .tag-side .sidebody[data-v-727d21a0]{padding:5px 10px}.tag-page .tag-side .sidebody a[data-v-727d21a0]:hover{color:#f60}.tag-page .tagmeta[data-v-727d21a0]{background-color:#fff;min-height:40px;padding:5px 10px;margin-bottom:5px;position:relative}.tag-page .tagmeta .fbtn[data-v-727d21a0]{position:absolute;top:10px;right:5px}.tag-page .rut-list[data-v-727d21a0]{padding:auto}.tag-page .demand-list-title[data-v-727d21a0]{border-top:4px solid #eee;padding:10px 0}",""])},pxgU:function(t,e,n){"use strict";function r(t){n("c/4n")}var i=n("o23n"),s=n("vykR"),a=n("XyMi"),o=r,l=Object(a.a)(i.a,s.a,s.b,!1,o,"data-v-eb82bcd6",null);e.a=l.exports},vykR:function(t,e,n){"use strict";n.d(e,"a",function(){return r}),n.d(e,"b",function(){return i});var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"demand-list"},[t._l(t.currentDemands,function(t){return n("demand",{key:t.id,attrs:{demand:t}})}),t._v(" "),t.hasMore?n("div",[n("el-button",{staticClass:"blockbtn",attrs:{size:"mini",disabled:!t.hasMore},on:{click:t.loadmoreDemand}},[t._v("\n               Show More\n    ")])],1):t._e()],2)},i=[]},wn3H:function(t,e,n){"use strict";n.d(e,"a",function(){return r}),n.d(e,"b",function(){return i});var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"tag-page"},[n("div",{staticClass:"tag-side"},[n("h4",{staticClass:"sidetitle"},[t._v("Related Tags")]),t._v(" "),t._l(t.relatedTags,function(e,r){return n("div",{key:r,staticClass:"sidebody"},[n("router-link",{attrs:{to:"/tag/"+e.tagid}},[t._v(t._s(e.tagname))])],1)})],2),t._v(" "),n("div",{staticClass:"tagmeta"},[n("h4",[n("b",{staticStyle:{"font-size":"1.5em"}},[t._v(t._s(t.tagName))])]),t._v(" "),n("div",[t._v(t._s(t.tagDetail.descript)+" \n      "),n("el-button",{attrs:{type:"text"},on:{click:t.toEditTag}},[t._v("...Edit")])],1),t._v(" "),n("el-button",{staticClass:"fbtn",attrs:{type:"success",size:"mini",plain:""},on:{click:t.favTag}},[t._v(t._s(t.action)+" "+t._s(t.favCount)+"\n    ")])],1),t._v(" "),n("div",{staticClass:"rut-list"},t._l(t.currentRuts,function(t){return n("rut-sum",{key:t.id,attrs:{rut:t}})})),t._v(" "),t.hasMore?n("div",[n("el-button",{staticClass:"blockbtn",attrs:{size:"mini",disabled:!t.hasMore},on:{click:t.loadmoreRuts}},[t._v("\n               Show More\n    ")])],1):t._e(),t._v(" "),t.tagName?n("div",{staticClass:"demand-list"},[n("div",{staticClass:"demand-list-title"},[n("b",{staticStyle:{"font-size":"1.2em"}},[t._v("Related Requests on This Topic")]),t._v("      \n      "),n("router-link",{attrs:{to:"/demands"}},[t._v("Send a Request")])],1),t._v(" "),n("demand-list",{key:t.tagid,attrs:{type:"popular",tag:t.tagName}})],1):t._e(),t._v(" "),n("el-dialog",{attrs:{title:"Edit Tag Description",visible:t.openDialog,"before-close":t.cancelOnClose},on:{"update:visible":function(e){t.openDialog=e}}},[n("el-form",{ref:"tagForm",attrs:{model:t.tagForm,rules:t.rules,size:"mini"}},[n("el-form-item",{attrs:{label:"Tag Name",prop:"name"}},[n("el-input",{model:{value:t.tagForm.name,callback:function(e){t.$set(t.tagForm,"name",e)},expression:"tagForm.name"}})],1),t._v(" "),n("el-form-item",{attrs:{label:"Parent Tag",prop:"parent"}},[n("el-input",{model:{value:t.tagForm.parent,callback:function(e){t.$set(t.tagForm,"parent",e)},expression:"tagForm.parent"}})],1),t._v(" "),n("el-form-item",{attrs:{label:"Description",prop:"description"}},[n("el-input",{attrs:{type:"textarea",autosize:{minRows:3}},model:{value:t.tagForm.description,callback:function(e){t.$set(t.tagForm,"description",e)},expression:"tagForm.description"}})],1)],1),t._v(" "),n("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{on:{click:t.cancelEditTag}},[t._v("Cancel")]),t._v(" "),n("el-button",{attrs:{type:"success"},on:{click:function(e){t.editTag("tagForm",t.tagForm)}}},[t._v("\n        Submit\n      ")])],1)],1)],1)},i=[]},yI0A:function(t,e,n){var r=n("ywTJ");"string"==typeof r&&(r=[[t.i,r,""]]),r.locals&&(t.exports=r.locals);var i=n("rjj0").default;i("9b4c4168",r,!0,{})},ywTJ:function(t,e,n){e=t.exports=n("FZ+f")(!1),e.push([t.i,".demand-main[data-v-7efafcd7]{padding:10px;background-color:#f8f9fa;border-bottom:2px solid #eee}.demand-main .demand-body[data-v-7efafcd7]{font-size:1.05em}.demand-main .demand-body a[data-v-7efafcd7]{color:#00838f}.demand-main .demand-body a[data-v-7efafcd7]:hover{color:#409eff}.demand-main .demand-bar[data-v-7efafcd7]{font-size:.75em}",""])}});
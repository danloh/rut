webpackJsonp([25],{"+lgA":function(t,e,n){"use strict";var a=n("P9l9"),d=n("iF09");e.a={name:"demand",props:["demand"],data:function(){return{vote:this.demand.vote,answercount:this.demand.answercount}},computed:{requestor:function(){return this.demand.requestor}},methods:{upDemand:function(){var t=this;if(Object(d.a)()){var e=this.demand.id;Object(a._44)(e).then(function(e){t.vote=e.data})}}}}},CgPp:function(t,e,n){"use strict";n.d(e,"a",function(){return a}),n.d(e,"b",function(){return d});var a=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"demand-list"},[t._l(t.currentDemands,function(t){return n("demand",{key:t.id,attrs:{demand:t}})}),t._v(" "),t.hasMore?n("div",[n("el-button",{staticClass:"blockbtn",attrs:{size:"mini",disabled:!t.hasMore},on:{click:t.loadmoreDemand}},[t._v("\n               Show More\n    ")])],1):t._e()],2)},d=[]},GbS9:function(t,e,n){var a=n("aQUU");"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);var d=n("rjj0").default;d("1ab7a062",a,!0,{})},JAFF:function(t,e,n){"use strict";function a(t){n("GbS9")}var d=n("+lgA"),r=n("wgb7"),i=n("XyMi"),o=a,s=Object(i.a)(d.a,r.a,r.b,!1,o,"data-v-7efafcd7",null);e.a=s.exports},To87:function(t,e,n){e=t.exports=n("FZ+f")(!1),e.push([t.i,".demand-list[data-v-eb82bcd6]{padding:auto}",""])},aQUU:function(t,e,n){e=t.exports=n("FZ+f")(!1),e.push([t.i,".demand-main[data-v-7efafcd7]{padding:10px;background-color:#f8f9fa;border-bottom:2px solid #eee}.demand-main .demand-body[data-v-7efafcd7]{font-size:1.05em}.demand-main .demand-body a[data-v-7efafcd7]{color:#00838f}.demand-main .demand-body a[data-v-7efafcd7]:hover{color:#409eff}.demand-main .demand-bar[data-v-7efafcd7]{font-size:.75em}",""])},o23n:function(t,e,n){"use strict";var a=n("Dd8w"),d=n.n(a),r=n("NYxO"),i=n("JAFF");e.a={name:"demand-list",components:{Demand:i.a},props:{type:String,userid:null,tag:String},computed:d()({},Object(r.b)(["currentDemands","currentD","maxD"]),{hasMore:function(){return this.currentD<this.maxD}}),methods:{initData:function(){var t={type:this.type,userid:this.userid,tag:this.tag};this.$store.dispatch("getDemands",t)},loadmoreDemand:function(){var t={type:this.type,userid:this.userid,tag:this.tag,page:this.currentD};this.$store.dispatch("moreDemands",t)}},created:function(){this.initData()}}},pxgU:function(t,e,n){"use strict";function a(t){n("qgfp")}var d=n("o23n"),r=n("CgPp"),i=n("XyMi"),o=a,s=Object(i.a)(d.a,r.a,r.b,!1,o,"data-v-eb82bcd6",null);e.a=s.exports},qgfp:function(t,e,n){var a=n("To87");"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);var d=n("rjj0").default;d("529fd944",a,!0,{})},tQu9:function(t,e,n){"use strict";function a(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"popular",e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"";return{name:t+"-demand",render:function(n){return n(d.a,{props:{type:t,userid:e}})}}}Object.defineProperty(e,"__esModule",{value:!0}),e.default=a;var d=n("pxgU")},wgb7:function(t,e,n){"use strict";n.d(e,"a",function(){return a}),n.d(e,"b",function(){return d});var a=function(){var t=this,e=t.$createElement,n=t._self._c||e;return t.requestor?n("div",{staticClass:"demand-main"},[n("div",{staticClass:"demand-body"},[n("router-link",{attrs:{to:"/demand/"+t.demand.id}},[n("b",[t._v(t._s(t.demand.body))])])],1),t._v(" "),n("div",{staticClass:"demand-bar"},[t._v("\n    - "),n("router-link",{attrs:{to:"/profile/"+t.requestor.id}},[t._v("\n        "+t._s(t.requestor.name)+"\n      ")]),t._v("\n    | "+t._s(t.vote)+" "),n("el-button",{attrs:{type:"text"},on:{click:t.upDemand}},[t._v("Upvote")]),t._v("\n    | "),n("router-link",{attrs:{to:"/create/"+t.demand.id}},[t._v("\n        "+t._s(t._f("pluralise")(t.answercount,"Answer"))+"  \n      ")]),t._v("\n    | "),n("router-link",{attrs:{to:"/demand/"+t.demand.id}},[t._v("\n        "+t._s(t._f("pluralise")(t.demand.commentcount,"Comment"))+"  \n      ")])],1)]):t._e()},d=[]}});
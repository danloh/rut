webpackJsonp([34],{DQiV:function(t,i,e){var a=e("Nqnw");"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);e("rjj0")("83b8f02e",a,!0,{})},Nqnw:function(t,i,e){i=t.exports=e("FZ+f")(!1),i.push([t.i,".activity-list[data-v-a688b844]{margin-top:5px;padding:10px;border-top:1px solid #eee;background-color:#eceff1}.activity-list .act-time[data-v-a688b844]{font-size:.8em;color:green}",""])},W4mg:function(t,i,e){"use strict";function a(t){e("DQiV")}Object.defineProperty(i,"__esModule",{value:!0});var n=e("uw/v"),c=e("dB0T"),o=e("XyMi"),r=a,s=Object(o.a)(n.a,c.a,c.b,!1,r,"data-v-a688b844",null);i.default=s.exports},dB0T:function(t,i,e){"use strict";e.d(i,"a",function(){return a}),e.d(i,"b",function(){return n});var a=function(){var t=this,i=t.$createElement,e=t._self._c||i;return e("div",[e("b",[t._v("What's Happening")]),t._v(" "),t._l(t.activity,function(i,a){return i.event.type?e("div",{key:a,staticClass:"activity-list"},[e("span",[t._v(t._s(i.action)+" "+t._s(i.event.type))]),t._v(" "),e("router-link",{attrs:{to:"/"+i.event.type+"/"+i.event.id}},[t._v("\n      "+t._s(i.event.content)+"\n    ")]),t._v(" "),e("br"),e("span",{staticClass:"act-time"},[t._v(t._s(t._f("timeAgo")(i.timestamp)))])],1):t._e()}),t._v(" "),0===t.activity.length?e("div",[t._v("Nothing Happened")]):t._e()],2)},n=[]},"uw/v":function(t,i,e){"use strict";var a=e("P9l9");i.a={name:"profile-activity",data:function(){return{activity:[]}},methods:{loadActivity:function(){var t=this,i=this.$route.params.id;Object(a.O)(i).then(function(i){t.activity=i.data})}},watch:{"$route.params.id":"loadActivity"},created:function(){this.loadActivity()}}}});
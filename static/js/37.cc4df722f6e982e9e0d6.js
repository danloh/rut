webpackJsonp([37],{KHto:function(e,t,a){var i=a("b4MM");"string"==typeof i&&(i=[[e.i,i,""]]),i.locals&&(e.exports=i.locals);var l=a("rjj0").default;l("2d90efd3",i,!0,{})},Nmpn:function(e,t,a){"use strict";var i=a("P9l9");t.a={name:"challenge",title:"Readup.Tips - Challenge To Reading Anything",data:function(){return{clipForm:{clip:"",doingItemID:null},rules:{clip:[{min:1,max:500,message:"Required, Max 500 Characters",trigger:"blur"}],doingItemID:[{required:!0,message:"Required",trigger:"change"}]},onRoad:{},items:[],dueDate:"",doingItems:[]}},methods:{submitClip:function(e,t){var a=this;this.$refs[e].validate(function(i){if(!i||!t.clip.trim()||null===t.doingItemID)return a.$message({showClose:!0,message:"Something Wrong, Please Check"}),!1;var l={clip:t.clip.trim(),itemid:t.doingItemID};a.$store.dispatch("postClip",l),a.resetForm(e)})},getOnRoad:function(){var e=this;Object(i.V)().then(function(t){e.onRoad=t.data,e.items=t.data.items.slice(0,10),e.dueDate=t.data.deadline})},markRoadAsDone:function(){var e=this,t=this.onRoad.id;Object(i._20)(t).then(function(t){t.data&&e.getOnRoad()})},getChallengeItems:function(){var e=this;Object(i.D)().then(function(t){e.doingItems=t.data})},resetForm:function(e){this.$refs[e].resetFields()}},mounted:function(){this.getOnRoad(),this.getChallengeItems()}}},Oyxt:function(e,t,a){"use strict";a.d(t,"a",function(){return i}),a.d(t,"b",function(){return l});var i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"challenge-page"},[a("div",{staticClass:"challenge-view"},[a("div",[a("el-form",{ref:"clipForm",attrs:{model:e.clipForm,rules:e.rules}},[a("el-form-item",{staticStyle:{"margin-bottom":"16px"},attrs:{prop:"clip"}},[a("el-input",{attrs:{type:"textarea",autosize:{minRows:2},placeholder:"Excerpt quotes %^&1:First Chapter,Page two:2"},model:{value:e.clipForm.clip,callback:function(t){e.$set(e.clipForm,"clip",t)},expression:"clipForm.clip"}})],1),e._v(" "),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:e.clipForm.clip.trim(),expression:"clipForm.clip.trim()"}],staticStyle:{"margin-bottom":"8px"},attrs:{prop:"doing"}},[a("el-select",{staticClass:"selectItem",attrs:{placeholder:"Pick an item which you are working on"},model:{value:e.clipForm.doingItemID,callback:function(t){e.$set(e.clipForm,"doingItemID",t)},expression:"clipForm.doingItemID"}},e._l(e.doingItems,function(e){return a("el-option",{key:e.id,attrs:{label:e.title,value:e.id}})}))],1),e._v(" "),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:e.clipForm.clip.trim(),expression:"clipForm.clip.trim()"}]},[a("el-button",{attrs:{type:"success",size:"mini",disabled:!e.clipForm.clip.trim()},on:{click:function(t){e.submitClip("clipForm",e.clipForm)}}},[e._v("\n                     Submit\n          ")])],1)],1)],1),e._v(" "),a("div",{staticClass:"submenu"},[a("b",[e._v("Sparks Of Readers  ")]),e._v(" "),a("router-link",{attrs:{to:"/challenge/allclip"}},[e._v("All")]),e._v(" "),a("router-link",{attrs:{to:"/challenge/hotclip"}},[e._v("Popular")]),e._v(" "),a("router-link",{attrs:{to:"/challenge/myclip"}},[e._v("My")])],1),e._v(" "),a("div",{staticClass:"clip-view"},[a("router-view")],1)]),e._v(" "),a("div",{staticClass:"challenge-side"},[a("div",{staticClass:"right-title"},[a("b",[e._v("Working on RoadMap:")]),e._v(" "),a("br"),e._v(" "),a("router-link",{attrs:{to:"/roadmap/"+e.onRoad.id}},[a("b",{staticStyle:{"font-size":"1.1em"}},[e._v(e._s(e.onRoad.title))])]),e._v(" "),a("br"),e._v(" "),a("b",{staticClass:"deadline"},[e._v("Deadline: "+e._s(e._f("toMDY")(e.dueDate,e.rep=!1)))]),e._v(" "),a("el-button",{attrs:{type:"text"},on:{click:e.markRoadAsDone}},[e._v(" ->")]),e._v(" "),a("br"),e._v(" "),a("b",[e._v("Including Items:")])],1),e._v(" "),e._l(e.items,function(t,i){return a("p",{key:i,staticClass:"right-item",attrs:{item:t}},[a("b",[e._v(e._s(t.cate))]),e._v(" "),a("router-link",{attrs:{to:"/item/"+t.id,title:t.title}},[e._v(" "+e._s(t.title.slice(0,42))+"\n                   ...\n      ")])],1)})],2)])},l=[]},b4MM:function(e,t,a){t=e.exports=a("FZ+f")(!1),t.push([e.i,".challenge-page[data-v-d4b1015a]{padding:10px 285px 10px 0;position:relative}.challenge-page .challenge-view[data-v-d4b1015a]{padding:auto}.challenge-page .challenge-view .selectItem[data-v-d4b1015a]{width:100%}.challenge-page .challenge-view .submenu[data-v-d4b1015a]{margin-bottom:5px}.challenge-page .challenge-view .submenu a[data-v-d4b1015a]{color:gray;margin-right:.85em}.challenge-page .challenge-view .submenu a[data-v-d4b1015a]:hover{color:#006400}.challenge-page .challenge-view .submenu a.router-link-active[data-v-d4b1015a]{color:orange;font-weight:800}.challenge-page .challenge-side[data-v-d4b1015a]{position:absolute;top:10px;right:0;width:270px;background-color:#f0f3f0;padding:5px}.challenge-page .challenge-side .right-title[data-v-d4b1015a]{padding:0 5px}.challenge-page .challenge-side .right-title b[data-v-d4b1015a]{font-size:.85em}.challenge-page .challenge-side .right-title .deadline[data-v-d4b1015a]{color:red}.challenge-page .challenge-side .right-item[data-v-d4b1015a]{padding:0 0 0 10px;font-size:.85em;background-color:#f7f8f7}.challenge-page .challenge-side a[data-v-d4b1015a]:hover{color:#f60}",""])},epzP:function(e,t,a){"use strict";function i(e){a("KHto")}Object.defineProperty(t,"__esModule",{value:!0});var l=a("Nmpn"),n=a("Oyxt"),o=a("XyMi"),r=i,s=Object(o.a)(l.a,n.a,n.b,!1,r,"data-v-d4b1015a",null);t.default=s.exports}});
webpackJsonp([37],{I8MS:function(e,t,a){"use strict";var i=a("iF09");t.a={name:"headlines",title:"News For Readers",data:function(){return{canSub:Object(i.a)(),headlineForm:{title:"",url:"",content:""},rules:{title:[{min:1,max:255,message:"Required, Max 255 Characters",trigger:"blur"}]},showForm:!1}},methods:{submitHeadline:function(e,t){var a=this;this.$refs[e].validate(function(n){if(n&&Object(i.a)()){var r=t.url.trim(),o=t.content.trim();if(!r&&!o)return a.$message({showClose:!0,message:"Either of URL and Text Content is requied"}),!1;var l={title:t.title.trim(),url:r,content:o};a.$store.dispatch("postHeadline",l),a.resetForm(e),a.showForm=!1}else Object(i.a)()||(a.$message({showClose:!0,message:"Should Log in to Continue"}),a.$router.push({path:"/login",query:{redirect:a.$route.fullPath}}))})},resetForm:function(e){this.$refs[e].resetFields()}}}},O581:function(e,t,a){t=e.exports=a("FZ+f")(!1),t.push([e.i,".headline-page[data-v-e5c644c2]{padding:10px 200px 10px 0;position:relative}.headline-page .headline-main .submenu[data-v-e5c644c2]{margin-bottom:5px}.headline-page .headline-main .submenu a[data-v-e5c644c2]{color:gray;margin-right:.85em}.headline-page .headline-main .submenu a[data-v-e5c644c2]:hover{color:#006400}.headline-page .headline-main .submenu a.router-link-active[data-v-e5c644c2]{color:orange;font-weight:800}.headline-page .headline-side[data-v-e5c644c2]{position:absolute;top:10px;right:0;width:180px;background-color:#f2f5f2;padding:5px}.headline-page .headline-side .right-title[data-v-e5c644c2]{padding:2px 5px}.headline-page .headline-side .right-item[data-v-e5c644c2]{padding:2px 5px;font-size:.8em}",""])},QKIv:function(e,t,a){"use strict";a.d(t,"a",function(){return i}),a.d(t,"b",function(){return n});var i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"headline-page"},[a("div",{staticClass:"headline-main"},[a("div",{staticClass:"submenu"},[a("b",[e._v("News For Readers  ")]),e._v(" "),a("router-link",{attrs:{to:"/headlines/top"}},[e._v("Top")]),e._v(" "),a("router-link",{attrs:{to:"/headlines/new"}},[e._v("New")]),e._v(" "),e.canSub?a("el-button",{staticStyle:{float:"right"},attrs:{type:"text"},on:{click:function(t){e.showForm=!e.showForm}}},[e._v("\n                 Submit\n      ")]):e._e()],1),e._v(" "),a("div",{directives:[{name:"show",rawName:"v-show",value:e.showForm,expression:"showForm"}]},[a("el-form",{ref:"headlineForm",attrs:{model:e.headlineForm,rules:e.rules}},[a("el-form-item",{staticStyle:{"margin-bottom":"10px"},attrs:{prop:"title"}},[a("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"Title"},model:{value:e.headlineForm.title,callback:function(t){e.$set(e.headlineForm,"title",t)},expression:"headlineForm.title"}})],1),e._v(" "),a("el-form-item",{staticStyle:{"margin-bottom":"8px"},attrs:{prop:"url"}},[a("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"either URL"},model:{value:e.headlineForm.url,callback:function(t){e.$set(e.headlineForm,"url",t)},expression:"headlineForm.url"}})],1),e._v(" "),a("el-form-item",{staticStyle:{"margin-bottom":"5px"},attrs:{prop:"content"}},[a("el-input",{attrs:{type:"textarea",autosize:{minRows:2},placeholder:"or Text Content"},model:{value:e.headlineForm.content,callback:function(t){e.$set(e.headlineForm,"content",t)},expression:"headlineForm.content"}})],1),e._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary",size:"mini",disabled:!e.headlineForm.title.trim()},on:{click:function(t){e.submitHeadline("headlineForm",e.headlineForm)}}},[e._v("\n                     Submit\n          ")])],1)],1)],1),e._v(" "),a("div",{staticClass:"headline-view"},[a("router-view")],1)]),e._v(" "),e._m(0)])},n=[function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"headline-side"},[a("p",{staticClass:"right-item"},[e._v("\n      On-Topic: Anything About Reading/Learning\n    ")])])}]},WOXv:function(e,t,a){var i=a("O581");"string"==typeof i&&(i=[[e.i,i,""]]),i.locals&&(e.exports=i.locals);var n=a("rjj0").default;n("295a5b9c",i,!0,{})},jXjW:function(e,t,a){"use strict";function i(e){a("WOXv")}Object.defineProperty(t,"__esModule",{value:!0});var n=a("I8MS"),r=a("QKIv"),o=a("XyMi"),l=i,s=Object(o.a)(n.a,r.a,r.b,!1,l,"data-v-e5c644c2",null);t.default=s.exports}});
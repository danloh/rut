webpackJsonp([38],{D87z:function(e,o,r){o=e.exports=r("FZ+f")(!1),o.push([e.i,".login-page[data-v-4a2f0158]{padding:10px 250px;position:relative}.login-page .login-form[data-v-4a2f0158]{padding:20px;border:1px dotted #689f38}.login-page .title[data-v-4a2f0158]{text-align:center;margin-bottom:20px}",""])},LoBU:function(e,o,r){"use strict";function t(e){r("nw1E")}Object.defineProperty(o,"__esModule",{value:!0});var n=r("rtbW"),s=r("dsxG"),a=r("XyMi"),i=t,l=Object(a.a)(n.a,s.a,s.b,!1,i,"data-v-4a2f0158",null);o.default=l.exports},dsxG:function(e,o,r){"use strict";r.d(o,"a",function(){return t}),r.d(o,"b",function(){return n});var t=function(){var e=this,o=e.$createElement,r=e._self._c||o;return r("div",{staticClass:"login-page"},[r("h3",{staticClass:"title"},[e._v("Please Log in")]),e._v(" "),r("el-form",{ref:"loginForm",staticClass:"login-form",attrs:{model:e.loginForm,rules:e.rules}},[r("el-form-item",{attrs:{prop:"username"}},[r("el-input",{attrs:{placeholder:"Username"},model:{value:e.loginForm.username,callback:function(o){e.$set(e.loginForm,"username",o)},expression:"loginForm.username"}})],1),e._v(" "),r("el-form-item",{attrs:{prop:"password"}},[r("el-input",{attrs:{type:e.pwdType,placeholder:"Password"},model:{value:e.loginForm.password,callback:function(o){e.$set(e.loginForm,"password",o)},expression:"loginForm.password"}})],1),e._v(" "),r("p",{staticStyle:{"font-size":"0.75em"}},[e._v("\n      Notice: Just Use Cookies Here to keep you logged in for a limited period, \n      Never collect any Private Information. \n      The service may not function properly if disable cookies.\n    ")]),e._v(" "),r("el-form-item",[r("el-button",{staticClass:"blockbtn",attrs:{type:"primary"},on:{click:function(o){e.onLogin("loginForm",e.loginForm)}}},[e._v("\n                 Log in\n      ")])],1),e._v(" "),r("router-link",{attrs:{to:"/register"}},[e._v("No Account? Sign Up")]),e._v("\n              \n    "),r("router-link",{attrs:{to:"/forget"}},[e._v(" Forget Password?")])],1)],1)},n=[]},nw1E:function(e,o,r){var t=r("D87z");"string"==typeof t&&(t=[[e.i,t,""]]),t.locals&&(e.exports=t.locals);r("rjj0")("66119472",t,!0,{})},rtbW:function(e,o,r){"use strict";o.a={name:"login",title:"Log in",data:function(){return{loginForm:{username:"",password:""},rules:{username:[{required:!0,message:"Please enter username",trigger:"blur"}],password:[{required:!0,message:"Please enter password",trigger:"blur"}]},pwdType:"password"}},methods:{onLogin:function(e,o){var r=this;this.$refs[e].validate(function(e){if(!e)return r.$message("error!! Please Check"),!1;r.$axios.defaults.auth={username:o.username,password:o.password},r.$store.dispatch("loginUser").then(function(){var e=r.$route.query.redirect||"/challenge";r.$router.push(e)}).catch(function(){r.$message({showClose:!0,duration:0,message:"oops...Please Check Account or Password",type:"error"})})})}}}}});
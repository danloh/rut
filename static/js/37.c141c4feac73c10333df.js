webpackJsonp([37],{"2K0X":function(e,r,a){r=e.exports=a("FZ+f")(!1),r.push([e.i,".sign-page[data-v-c4c896a8]{padding:10px 250px;position:relative}.sign-page .sign-form[data-v-c4c896a8]{padding:20px;border:1px dotted #689f38}.sign-page .title[data-v-c4c896a8]{text-align:center;margin-bottom:20px}",""])},EOTA:function(e,r,a){"use strict";var t=a("P9l9");r.a={name:"register",title:"Register",data:function(){var e=this;return{regForm:{username:"",email:"",password:"",repassword:""},rules:{username:[{required:!0,validator:function(r,a,t){""!==a.trim()?e.validName().then(function(e){e.data?t():t(new Error("Please Try again, The username has been used"))}):t(new Error("Please Input Username"))},trigger:"blur"}],email:[{required:!0,validator:function(r,a,t){/^[a-zA-Z0-9_-]+([-_.][A-Za-z0-9]+)*@[a-zA-Z0-9_-]+(\.[a-zA-Z]+)+$/.test(a.trim())?e.validEmail().then(function(e){e.data?t():t(new Error("The Email has been registered, Please log in directly"))}):t(new Error("Please Input Email"))},trigger:"blur"}],password:[{required:!0,validator:function(r,a,t){""===a.trim()?t(new Error("Please input the password")):(""!==e.regForm.repassword&&e.$refs.regForm.validateField("repassword"),t())},trigger:"blur"},{min:6,message:"At Least 6 characters",trigger:"blur"}],repassword:[{required:!0,validator:function(r,a,t){""===a.trim()?t(new Error("Please input the password again")):a!==e.regForm.password?t(new Error("Two inputs do not match!")):t()},trigger:"blur"},{min:6,message:"At Least 6 characters",trigger:"blur"}]},pwdType:"password"}},methods:{onReg:function(e,r){var a=this;this.$refs[e].validate(function(e){if(!e)return a.$message({showClose:!0,message:"error!! Please Check"}),!1;var t=a.$route.query.refcode,s={username:r.username,email:r.email.trim(),password:r.password,incode:t||""};a.$store.dispatch("registerUser",s).then(function(){a.$router.push("/challenge"),a.$message({showClose:!0,message:"Welcome! A confirmation email has been sent to you by email."})})})},validName:function(){var e=this.regForm.username;return Object(t.i)(e)},validEmail:function(){var e=this.regForm.email;return Object(t.c)(e)}}}},HXce:function(e,r,a){var t=a("2K0X");"string"==typeof t&&(t=[[e.i,t,""]]),t.locals&&(e.exports=t.locals);a("rjj0")("112fd9de",t,!0,{})},jPWb:function(e,r,a){"use strict";a.d(r,"a",function(){return t}),a.d(r,"b",function(){return s});var t=function(){var e=this,r=e.$createElement,a=e._self._c||r;return a("div",{staticClass:"sign-page"},[a("h3",{staticClass:"title"},[e._v("Welcome to Join")]),e._v(" "),a("el-form",{ref:"regForm",staticClass:"sign-form",attrs:{model:e.regForm,rules:e.rules}},[a("el-form-item",{attrs:{prop:"username"}},[a("el-input",{attrs:{placeholder:"Username"},model:{value:e.regForm.username,callback:function(r){e.$set(e.regForm,"username",r)},expression:"regForm.username"}})],1),e._v(" "),a("el-form-item",{attrs:{prop:"email"}},[a("el-input",{attrs:{placeholder:"Email"},model:{value:e.regForm.email,callback:function(r){e.$set(e.regForm,"email",r)},expression:"regForm.email"}})],1),e._v(" "),a("el-form-item",{attrs:{prop:"password"}},[a("el-input",{attrs:{type:e.pwdType,placeholder:"Password, at least 6 characters"},model:{value:e.regForm.password,callback:function(r){e.$set(e.regForm,"password",r)},expression:"regForm.password"}})],1),e._v(" "),a("el-form-item",{attrs:{prop:"repassword"}},[a("el-input",{attrs:{type:e.pwdType,placeholder:"Confirm Password"},model:{value:e.regForm.repassword,callback:function(r){e.$set(e.regForm,"repassword",r)},expression:"regForm.repassword"}})],1),e._v(" "),a("p",{staticStyle:{"font-size":"0.75em"}},[e._v("\n      Notice: Will Use Cookies to keep you logged in for a limited period, \n      Never collect any Private Information. \n      The service may not function properly if disable cookies.\n    ")]),e._v(" "),a("el-form-item",[a("el-button",{staticClass:"blockbtn",attrs:{type:"primary"},on:{click:function(r){e.onReg("regForm",e.regForm)}}},[e._v("\n                 Sign Up\n      ")])],1),e._v(" "),a("router-link",{attrs:{to:"/login"}},[e._v("Have an Account?  Login")])],1)],1)},s=[]},kTq1:function(e,r,a){"use strict";function t(e){a("HXce")}Object.defineProperty(r,"__esModule",{value:!0});var s=a("EOTA"),o=a("jPWb"),i=a("XyMi"),n=t,l=Object(i.a)(s.a,o.a,o.b,!1,n,"data-v-c4c896a8",null);r.default=l.exports}});
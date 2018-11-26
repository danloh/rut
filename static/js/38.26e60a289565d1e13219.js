webpackJsonp([38],{"1mIR":function(t,e,a){"use strict";a.d(e,"a",function(){return i}),a.d(e,"b",function(){return r});var i=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"edit-page"},[a("h3",{staticClass:"title"},[t._v(" Edit My Profile")]),t._v(" "),a("b",{staticStyle:{color:"green","font-size":"0.8em"}},[t._v("\n    Please Note: The Profile Information will be displayed publicly\n  ")]),t._v(" "),a("el-form",{ref:"settingForm",staticClass:"edit-form",attrs:{size:"mini",model:t.settingForm,rules:t.rules,"label-width":"90px"}},[a("el-form-item",{attrs:{label:"Nickname",prop:"nickname"}},[a("el-input",{attrs:{placeholder:"a-zA-Z_0-9{2,20}"},model:{value:t.settingForm.nickname,callback:function(e){t.$set(t.settingForm,"nickname",e)},expression:"settingForm.nickname"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"Location",prop:"location"}},[a("el-input",{model:{value:t.settingForm.location,callback:function(e){t.$set(t.settingForm,"location",e)},expression:"settingForm.location"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"Avatar URL",prop:"avatarurl"}},[a("el-input",{attrs:{type:"textarea",autosize:""},model:{value:t.settingForm.avatarUrl,callback:function(e){t.$set(t.settingForm,"avatarUrl",e)},expression:"settingForm.avatarUrl"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"About Me",prop:"about"}},[a("el-input",{attrs:{type:"textarea",autosize:{minRows:3}},model:{value:t.settingForm.about,callback:function(e){t.$set(t.settingForm,"about",e)},expression:"settingForm.about"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"Website",prop:"url"}},[a("el-input",{attrs:{type:"textarea",autosize:"",placeholder:"Personal Page or Website Url"},model:{value:t.settingForm.url,callback:function(e){t.$set(t.settingForm,"url",e)},expression:"settingForm.url"}})],1),t._v(" "),a("el-form-item",[a("el-button",{staticClass:"blockbtn",attrs:{type:"success",size:"mini",disabled:!t.canSetting},on:{click:function(e){t.onSetting("settingForm",t.settingForm)}}},[t._v("\n                 Update My Profile\n      ")])],1)],1)],1)},r=[]},"6j0K":function(t,e,a){"use strict";function i(t){a("BrIy")}Object.defineProperty(e,"__esModule",{value:!0});var r=a("O7dQ"),n=a("1mIR"),o=a("XyMi"),s=i,l=Object(o.a)(r.a,n.a,n.b,!1,s,"data-v-7b2d1c96",null);e.default=l.exports},BrIy:function(t,e,a){var i=a("ygfG");"string"==typeof i&&(i=[[t.i,i,""]]),i.locals&&(t.exports=i.locals);var r=a("rjj0").default;r("644fae66",i,!0,{})},HJfm:function(t,e,a){"use strict";a.d(e,"d",function(){return i}),a.d(e,"a",function(){return r}),a.d(e,"b",function(){return n}),a.d(e,"c",function(){return o}),a.d(e,"e",function(){return s});var i=/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[#@!~%^$&*-])[a-zA-Z\d#@!~%^$&*-]{6,18}$/,r=/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/,n=/^[a-z][0-9a-z_]{2,19}$/,o=/^[\w ]{2,20}$/,s=/[\n|\r|\s]#(\w+)/g},O7dQ:function(t,e,a){"use strict";var i=a("P9l9"),r=a("iF09"),n=a("HJfm");e.a={name:"edit-profile",title:"Edit My Profile",data:function(){return{settingForm:{nickname:"",location:"",avatarUrl:"",about:"",url:""},rules:{location:[{max:64,message:"Max Length should be 64",trigger:"change"}],avatarUrl:[{max:500,message:"Max Length should be 500",trigger:"change"}],url:[{max:120,message:"Max Length should be 120",trigger:"change"}]},userid:null,canSetting:!1}},methods:{onSetting:function(t,e){var a=this;this.$refs[t].validate(function(t){var o=e.nickname.trim();if(!(t&&Object(r.a)()&&a.canSetting))return a.$message({showClose:!0,message:"Something Wrong, Please Check"}),!1;var s={nickname:n.c.test(o)?o:"",location:e.location.trim(),avatarUrl:e.avatarUrl.trim(),about:e.about.trim(),url:e.url.trim()};Object(i.v)(s).then(function(t){a.$router.push("/profile/"+a.userid),a.$message({showClose:!0,message:t.data})})})},setFormData:function(t){this.settingForm.nickname=t.nickname,this.settingForm.location=t.location,this.settingForm.avatarUrl=t.avatar,this.settingForm.about=t.about,this.settingForm.url=t.exlink,this.canSetting=!0}},created:function(){var t=this.$store.getters.currentUser;this.userid=t.id,this.setFormData(t)}}},ygfG:function(t,e,a){e=t.exports=a("FZ+f")(!1),e.push([t.i,".edit-page[data-v-7b2d1c96]{padding:10px 40px;position:relative}.edit-page .edit-form[data-v-7b2d1c96]{padding:20px;border:1px dotted #689f38}.edit-page .title[data-v-7b2d1c96]{text-align:center;margin-bottom:20px}",""])}});
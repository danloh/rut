webpackJsonp([43],{"0Stc":function(t,n){},"1yPN":function(t,n,e){"use strict";e.d(n,"a",function(){return r}),e.d(n,"b",function(){return u});var r=function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("div",{attrs:{id:"app"}},[e("header",{staticClass:"header"},[e("nav",{staticClass:"nav-menu"},[e("router-link",{attrs:{to:"/"}},[e("b",{staticStyle:{color:"darkorange","font-size":"1.2em","letter-spacing":"0.0005em"}},[t._v("\n            Readup.Tips"),e("sup",{staticStyle:{"font-size":"0.5em",color:"grey"}},[t._v(" alpha")])])]),t._v(" "),t.authed?e("router-link",{attrs:{to:"/feeds"}},[e("b",[t._v("Feed")])]):t._e(),t._v(" "),e("router-link",{attrs:{to:"/challenge"}},[e("b",[t._v("Challenge")])]),t._v(" "),e("router-link",{attrs:{to:"/demands"}},[e("b",[t._v("Request")])]),t._v(" "),e("router-link",{attrs:{to:"/headlines"}},[e("b",[t._v("Headline")])]),t._v(" "),e("router-link",{attrs:{to:"/create"}},[e("b",[t._v("Create Now")])]),t._v(" "),e("div",{staticClass:"right-menu"},[t.authed?e("el-dropdown",[e("el-button",{attrs:{type:"success",size:"small"}},[e("i",{staticClass:"el-icon-menu"}),t._v(" "),e("i",{staticClass:"el-icon-arrow-down el-icon--right"})]),t._v(" "),e("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[e("el-dropdown-item",[e("router-link",{attrs:{to:"/profile/"+t.currentUserID}},[t._v("Profile")])],1),t._v(" "),e("el-dropdown-item",{attrs:{divided:""}},[e("el-button",{attrs:{type:"text",size:"mini"},on:{click:t.onLogout}},[t._v("Log out")])],1)],1)],1):e("div",[e("el-button",{attrs:{type:"text"},on:{click:function(n){t.toLogin=!0}}},[e("b",{staticClass:"login"},[t._v("Log in")])])],1),t._v(" "),e("el-dialog",{staticClass:"loginDialog",attrs:{visible:t.toLogin,width:"40%"},on:{"update:visible":function(n){t.toLogin=n}}},[e("login-form",{attrs:{next:"current"},on:{close:function(n){t.toLogin=!1}}})],1)],1)],1)]),t._v(" "),e("div",{staticClass:"view"},[e("router-view")],1),t._v(" "),e("footer",{staticClass:"footer"},[e("div",{staticClass:"bottom"},[t._v("\n      ©Readup.Tips - since 2018\n      | "),e("router-link",{attrs:{to:"/newitem"}},[t._v("submit")]),t._v("\n      | "),e("router-link",{attrs:{to:"/"}},[t._v("About")]),t._v("\n      | "),e("router-link",{attrs:{to:"/"}},[t._v("Terms")]),t._v("\n      | "),e("a",{attrs:{href:"mailto:readup.tips@gmail.com?subject=Feedback..."}},[t._v("Contact")]),t._v(" "),t._v("\n              \n      "),e("el-input",{staticStyle:{width:"16em"},attrs:{size:"mini",placeholder:"Search Readup.Tips"},nativeOn:{keyup:function(n){if(!("button"in n)&&t._k(n.keyCode,"enter",13,n.key))return null;t.siteSearch(n)}},model:{value:t.searchWord,callback:function(n){t.searchWord=n},expression:"searchWord"}},[e("i",{staticClass:"el-input__icon el-icon-search",attrs:{slot:"prefix"},slot:"prefix"})])],1)])])},u=[]},"3gVa":function(t,n){},"62IG":function(t,n,e){"use strict";function r(t){e("abK8")}var u=e("QsGi"),i=e("bDIs"),o=e("XyMi"),a=r,c=Object(o.a)(u.a,i.a,i.b,!1,a,"data-v-49b86df0",null);n.a=c.exports},"6aq2":function(t,n,e){"use strict";function r(t,n){return 1===t?t+n+" ago":t+n+"s ago"}function u(t){var n=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],e=n?t.replace(/\s+/g,"T").concat("Z"):t,u=new Date(e),i=u.getTime(),o=Number(Date.now())/1e3+0-Number(i)/1e3;return o<3600?l()(~~(o/60),0)?"just now":r(~~(o/60)," minute"):o<86400?r(~~(o/3600)," hour"):r(~~(o/86400)," day")}function i(t){var n=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],e=n?t.replace(/\s+/g,"T").concat("Z"):t;return t?new Date(e).toLocaleString():t}function o(t){var n=!(arguments.length>1&&void 0!==arguments[1])||arguments[1];if(!t)return t;var e=n?t.replace(/\s+/g,"T").concat("Z"):t;return t=new Date(e),p[t.getMonth()+1]+" "+t.getDate()+","+t.getFullYear()}function a(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:155,e=!(arguments.length>2&&void 0!==arguments[2])||arguments[2];if(!t)return"";if(t.length>n&&e){var r=t.substring(0,n),u=r.lastIndexOf("<a"),i=r.lastIndexOf("</a>"),o=u>i?u:n;return r=r.substring(0,o)+" ..."}return t}function c(t,n){return t+" "+n+(t<=1?"":"s")}function s(t,n,e){""===n.trim()?e(new Error("Blank Value")):e()}function f(t){var n=t.replace(/^https?:\/\//,"").replace(/\/.*$/,""),e=n.split(".").slice(-3);return"www"===e[0]&&e.shift(),e.join(".")}Object.defineProperty(n,"__esModule",{value:!0}),n.timeAgo=u,n.toLocal=i,n.toMDY=o,n.showLess=a,n.pluralise=c,n.trimValid=s,n.host=f;var d=e("g4PW"),l=e.n(d),p={1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}},"6rOw":function(t,n,e){"use strict";e.d(n,"a",function(){return r}),e.d(n,"b",function(){return u});var r=function(){var t=this,n=t.$createElement,e=t._self._c||n;return e("div",[e("h3",{staticClass:"title"},[t._v("Please Log in")]),t._v(" "),e("el-form",{ref:"loginForm",staticClass:"login-form",attrs:{model:t.loginForm,rules:t.rules}},[e("el-form-item",{attrs:{prop:"username"}},[e("el-input",{attrs:{placeholder:"Username"},model:{value:t.loginForm.username,callback:function(n){t.$set(t.loginForm,"username",n)},expression:"loginForm.username"}})],1),t._v(" "),e("el-form-item",{attrs:{prop:"password"}},[e("el-input",{attrs:{type:t.pwdType,placeholder:"Password"},model:{value:t.loginForm.password,callback:function(n){t.$set(t.loginForm,"password",n)},expression:"loginForm.password"}})],1),t._v(" "),e("p",{staticStyle:{"font-size":"0.75em"}},[t._v("\n      Notice: Just Use Cookies Here to keep you logged in for a limited period, \n      Never collect any Private Information. \n      The service may not function properly if disable cookies.\n    ")]),t._v(" "),e("el-form-item",[e("el-button",{staticClass:"blockbtn",attrs:{type:"primary"},on:{click:function(n){t.onLogin("loginForm",t.loginForm)}}},[t._v("\n                  Log in\n      ")])],1),t._v(" "),e("el-button",{attrs:{type:"text"},on:{click:function(n){t.toNext("/register")}}},[t._v("\n      No Account? Sign Up\n    ")]),t._v("\n              \n    "),e("el-button",{attrs:{type:"text"},on:{click:function(n){t.toNext("/forget")}}},[t._v("\n       Forget Password?\n    ")])],1)],1)},u=[]},EnNo:function(t,n,e){"use strict";var r=e("Gu7T"),u=e.n(r),i=e("//Fk"),o=e.n(i),a=e("P9l9"),c={totalDemands:0,currentD:0,maxD:0,currentDemands:[],demandDetail:{}},s={getDemands:function(t,n){var e=t.commit;Object(a.E)(n).then(function(t){e("SET_DEMANDS",t.data)})},getDemand:function(t,n){var e=t.commit;return new o.a(function(t,r){Object(a.B)(n).then(function(n){e("SET_DEMAND",n.data),t(n)}).catch(function(t){r(t)})})},postDemand:function(t,n){var e=t.commit;Object(a._14)(n).then(function(t){e("ADD_DEMAND",t.data)})},moreDemands:function(t,n){var e=t.commit;Object(a.E)(n).then(function(t){e("MORE_DEMANDS",t.data.demands)})}},f={SET_DEMANDS:function(t,n){t.totalDemands=n.total,t.currentD=1,t.maxD=Math.ceil(n.total/20),t.currentDemands=n.demands},MORE_DEMANDS:function(t,n){var e;t.currentD+=1,(e=t.currentDemands).push.apply(e,u()(n))},ADD_DEMAND:function(t,n){t.currentDemands.unshift(n)},SET_DEMAND:function(t,n){t.demandDetail=n}};n.a={state:c,actions:s,mutations:f}},IcnI:function(t,n,e){"use strict";var r=e("//Fk"),u=e.n(r),i=e("7+uW"),o=e("NYxO"),a=e("iF09"),c=e("UjVw"),s=e("XMX0"),f=e("hTt+"),d=e("SPCp"),l=e("EnNo"),p=e("yYt1"),m=e("P9l9");i.default.use(o.a);var h={currentUserID:Number(Object(a.b)()),authed:Boolean(Object(a.b)())&&Boolean(Object(a.c)()),token:Object(a.c)(),currentUser:{},whoEdit:{}},v={SET_USER:function(t,n){var e=n.userid;t.currentUserID=e,t.authed=Boolean(e),Object(a.f)(e,n.exp)},SET_TOKEN:function(t,n){var e=n.token;t.token=e,Object(a.g)(e,n.exp)},SET_INFO:function(t,n){t.currentUser=n},DEL_TOKEN:function(t){t.token="",t.currentUserID="",t.currentUser={},t.authed=!1,Object(a.e)(),Object(a.d)()},SET_WHOEDIT:function(t,n){t.whoEdit=n}},g={getCurrentUser:function(t){var n=t.commit;return new u.a(function(t,e){Object(m.A)().then(function(e){n("SET_INFO",e.data),t(e)}).catch(function(t){e(t)})})},registerUser:function(t,n){var e=t.commit;return new u.a(function(t,r){Object(m._21)(n).then(function(n){var r=n.data;e("SET_TOKEN",r),e("SET_USER",r),t(n)}).catch(function(t){r(t)})})},loginUser:function(t,n){var e=t.commit;return new u.a(function(t,r){Object(m._11)(n).then(function(n){var r=n.data;e("SET_TOKEN",r),e("SET_USER",r),t(n)}).catch(function(t){r(t)})})}},b=new o.a.Store({state:h,actions:g,mutations:v,getters:c.a,modules:{rut:s.a,item:f.a,clip:d.a,demand:l.a,headline:p.a}});n.a=b},IoXI:function(t,n,e){"use strict";function r(t){var n=t.$options.title;if(n)return"function"==typeof n?n.call(t):n}function u(t){var n=r(t);n&&(document.title=n+" @Readup.Tips")}var i={beforeUpdate:function(){u(this)},mounted:function(){u(this)}};n.a=i},M93x:function(t,n,e){"use strict";function r(t){e("3gVa")}var u=e("xJD8"),i=e("1yPN"),o=e("XyMi"),a=r,c=Object(o.a)(u.a,i.a,i.b,!1,a,null,null);n.a=c.exports},NHnr:function(t,n,e){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var r=e("//Fk"),u=e.n(r),i=e("fZjL"),o=e.n(i),a=e("MU8w"),c=(e.n(a),e("7+uW")),s=e("mtWM"),f=e.n(s),d=e("tvR6"),l=(e.n(d),e("wUZ8")),p=e.n(l),m=e("urW8"),h=e.n(m),v=e("62IG"),g=e("IoXI"),b=e("6aq2"),_=e("iF09"),w=e("M93x"),E=e("YaEn"),D=e("IcnI"),I=e("9JMe"),k=(e.n(I),e("zL8q"));e.n(k);Object(I.sync)(D.a,E.a),c.default.config.productionTip=!1,h.a.use(p.a),c.default.use(k.Dialog),c.default.use(k.Dropdown),c.default.use(k.DropdownMenu),c.default.use(k.DropdownItem),c.default.use(k.Input),c.default.use(k.Radio),c.default.use(k.RadioGroup),c.default.use(k.RadioButton),c.default.use(k.Select),c.default.use(k.Option),c.default.use(k.OptionGroup),c.default.use(k.Button),c.default.use(k.ButtonGroup),c.default.use(k.DatePicker),c.default.use(k.Form),c.default.use(k.FormItem),c.default.use(k.Icon),c.default.prototype.$message=k.Message;var T=c.default.prototype.$bar=new c.default(v.a).$mount();document.body.appendChild(T.$el),c.default.mixin(g.a),o()(b).forEach(function(t){c.default.filter(t,b[t])}),f.a.interceptors.response.use(function(t){return t},function(t){if(t.response)switch(t.response.status){case 401:D.a.commit("DEL_TOKEN"),"/login"!==E.a.currentRoute.path&&(E.a.push({path:"/login",query:{redirect:E.a.currentRoute.fullPath}}),(new c.default).$message("Oops...Access Denied, Need To Log in"));break;case 403:(new c.default).$message("Oops...Forbidden");break;case 404:(new c.default).$message("The Resource Was Not Found"),E.a.replace({path:"/404"});break;case 418:(new c.default).$message("Eureka! 42");break;case 500:(new c.default).$message("Oops...Error"),E.a.replace({path:"/"});break;default:(new c.default).$message("Oops...Something Failed: "+t.response.statusText)}return u.a.reject(t)}),E.a.beforeEach(function(t,n,e){if(T.start(),t.meta.auth){var r=Object(_.c)();f.a.defaults.auth={username:r,password:r},r?e():e({path:"/login",query:{redirect:t.fullPath}})}else e()}),E.a.afterEach(function(){T.finish()}),c.default.prototype.$axios=f.a,n.default=f.a,new c.default({router:E.a,store:D.a,render:function(t){return t(w.a)}}).$mount("#app")},P9l9:function(t,n,e){"use strict";e.d(n,"_28",function(){return Wt}),e.d(n,"_21",function(){return s}),e.d(n,"i",function(){return f}),e.d(n,"c",function(){return d}),e.d(n,"m",function(){return l}),e.d(n,"a",function(){return m}),e.d(n,"_22",function(){return h}),e.d(n,"_23",function(){return v}),e.d(n,"d",function(){return g}),e.d(n,"_11",function(){return b}),e.d(n,"_20",function(){return p}),e.d(n,"A",function(){return _}),e.d(n,"_4",function(){return w}),e.d(n,"H",function(){return E}),e.d(n,"O",function(){return D}),e.d(n,"G",function(){return I}),e.d(n,"p",function(){return k}),e.d(n,"g",function(){return T}),e.d(n,"_6",function(){return y}),e.d(n,"_18",function(){return S}),e.d(n,"L",function(){return O}),e.d(n,"y",function(){return C}),e.d(n,"x",function(){return x}),e.d(n,"_27",function(){return R}),e.d(n,"T",function(){return P}),e.d(n,"W",function(){return M}),e.d(n,"_1",function(){return N}),e.d(n,"_0",function(){return H}),e.d(n,"Z",function(){return Ht}),e.d(n,"Y",function(){return jt}),e.d(n,"X",function(){return j}),e.d(n,"k",function(){return L}),e.d(n,"_25",function(){return A}),e.d(n,"j",function(){return F}),e.d(n,"b",function(){return U}),e.d(n,"_9",function(){return $}),e.d(n,"_30",function(){return W}),e.d(n,"r",function(){return K}),e.d(n,"s",function(){return q}),e.d(n,"u",function(){return G}),e.d(n,"_7",function(){return z}),e.d(n,"v",function(){return V}),e.d(n,"n",function(){return X}),e.d(n,"F",function(){return Y}),e.d(n,"_2",function(){return B}),e.d(n,"_3",function(){return J}),e.d(n,"_10",function(){return Z}),e.d(n,"_31",function(){return Q}),e.d(n,"l",function(){return tt}),e.d(n,"t",function(){return nt}),e.d(n,"e",function(){return et}),e.d(n,"w",function(){return rt}),e.d(n,"M",function(){return ut}),e.d(n,"N",function(){return it}),e.d(n,"K",function(){return ot}),e.d(n,"f",function(){return mt}),e.d(n,"_5",function(){return ht}),e.d(n,"_26",function(){return at}),e.d(n,"_8",function(){return ct}),e.d(n,"_29",function(){return st}),e.d(n,"h",function(){return ft}),e.d(n,"_16",function(){return dt}),e.d(n,"o",function(){return lt}),e.d(n,"R",function(){return pt}),e.d(n,"z",function(){return vt}),e.d(n,"_17",function(){return _t}),e.d(n,"U",function(){return wt}),e.d(n,"V",function(){return Et}),e.d(n,"q",function(){return Dt}),e.d(n,"_35",function(){return It}),e.d(n,"S",function(){return kt}),e.d(n,"Q",function(){return Tt}),e.d(n,"E",function(){return yt}),e.d(n,"P",function(){return St}),e.d(n,"B",function(){return Ot}),e.d(n,"D",function(){return Ct}),e.d(n,"C",function(){return xt}),e.d(n,"_12",function(){return gt}),e.d(n,"_32",function(){return bt}),e.d(n,"_14",function(){return Rt}),e.d(n,"_33",function(){return Pt}),e.d(n,"_24",function(){return Mt}),e.d(n,"_13",function(){return Nt}),e.d(n,"_19",function(){return Lt}),e.d(n,"I",function(){return At}),e.d(n,"J",function(){return Ft}),e.d(n,"_15",function(){return Ut}),e.d(n,"_34",function(){return $t});var r=e("bOdI"),u=e.n(r),i=e("woOf"),o=e.n(i),a=e("NHnr"),c=function(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},e=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"get",r=~["delete","get","head"].indexOf(e)?"params":"data";return Object(a.default)(o()({url:t,method:e},u()({},r,n))).then(function(t){return t})},s=function(t){return c("/api/register",t,"post")},f=function(t){return c("/api/checkname/"+t)},d=function(t){return c("/api/checkemail/"+t)},l=function(t){return c("/api/confirm/"+t)},p=function(){return c("/api/confirm")},m=function(t){return c("/api/changepassword",t,"post")},h=function(t){return c("/api/reset",t,"post")},v=function(t,n){return c("/api/reset/"+t,n,"post")},g=function(t,n){return c("/api/checkifexpired/"+t,n)},b=function(t){return c("/api/login",t)},_=function(t){return c("/api/currentuser",t)},w=function(t,n){return c("/api/user/"+t,n)},E=function(t,n,e){return c("/api/user/"+t+"/"+n,e)},D=function(t,n){return c("/api/"+t+"/myactivity",n)},I=function(t){return c("/api/feeds",t)},k=function(t){return c("/api/editprofile",t,"post")},T=function(t,n){return c("/api/checkfollow/"+t,n)},y=function(t,n,e){return c("/api/"+t+"/user/"+n,e)},S=function(t,n){return c("/api/create/"+n,t,"post")},O=function(t){return c("/api/index/ruts",t)},C=function(t){return c("/api/challengerut",t)},x=function(t){return c("/api/challengeitems",t)},R=function(t){return c("/api/setdeadline",t)},P=function(t,n,e){return c("/api/"+n+"/"+t+"/ruts",e)},M=function(t,n){return c("/api/rut/"+t,n)},N=function(t,n){return c("/api/rut/"+t+"/tips",n)},H=function(t,n){return c("/api/rut/"+t+"/demands",n)},j=function(t,n){return c("/api/rut/"+t+"/challengers",n)},L=function(t,n,e){return c("/api/check"+n+"/rut/"+t,e)},A=function(t,n,e){return c("/api/"+t+"/rut/"+n,e)},F=function(t,n,e){return c("/api/checkifrut/"+n+"/lockedto/"+t,e)},U=function(t,n,e){return c("/api/checkif/"+t+"/caneditrut/"+n,e)},$=function(t,n){return c("/api/lockrut/"+t,n)},W=function(t,n){return c("/api/unlockrut/"+t,n)},K=function(t,n){return c("/api/editrut/"+t,n,"post")},q=function(t,n){return c("/api/editrutce/"+t,n,"post")},G=function(t,n){return c("/api/edittags/"+t,n,"post")},z=function(t,n,e){return c("/api/item/"+t+"/torut/"+n,e,"post")},V=function(t,n){return c("/api/edittips/"+t,n,"post")},X=function(t,n){return c("/api/del/tips/"+t,n)},Y=function(t,n){return c("/api/"+t+"/fav/tags",n)},B=function(t,n){return c("/api/tag/"+t,n)},J=function(t,n){return c("/api/tag/"+t+"/ruts",n)},Z=function(t,n){return c("/api/locktag/"+t,n)},Q=function(t,n){return c("/api/unlocktag/"+t,n)},tt=function(t,n,e){return c("/api/checkiftag/"+n+"/lockedto/"+t,e)},nt=function(t,n){return c("/api/edittag/"+t,n,"post")},et=function(t,n){return c("/api/checkfavtag/"+t,n)},rt=function(t,n,e){return c("/api/"+t+"/tag/"+n,e)},ut=function(t,n){return c("/api/item/"+t,n)},it=function(t,n){return c("/api/item/"+t+"/reviews",n)},ot=function(t,n){return c("/api/item/"+t+"/inruts",n)},at=function(t,n){return c("/api/search/"+t+"/items",n)},ct=function(t,n){return c("/api/lockitem/"+t,n)},st=function(t,n){return c("/api/unlockitem/"+t,n)},ft=function(t,n,e){return c("/api/checkifitem/"+n+"/lockedto/"+t,e)},dt=function(t){return c("/api/newitem",t,"post")},lt=function(t,n){return c("/api/edititem/"+t,n,"post")},pt=function(t,n,e){return c("/api/"+n+"/"+t+"/items",e)},mt=function(t,n){return c("/api/checkflag/item/"+t,n)},ht=function(t,n,e){return c("/api/flag"+t+"/item/"+n,e)},vt=function(t){return c("/api/clips",t)},gt=function(t){return c("/api/newclip",t,"post")},bt=function(t,n){return c("/api/upvoteclip/"+t,n)},_t=function(t,n){return c("/api/newreview/"+t,n,"post")},wt=function(t,n){return c("/api/review/"+t,n)},Et=function(t,n){return c("/api/review/"+t+"/comments",n)},Dt=function(t,n){return c("/api/editreview/"+t,n,"post")},It=function(t,n){return c("/api/upvotereview/"+t,n)},kt=function(t,n){return c("/api/user/"+t+"/reviews",n)},Tt=function(t,n){return c("/api/user/"+t+"/demands",n)},yt=function(t){return c("/api/demands",t)},St=function(t,n){return c("/api/onlydemand/"+t,n)},Ot=function(t,n){return c("/api/demand/"+t,n)},Ct=function(t,n){return c("/api/demand/"+t+"/comments",n)},xt=function(t,n){return c("/api/demand/"+t+"/answers",n)},Rt=function(t){return c("/api/newdemand",t,"post")},Pt=function(t,n){return c("/api/upvotedemand/"+t,n)},Mt=function(t,n,e){return c("/api/rut/"+t+"/answerdemand/"+n,e)},Nt=function(t,n,e){return c("/api/comment/"+t+"/"+n,e,"post")},Ht=function(t,n){return c("/api/commentsonrut/"+t,n)},jt=function(t,n){return c("/api/rut/"+t+"/circles",n)},Lt=function(t,n){return c("/api/newcircle/rut/"+t,n,"post")},At=function(t){return c("/api/headlines",t)},Ft=function(t,n){return c("/api/headline/"+t+"/comments",n)},Ut=function(t){return c("/api/newheadline",t,"post")},$t=function(t,n){return c("/api/upvoteheadline/"+t,n)},Wt=function(t){return c("/api/testerror",t)}},QsGi:function(t,n,e){"use strict";n.a={data:function(){return{percent:0,show:!1,canSuccess:!0,duration:3e3,height:"3px",color:"#ffca2b",failedColor:"#ff0000"}},methods:{start:function(){var t=this;return this.show=!0,this.canSuccess=!0,this._timer&&(clearInterval(this._timer),this.percent=0),this._cut=1e4/Math.floor(this.duration),this._timer=setInterval(function(){t.increase(t._cut*Math.random()),t.percent>95&&t.finish()},100),this},set:function(t){return this.show=!0,this.canSuccess=!0,this.percent=Math.floor(t),this},get:function(){return Math.floor(this.percent)},increase:function(t){return this.percent=this.percent+Math.floor(t),this},decrease:function(t){return this.percent=this.percent-Math.floor(t),this},finish:function(){return this.percent=100,this.hide(),this},pause:function(){return clearInterval(this._timer),this},hide:function(){var t=this;return clearInterval(this._timer),this._timer=null,setTimeout(function(){t.show=!1,t.$nextTick(function(){setTimeout(function(){t.percent=0},200)})},500),this},fail:function(){return this.canSuccess=!1,this}}}},SPCp:function(t,n,e){"use strict";var r=e("Gu7T"),u=e.n(r),i=e("P9l9"),o={totalClips:0,currentClips:[],currentP:0,maxP:0},a={getClips:function(t,n){var e=t.commit;Object(i.z)(n).then(function(t){e("SET_CLIPS",t.data)})},postClip:function(t,n){var e=t.commit;Object(i._12)(n).then(function(t){e("ADD_CLIP",t.data)})},moreClips:function(t,n){var e=t.commit;Object(i.z)(n).then(function(t){e("MORE_CLIPS",t.data.clips)})}},c={SET_CLIPS:function(t,n){t.totalClips=n.total,t.currentP=1,t.maxP=Math.ceil(n.total/20),t.currentClips=n.clips},MORE_CLIPS:function(t,n){var e;t.currentP+=1,(e=t.currentClips).push.apply(e,u()(n))},ADD_CLIP:function(t,n){t.currentClips.unshift(n)}};n.a={state:o,actions:a,mutations:c}},UjVw:function(t,n,e){"use strict";var r={currentUserID:function(t){return t.currentUserID},authed:function(t){return t.authed},currentUser:function(t){return t.currentUser},nexturl:function(t){return t.route.path},whoEdit:function(t){return t.whoEdit},indexRuts:function(t){return t.rut.indexRuts},showTags:function(t){return t.rut.showTags},rutDetail:function(t){return t.rut.rutDetail},totalClips:function(t){return t.clip.totalClips},currentP:function(t){return t.clip.currentP},maxP:function(t){return t.clip.maxP},currentClips:function(t){return t.clip.currentClips},totalDemands:function(t){return t.demand.totalDemands},currentD:function(t){return t.demand.currentD},maxD:function(t){return t.demand.maxD},currentDemands:function(t){return t.demand.currentDemands},demandDetail:function(t){return t.demand.demandDetail},currentItem:function(t){return t.item.currentItem},reviewDetail:function(t){return t.item.reviewDetail},searchItems:function(t){return t.item.searchItems},itemKeyword:function(t){return t.item.itemKeyword},totalHeadlines:function(t){return t.headline.totalHeadlines},currentH:function(t){return t.headline.currentH},maxH:function(t){return t.headline.maxH},currentHeadlines:function(t){return t.headline.currentHeadlines}};n.a=r},XMX0:function(t,n,e){"use strict";var r=e("//Fk"),u=e.n(r),i=e("P9l9"),o={indexRuts:[],showTags:[],rutDetail:{}},a={getRut:function(t,n){var e=t.commit;return new u.a(function(t,r){Object(i.W)(n).then(function(n){e("SET_RUT",n.data),t(n)}).catch(function(t){r(t)})})}},c={SET_INDEX:function(t,n){t.indexRuts=n.ruts,t.showTags=n.tags.slice(0,20)},SET_RUT:function(t,n){t.rutDetail=n},NEW_TAGS:function(t,n){t.rutDetail.tags=n}};n.a={state:o,actions:a,mutations:c}},YaEn:function(t,n,e){"use strict";var r=e("7+uW"),u=e("/ocq"),i=e("IcnI"),o=e("P9l9");r.default.use(u.a);var a=function(){return e.e(6).then(e.bind(null,"Irp/"))},c=function(){return e.e(31).then(e.bind(null,"pEKy"))},s=function(){return e.e(33).then(e.bind(null,"epzP"))},f=function(){return e.e(32).then(e.bind(null,"Jt/w"))},d=function(){return e.e(3).then(e.bind(null,"Yhyb"))},l=function(){return e.e(30).then(e.bind(null,"jXjW"))},p=function(){return e.e(8).then(e.bind(null,"Mmy0"))},m=function(){return e.e(29).then(e.bind(null,"Ky3J"))},h=function(){return e.e(4).then(e.bind(null,"ZM+T"))},v=function(){return e.e(1).then(e.bind(null,"b3vX"))},g=function(){return e.e(0).then(e.bind(null,"k4/l"))},b=function(){return e.e(2).then(e.bind(null,"z57P"))},_=function(){return e.e(7).then(e.bind(null,"ma6q"))},w=function(){return e.e(28).then(e.bind(null,"2Jx5"))},E=function(){return e.e(27).then(e.bind(null,"otog"))},D=function(){return e.e(37).then(e.bind(null,"kTq1"))},I=function(){return e.e(40).then(e.bind(null,"I7sH"))},k=function(){return e.e(39).then(e.bind(null,"7Vuz"))},T=function(){return e.e(36).then(e.bind(null,"RrFR"))},y=function(){return e.e(41).then(e.bind(null,"X6Vi"))},S=function(){return e.e(38).then(e.bind(null,"LoBU"))},O=function(){return e.e(16).then(e.bind(null,"Yg2C"))},C=function(){return e.e(15).then(e.bind(null,"/BCD"))},x=function(){return e.e(10).then(e.bind(null,"tpqG"))},R=function(){return e.e(14).then(e.bind(null,"dWBv"))},P=function(){return e.e(11).then(e.bind(null,"hTVM"))},M=function(){return e.e(20).then(e.bind(null,"Ls1q"))},N=function(){return e.e(18).then(e.bind(null,"JLnY"))},H=function(){return e.e(19).then(e.bind(null,"TIKV"))},j=function(){return e.e(5).then(e.bind(null,"UZPP"))},L=function(t){return function(){return e.e(23).then(e.bind(null,"oTxi")).then(function(n){return n.default(t)})}},A=function(t){return function(){return e.e(22).then(e.bind(null,"tQu9")).then(function(n){return n.default(t)})}},F=function(t){return function(){return e.e(13).then(e.bind(null,"Ahar")).then(function(n){return n.default(t)})}},U=function(t){return function(){return e.e(12).then(e.bind(null,"j6oK")).then(function(n){return n.default(t)})}},$=function(t){return function(){return e.e(9).then(e.bind(null,"G/o+")).then(function(n){return n.default(t)})}},W=function(){return e.e(17).then(e.bind(null,"dbCm"))},K=function(){return e.e(26).then(e.bind(null,"AORQ"))},q=function(){return e.e(21).then(e.bind(null,"Ti2K"))},G=function(){return e.e(34).then(e.bind(null,"W4mg"))},z=function(){return e.e(25).then(e.bind(null,"Y9vY"))},V=function(){return e.e(35).then(e.bind(null,"6j0K"))},X=function(){return e.e(24).then(e.bind(null,"2wh8"))},Y=function(t,n,e){return e||{x:0,y:0}},B=function(t,n,e){var u=i.a.getters.currentUserID,a=i.a.getters.rutDetail.id;u&&a?Object(o.b)(u,a).then(function(t){t.data.canedit?e():(i.a.commit("SET_WHOEDIT",t.data),(new r.default).$message("In Editing...Please Try Later"))}):(new r.default).$message("In Editing...Please Go back")},J=function(t,n,e){var r=i.a.getters.currentUserID,u=t.params.id;r===Number(u)&&e()},Z=new u.a({mode:"history",fallback:!1,scrollBehavior:Y,routes:[{path:"/",component:a,name:"Home"},{path:"/feeds",component:c,name:"Feeds",meta:{auth:!0}},{path:"/register",component:D,name:"Register"},{path:"/confirm/:token",component:I,name:"Confirm",meta:{auth:!0}},{path:"/forget",component:k,name:"Forget"},{path:"/reset/:token",component:T,name:"ResetPsw"},{path:"/changepsw",component:y,name:"ChangePsw"},{path:"/login",component:S,name:"Login"},{path:"/tag/:id",component:_,name:"Tag"},{path:"/create/:id(\\d+)?",component:O,name:"CreateRut",meta:{auth:!0}},{path:"/readuplist/:id",component:h,name:"Rutview"},{path:"/edit/readuplist/:id",component:C,name:"EditRut",meta:{auth:!0},beforeEnter:B},{path:"/additemto/readuplist/:id",component:x,name:"AddItem",meta:{auth:!0},beforeEnter:B},{path:"/edit/readuptips/:id",component:R,name:"EditTips",meta:{auth:!0},beforeEnter:B},{path:"/commenton/rut/:id",component:v,name:"RutComment"},{path:"/item/:id",component:g,name:"Item"},{path:"/myrc/item/:itemid",component:j,name:"MyRc",props:!0,meta:{auth:!0}},{path:"/edit/item/:id",component:M,name:"EditItem",meta:{auth:!0}},{path:"/review/item/:id",component:N,name:"NewReview",meta:{auth:!0}},{path:"/editreview/:id",component:H,name:"EditReview",meta:{auth:!0}},{path:"/review/:id",component:b,name:"ReviewView"},{path:"/demands",component:f,children:[{path:"",name:"defaultdemand",redirect:"popular"},{path:"popular",name:"Populardemand",component:A("popular")},{path:"new",name:"Newdemand",component:A("new")}]},{path:"/demand/:id",name:"demand",component:d},{path:"/challenge",component:s,meta:{auth:!0},children:[{path:"",name:"defaultclip",redirect:"hotclip"},{path:"myclip",name:"Myclip",component:L({ref:"My"}),meta:{auth:!0}},{path:"hotclip",name:"Hotclip",component:L({ref:"Hot"}),meta:{auth:!0}},{path:"allclip",name:"Allclip",component:L({ref:"All"}),meta:{auth:!0}}]},{path:"/headline/:id",name:"Headline",component:p},{path:"/headlines",component:l,children:[{path:"",name:"defaultheadline",redirect:"top"},{path:"top",name:"TopHeadline",component:F("top")},{path:"new",name:"NewHeadline",component:F("new")}]},{path:"/profile/:id",component:m,children:[{path:"",name:"defaultProfile",redirect:"activity"},{path:"activity",name:"Activity",component:G},{path:"created",name:"CreatedRuts",component:U("created")},{path:"star",name:"StarRuts",component:U("star")},{path:"challenge",name:"ChallengeRuts",component:U("challenge")},{path:"working",name:"WorkingItems",component:$("doing")},{path:"scheduled",name:"ScheduledItems",component:$("todo")},{path:"havedone",name:"DoneItems",component:$("done")},{path:"reviews",name:"Reviews",component:W},{path:"demands",name:"Demands",component:K},{path:"clips",name:"Clips",component:q},{path:"followeds",name:"Followeds",component:X}]},{path:"/setting/:id",component:z,children:[{path:"",name:"defaultSetting",redirect:"setting"},{path:"setting",name:"Setting",component:V,beforeEnter:J,meta:{auth:!0}},{path:"change",name:"Change",component:y,beforeEnter:J,meta:{auth:!0}}]},{path:"/newitem",component:P,name:"NewItem",meta:{auth:!0}},{path:"/searchresult/:type",component:w,name:"SearchResult",props:!0},{path:"/404",component:E,name:"NotFound",hidden:!0},{path:"*",hidden:!0,redirect:{path:"/404"}}]});n.a=Z},abK8:function(t,n){},bDIs:function(t,n,e){"use strict";e.d(n,"a",function(){return r}),e.d(n,"b",function(){return u});var r=function(){var t=this,n=t.$createElement;return(t._self._c||n)("div",{staticClass:"progress",style:{width:t.percent+"%",height:t.height,"background-color":t.canSuccess?t.color:t.failedColor,opacity:t.show?1:0}})},u=[]},"hTt+":function(t,n,e){"use strict";var r=e("Gu7T"),u=e.n(r),i=e("//Fk"),o=e.n(i),a=e("P9l9"),c={currentItem:{},reviewDetail:{},searchItems:[],itemKeyword:""},s={getItem:function(t,n){var e=t.commit;return new o.a(function(t,r){Object(a.M)(n).then(function(n){e("SET_ITEM",n.data),t(n)}).catch(function(t){r(t)})})},getReview:function(t,n){var e=t.commit;return new o.a(function(t,r){Object(a.U)(n).then(function(n){e("SET_REVIEW",n.data),t(n)}).catch(function(t){r(t)})})}},f={SET_ITEM:function(t,n){t.currentItem=n},SET_REVIEW:function(t,n){t.reviewDetail=n},SET_SEARCH_ITEMS:function(t,n){t.searchItems=n.items,t.itemKeyword=n.keyword},MORE_SEARCH_ITEMS:function(t,n){var e;(e=t.searchItems).push.apply(e,u()(n.items))}};n.a={state:c,actions:s,mutations:f}},iF09:function(t,n,e){"use strict";function r(){return d.a.get(p)}function u(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0;return d.a.set(p,t,{expires:n})}function i(){return d.a.remove(p)}function o(){return d.a.get(m)}function a(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0;return d.a.set(m,t,{expires:n})}function c(){return d.a.remove(m)}function s(){var t=r();return l.default.defaults.auth={username:t,password:t},!!t}n.c=r,n.g=u,n.e=i,n.b=o,n.f=a,n.d=c,n.a=s;var f=e("lbHh"),d=e.n(f),l=e("NHnr"),p="R-Token",m="R-ID"},l3im:function(t,n,e){"use strict";function r(t){e("0Stc")}var u=e("zf/q"),i=e("6rOw"),o=e("XyMi"),a=r,c=Object(o.a)(u.a,i.a,i.b,!1,a,"data-v-43a7b585",null);n.a=c.exports},tvR6:function(t,n){},xJD8:function(t,n,e){"use strict";var r=e("Dd8w"),u=e.n(r),i=e("NYxO"),o=e("l3im");n.a={name:"app",components:{LoginForm:o.a},data:function(){return{searchWord:"",toLogin:!1}},computed:u()({},Object(i.b)(["currentUserID","authed"])),methods:{onLogout:function(){this.$store.commit("DEL_TOKEN"),this.$router.push("/")},siteSearch:function(){var t=this.searchWord;return""!==t&&(window.open("https://www.google.com/search?q=site:readup.tips/%20"+t,"_blank"),!1)}}}},yYt1:function(t,n,e){"use strict";var r=e("Gu7T"),u=e.n(r),i=e("P9l9"),o={totalHeadlines:0,currentHeadlines:[],currentH:0,maxH:0},a={getHeadlines:function(t,n){var e=t.commit;Object(i.I)(n).then(function(t){e("SET_HEADLINES",t.data)})},postHeadline:function(t,n){var e=t.commit;Object(i._15)(n).then(function(t){e("ADD_HEADLINE",t.data)})},moreHeadlines:function(t,n){var e=t.commit;Object(i.I)(n).then(function(t){e("MORE_HEADLINES",t.data.headlines)})}},c={SET_HEADLINES:function(t,n){t.totalHeadlines=n.total,t.currentH=1,t.maxH=Math.ceil(n.total/20),t.currentHeadlines=n.headlines},MORE_HEADLINES:function(t,n){var e;t.currentH+=1,(e=t.currentHeadlines).push.apply(e,u()(n))},ADD_HEADLINE:function(t,n){t.currentHeadlines.unshift(n)}};n.a={state:o,actions:a,mutations:c}},"zf/q":function(t,n,e){"use strict";n.a={name:"login-form",props:["next"],data:function(){return{loginForm:{username:"",password:""},rules:{username:[{required:!0,message:"Please enter username",trigger:"blur"}],password:[{required:!0,message:"Please enter password",trigger:"blur"}]},pwdType:"password"}},methods:{onLogin:function(t,n){var e=this;this.$refs[t].validate(function(t){if(!t)return e.$message("error!! Please Check"),!1;e.$axios.defaults.auth={username:n.username,password:n.password},e.$store.dispatch("loginUser").then(function(){var t="current"===e.next?e.$route.fullPath:e.$route.query.redirect||"/challenge";e.$router.push(t),e.$emit("close")}).catch(function(){e.$message({showClose:!0,duration:0,message:"oops...Please Check Account or Password",type:"error"})})})},toNext:function(t){this.$router.push(t),this.$emit("close")}}}}},["NHnr"]);
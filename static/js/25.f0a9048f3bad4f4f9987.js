webpackJsonp([25],{"72el":function(t,e,i){"use strict";i.d(e,"a",function(){return a}),i.d(e,"b",function(){return r});var a=function(){var t=this,e=t.$createElement,i=t._self._c||e;return t.userid?i("div",{staticClass:"setting-page"},[i("div",{staticClass:"setting-view"},[i("router-view")],1),t._v(" "),i("div",{staticClass:"setting-side"},[i("div",{staticClass:"right-avatar"},[i("img",{staticClass:"avatar",attrs:{src:t.currentUser.avatar,alt:"Avatar"}}),t._v(" "),i("p",{staticClass:"user-info"},[t._v("From: "+t._s(t.currentUser.location||"Unknown"))])]),t._v(" "),i("div",{staticClass:"right-nav"},[i("router-link",{attrs:{to:"/setting/"+t.userid+"/setting"}},[t._v("Edit Profile")]),t._v(" "),i("br"),t._v(" "),i("router-link",{attrs:{to:"/setting/"+t.userid+"/change"}},[t._v("\n        Change Password\n      ")]),t._v(" "),i("br"),t._v(" "),t.confirmed?t._e():i("el-button",{attrs:{type:"text"},on:{click:t.reconfirm}},[t._v("\n        Confirm My Email\n      ")]),t._v(" "),i("br"),t._v(" "),i("el-button",{attrs:{type:"text"},on:{click:function(e){t.showDialog=!0}}},[t._v("Invite Friends")]),t._v(" "),i("el-dialog",{attrs:{title:"Share Link To Invite Your Friends",visible:t.showDialog},on:{"update:visible":function(e){t.showDialog=e}}},[i("b",[t._v("Send this Link to Invite Your Friend To Readup.Tips")]),t._v(" "),i("p",{staticStyle:{color:"green"}},[t._v(t._s(t.invitelink))]),t._v(" "),i("share-bar",{attrs:{passTitle:"Invite You To Readup.Tips",passUrl:t.invitelink}})],1)],1)])]):t._e()},r=[]},CNqu:function(t,e,i){var a=i("G2nt");"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);i("rjj0")("3b3e72d2",a,!0,{})},G2nt:function(t,e,i){e=t.exports=i("FZ+f")(!1),e.push([t.i,"#social-share-bar[data-v-755a1738]{text-align:right}#social-share-bar>.share-link[data-v-755a1738]{cursor:pointer;display:inline-block;text-align:center}#social-share-bar>.share-link.evernote[data-v-755a1738]:hover{background-color:#8be056}#social-share-bar>.share-link.twitter[data-v-755a1738]:hover{background-color:#55acee}#social-share-bar>.share-link.facebook[data-v-755a1738]:hover{background-color:#3b5998}#social-share-bar>.share-link.google-plus[data-v-755a1738]:hover{background-color:#dd4b39}#social-share-bar>.share-link.linkedin[data-v-755a1738]:hover{background-color:#007bb5}#social-share-bar>.share-link .icon[data-v-755a1738]{padding:5px;width:16px;height:16px}",""])},PEd3:function(t,e,i){"use strict";i.d(e,"a",function(){return a}),i.d(e,"b",function(){return r});var a=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{attrs:{id:"social-share-bar"}},[i("a",{staticClass:"share-link twitter",attrs:{title:"Twitter",rel:"nofollow noopener noreferrer"},on:{click:function(e){e.preventDefault(),t.shareWindow("https://twitter.com/share?text="+t.title()+"&url="+t.url)}}},[i("img",{staticClass:"icon",attrs:{alt:"TW",src:"/static/pic/twitter.svg"}})]),t._v(" "),i("a",{staticClass:"share-link facebook",attrs:{title:"Facebook",rel:"nofollow noopener noreferrer"},on:{click:function(e){e.preventDefault(),t.shareWindow("https://www.facebook.com/sharer/sharer.php?u="+t.url)}}},[i("img",{staticClass:"icon",attrs:{alt:"FB",src:"/static/pic/facebook.svg"}})]),t._v(" "),i("a",{staticClass:"share-link linkedin",attrs:{title:"Linkedin",rel:"nofollow noopener noreferrer"},on:{click:function(e){e.preventDefault(),t.shareWindow("https://www.linkedin.com/shareArticle?mini=true&url="+t.url+"&title="+t.title())}}},[i("img",{staticClass:"icon",attrs:{alt:"Linkedin",src:"/static/pic/linkedin.svg"}})]),t._v(" "),i("a",{staticClass:"share-link google-plus",attrs:{title:"Google+",rel:"nofollow noopener noreferrer"},on:{click:function(e){e.preventDefault(),t.shareWindow("https://plus.google.com/share?url="+t.url)}}},[i("img",{staticClass:"icon",attrs:{alt:"G+",src:"/static/pic/gplus.svg"}})]),t._v(" "),i("a",{staticClass:"share-link evernote",attrs:{title:"Evernote",rel:"nofollow noopener noreferrer"},on:{click:function(e){e.preventDefault(),t.shareWindow("https://www.evernote.com/clip.action?url="+t.url+"&title="+t.title())}}},[i("img",{staticClass:"icon",attrs:{alt:"Evernote",src:"/static/pic/evernote.svg"}})])])},r=[]},Y9vY:function(t,e,i){"use strict";function a(t){i("ZIYK")}Object.defineProperty(e,"__esModule",{value:!0});var r=i("q10I"),n=i("72el"),s=i("XyMi"),o=a,c=Object(s.a)(r.a,n.a,n.b,!1,o,"data-v-2b7b1c30",null);e.default=c.exports},ZCVe:function(t,e,i){"use strict";function a(t){i("CNqu")}var r=i("r8Lr"),n=i("PEd3"),s=i("XyMi"),o=a,c=Object(s.a)(r.a,n.a,n.b,!1,o,"data-v-755a1738",null);e.a=c.exports},ZIYK:function(t,e,i){var a=i("fU7i");"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);i("rjj0")("b821a8f0",a,!0,{})},fU7i:function(t,e,i){e=t.exports=i("FZ+f")(!1),e.push([t.i,".setting-page[data-v-2b7b1c30]{padding:10px 240px 10px 0;position:relative}.setting-page .setting-view[data-v-2b7b1c30]{padding:auto}.setting-page .setting-side[data-v-2b7b1c30]{position:absolute;top:10px;right:0;width:220px;background-color:#fff}.setting-page .setting-side .right-avatar[data-v-2b7b1c30]{background-color:#e5ebe4;min-height:80px;padding:5px;position:relative}.setting-page .setting-side .right-avatar .avatar[data-v-2b7b1c30]{width:60px;height:80px}.setting-page .setting-side .right-avatar .user-info[data-v-2b7b1c30]{position:absolute;top:10px;right:0;width:145px}.setting-page .setting-side .right-nav[data-v-2b7b1c30]{padding:5px 20px}.setting-page .setting-side .right-nav a[data-v-2b7b1c30]{color:gray;line-height:28px;font-weight:400}.setting-page .setting-side .right-nav a[data-v-2b7b1c30]:hover{color:#006400}.setting-page .setting-side .right-nav a.router-link-active[data-v-2b7b1c30]{color:green;font-weight:800}",""])},q10I:function(t,e,i){"use strict";var a=i("Dd8w"),r=i.n(a),n=i("ZCVe"),s=i("P9l9"),o=i("NYxO");e.a={name:"setting",title:"Setting",components:{ShareBar:n.a},data:function(){return{showDialog:!1,userid:"",confirmed:!0}},computed:r()({},Object(o.b)(["currentUser"]),{invitelink:function(){return"https://readup.tips/register?refcode="+this.currentUser.recode}}),methods:{loadAuthedUser:function(){var t=this,e=this.currentUser,i=this.$route.params.id;e&&e.id===Number(i)?(this.userid=e.id,this.confirmed=e.confirmed):this.$store.dispatch("getCurrentUser").then(function(e){t.userid=e.data.id,t.confirmed=e.data.confirmed})},reconfirm:function(){var t=this;Object(s._20)().then(function(e){t.$message({showClose:!0,message:e.data})})}},created:function(){this.loadAuthedUser()}}},r8Lr:function(t,e,i){"use strict";e.a={name:"share-bar",props:{passUrl:String,passTitle:String,prefix:{type:String,default:""}},computed:{url:function(){return this.passUrl||"https://readup.tips"+this.$route.fullPath}},methods:{title:function(){try{if(document)return this.prefix+(this.passTitle||document.title)}catch(t){return"Readup.Tips"}},shareWindow:function(t){t=encodeURI(t),console.log(t);var e=screen.availWidth/2,i=screen.availHeight/5*2,a=(screen.availHeight-i)/2,r=(screen.availWidth-e)/2,n="top="+a+",left="+r+",width="+e+",height="+i+",scrollbars=0,status=0,menubar=0,resizable=2,location=0";window.open(t,"newWin",n).focus()}}}}});
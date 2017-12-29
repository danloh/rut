// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import VueQuillEditor from 'vue-quill-editor'
import ProgressBar from './components/Misc/ProgressBar.vue'
import titleMixin from './util/title'
import * as filters from './util/filters'
import { getToken } from '@/util/auth'
import App from './App'
import router from './router'
import store from './store'

Vue.config.productionTip = false

// UI + en
Vue.use(ElementUI, { locale })

// rich Text editor
const editorOption = {
  theme: 'snow',
  placeholder: 'Compose...',
  modules: {
    toolbar: [
      ['bold', 'underline'],
      [{ 'list': 'ordered' }, { 'list': 'bullet' }],
      [{ 'color': [] }, { 'background': [] }],
      ['blockquote'],
      ['link'],
      ['clean']
    ]
  }
}
Vue.use(VueQuillEditor, editorOption)

// progress bar, reder off-document and append afterwards
const bar = Vue.prototype.$bar = new Vue(ProgressBar).$mount()
document.body.appendChild(bar.$el)

// mixin title handler
Vue.mixin(titleMixin)

// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

// Axios config
// Request interceptor
axios.interceptors.request.use(
  config => {
    let token = store.state.token
    if (token) {
      config.headers.Authorization = `token ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)
// Response interceptor
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          store.commit('DEL_TOKEN')
          new Vue().$message('Oops...Access Denied, Need To Log in')
          if (router.currentRoute.path !== '/login') {
            router.push({
              path: '/login',
              query: {redirect: router.currentRoute.fullPath}
            })
          }
          break
        case 403:
          new Vue().$message('Oops...Operation Forbidden')
          break
        case 404:
          new Vue().$message('The Resource You Requested Was Not Found')
          router.replace({ path: '/404' })
          break
        case 418:
          new Vue().$message('Eureka! 42')
          break
        case 500:
          new Vue().$message('Oops...Internal Server Error')
          router.replace({ path: '/' })
          break
      }
    }
    // console.log(error.response.data)
    return Promise.reject(error)
  }
)

// config router
// check auth when login required( define in meta // need to tackle some issue!!
router.beforeEach((to, from, next) => {
  bar.start()
  if (to.meta.auth) {
    // config axios defaul auth??!!
    let localToken = getToken()
    axios.defaults.auth = {
      username: localToken,
      password: localToken
    }
    if (localToken) {
      next()
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath} // redirect after login
      })
    }
  } else {
    next()
  }
})
// finish bar after route
router.afterEach(() => {
  bar.finish()
})

// register axios as default http client
Vue.prototype.$axios = axios
export default axios

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

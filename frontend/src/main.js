// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en'
import ProgressBar from './components/Misc/ProgressBar.vue'
import titleMixin from './util/title'
import * as filters from './util/filters'
import App from './App'
import router from './router'
import store from './store'

Vue.config.productionTip = false

// UI + en
Vue.use(ElementUI, { locale })
// progress bar, reder off-document and append afterwards
const bar = Vue.prototype.$bar = new Vue(ProgressBar).$mount()
document.body.appendChild(bar.$el)

// mixin title handler
Vue.mixin(titleMixin)

// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

// config axios
// defaul auth
axios.defaults.auth = {
  username: '',
  password: ''
}
// Request interceptor
axios.interceptors.request.use((config) => {
  if (store.state.token) {
    config.headers['X-Token'] = store.state.token
  }
  return config
}, (error) => {
  return Promise.reject(error)
})
// Response interceptor
axios.interceptors.response.use((response) => {
  return response
}, (error) => {
  if (error.response) {
    switch (error.response.status) {
      case 401:
        store.commit('DEL_TOKEN')
        router.push('/login')
    }
  }
  return Promise.reject(error.response.data)
})

// config router
// check auth when login required( define in meta // need to tackle some issue!!
router.beforeEach((to, from, next) => {
  bar.start()
  if (to.meta.auth) {
    let localToken = localStorage.token
    let localID = localStorage.userid
    if (localToken) {
      axios.defaults.auth = {
        username: localToken,
        password: localToken
      }
      store.commit('SET_TOKEN', localToken)
      store.commit('SET_USER', Number(localID))
      next()
    } else {
      next({path: '/login'})
    }
  } else {
    next()
  }
})

router.afterEach(() => {
  bar.finish()
})

Vue.prototype.$axios = axios
export default axios

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

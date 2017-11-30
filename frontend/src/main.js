// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en'
import ProgressBar from './components/ProgressBar.vue'
import App from './App'
import router from './router'
import store from './store'

// UI + en
Vue.use(ElementUI, { locale })
// progress bar, reder off-document and append afterwards
const bar = Vue.prototype.$bar = new Vue(ProgressBar).$mount()
document.body.appendChild(bar.$el)

Vue.config.productionTip = false

// config axios
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
// check auth when login required( define in meta
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
      store.commit('SET_USER', localID)
      next()
      bar.finish()
    } else {
      next({path: '/login'})
    }
  } else {
    next()
    bar.finish()
  }
})

Vue.prototype.$axios = axios
export default axios

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

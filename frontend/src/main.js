// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/en'
import App from './App'
import router from './router'
import store from './store'

Vue.use(ElementUI, { locale })
Vue.config.productionTip = false

// config axios
axios.defaults.auth = {
  username: '',
  password: ''
}

// config router
// check auth when login required( define in meta)
router.beforeEach((to, from, next) => {
  if (to.meta.auth) {
    let localToken = localStorage.token
    if (localToken) {
      axios.default.auth = {
        username: store.state.token,
        password: store.state.token
      }
      next()
    } else {
      next({path: '/login'})
    }
  } else {
    next()
  }
})

Vue.prototype.$axios = axios

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

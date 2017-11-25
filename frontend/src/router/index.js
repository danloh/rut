import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

// import components
import Home from '../view/Home'
import Register from '../components/Register'
import Login from '../components/Login'
import Challenge from '../view/Challenge'
import Demands from '../view/Demands'
import Profile from '../view/Profile'
import RutView from '../view/RutView'
import Connect from '../components/Connect'
import Create from '../components/Create'
import ItemView from '../view/ItemView'
import createClipList from '../components/CreateClipList'

const router = new Router({
  mode: 'history',
  fallback: false,
  routes: [
    { path: '/', component: Home, name: 'Home', meta: {auth: true} },
    { path: '/register', component: Register, name: 'Register' },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/demand', component: Demands, name: 'Demands' },
    { path: '/connect', component: Connect, name: 'Connect' },
    { path: '/create', component: Create, name: 'Create', meta: {auth: true} },
    { path: '/profile/:id', component: Profile, name: 'Profile' },
    { path: '/readuplist/:id', component: RutView, name: 'Rutview' },
    { path: '/item/:id', component: ItemView, name: 'Itemview' },
    { path: '/challenge',
      component: Challenge,
      meta: {auth: true},
      children: [
        { path: '', name: 'Myclip', component: createClipList() },
        { path: 'allclip', name: 'Allclip', component: createClipList('allclip', {ref: 'All'}) }
      ]
    }
  ]
})

// router.beforeEach((to, from, next) => {
//   if (to.meta.auth) {
//     store.dispatch('VERIFY').then((v) => {
//       if (v) {
//         next()
//       } else {
//         store.commit('MOD_NEXT', to.path)
//         next({ path: '/connect' })
//       }
//     })
//   } else {
//     next()
//   }
// })

export default router

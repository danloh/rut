import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import store from '@/store'
// import components
import Home from '@/view/Home'
import Challenge from '@/view/Challenge'
import Demands from '@/view/Demands'
import DemandView from '@/view/DemandView'
import Profile from '@/view/Profile'
import RutView from '@/view/RutView'
import ItemView from '@/view/ItemView'
import TagView from '@/view/TagView'
import Register from '@/components/Register'
import Login from '@/components/Login'
import Connect from '@/components/Connect'
import Create from '@/components/Rut/Create'
import EditRut from '@/components/Rut/EditRut'
import AddItem from '@/components/Rut/AddItem'
import EditTips from '@/components/Rut/EditTips'
import EditItem from '@/components/Item/EditItem'
import createClipList from '@/components/Challenge/CreateClipList'
import createDemandList from '@/components/Demand/CreateDemandList'
import createReviewList from '@/components/Item/CreateReviewList'
import createProfileRuts from '@/components/Profile/CreateProfileRuts'
import createProfileItems from '@/components/Profile/CreateProfileItems'

// for go back / forward scrollBehavior
const scrollBehavior = (to, from, savedPosition) => {
  if (savedPosition) {
    return savedPosition
  } else {
    const position = {x: 0, y: 0}
    return position
  }
}
// for auth edit rut
const beforeEnter = (to, from, next) => {
  let currentUserID = store.getters.currentUserID
  let creatorID = store.getters.rutDetail.creator.id
  if (currentUserID === creatorID) {
    next()
  }
}

const router = new Router({
  mode: 'history',
  fallback: false,
  scrollBehavior, // : () => ({y: 0}),
  routes: [
    { path: '/', component: Home, name: 'Home', meta: {auth: true} },
    { path: '/register', component: Register, name: 'Register' },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/connect', component: Connect, name: 'Connect' },
    { path: '/tag/:id', component: TagView, name: 'Tag' },
    { path: '/create/:id(\\d+)?', component: Create, name: 'CreateRut', meta: {auth: true} },
    { path: '/readuplist/:id', component: RutView, name: 'Rutview' },
    { path: '/edit/readuplist/:id',
      component: EditRut,
      name: 'EditRut',
      meta: {auth: true},
      beforeEnter
    },
    { path: '/additemto/readuplist/:id',
      component: AddItem,
      name: 'AddItem',
      meta: {auth: true},
      beforeEnter
    },
    { path: '/edit/readuptips/:id',
      component: EditTips,
      name: 'EditTips',
      meta: {auth: true},
      beforeEnter
    },
    { path: '/item/:id',
      component: ItemView,
      children: [
        { path: '', name: 'defaultreview', redirect: 'hotreview' },
        { path: 'hotreview', name: 'Hotreview', component: createReviewList('hot') },
        { path: 'newreview', name: 'Newreview', component: createReviewList('new') }
      ]
    },
    { path: '/edit/item/:id',
      component: EditItem,
      name: 'EditItem',
      meta: {auth: true}
    },
    { path: '/demands',
      component: Demands,
      children: [
        { path: '', name: 'defaultdemand', redirect: 'popular' },
        { path: 'popular', name: 'Populardemand', component: createDemandList() },
        { path: 'new', name: 'Newdemand', component: createDemandList('new') }
      ]
    },
    { path: '/demand/:id', name: 'demand', component: DemandView },
    { path: '/challenge',
      component: Challenge,
      meta: {auth: true},
      children: [
        { path: '', name: 'defaultclip', redirect: 'myclip' },
        { path: 'myclip', name: 'Myclip', component: createClipList(), meta: {auth: true} },
        { path: 'allclip', name: 'Allclip', component: createClipList('allclip', {ref: 'All'}), meta: {auth: true} }
      ]
    },
    { path: '/profile/:id',
      component: Profile,
      children: [
        { path: '', name: 'defaultPruts', redirect: 'created' },
        { path: 'created', name: 'CreatedRuts', component: createProfileRuts('created') },
        { path: 'star', name: 'StarRuts', component: createProfileRuts('star') },
        { path: 'challenge', name: 'ChallengeRuts', component: createProfileRuts('challenge') },
        { path: 'working', name: 'WorkingItems', component: createProfileItems('doing') },
        { path: 'scheduled', name: 'ScheduledItems', component: createProfileItems('todo') },
        { path: 'havedone', name: 'DoneItems', component: createProfileItems('done') }
      ]
    }
  ]
})

export default router

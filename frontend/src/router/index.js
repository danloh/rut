import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

// import components
import Home from '@/view/Home'
import Register from '@/components/Register'
import Login from '@/components/Login'
import Challenge from '@/view/Challenge'
import Demands from '@/view/Demands'
import Profile from '@/view/Profile'
import RutView from '@/view/RutView'
import TagView from '@/view/TagView'
import Connect from '@/components/Connect'
import Create from '@/components/Create'
import ItemView from '@/view/ItemView'
import createClipList from '@/components/Challenge/CreateClipList'
import createDemandList from '@/components/Demand/CreateDemandList'
import createReviewList from '@/components/Item/CreateReviewList'
import createProfileRuts from '@/components/Profile/CreateProfileRuts'
import createProfileItems from '@/components/Profile/CreateProfileItems'

const router = new Router({
  mode: 'history',
  fallback: false,
  routes: [
    { path: '/', component: Home, name: 'Home', meta: {auth: true} },
    { path: '/register', component: Register, name: 'Register' },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/connect', component: Connect, name: 'Connect' },
    { path: '/create', component: Create, name: 'Create', meta: {auth: true} },
    { path: '/readuplist/:id', component: RutView, name: 'Rutview' },
    { path: '/tag/:id', component: TagView, name: 'Tag' },
    { path: '/item/:id',
      component: ItemView,
      children: [
        { path: '', name: 'defaultreview', redirect: 'hotreview' },
        { path: 'hotreview', name: 'hotreview', component: createReviewList('hot') },
        { path: 'newreview', name: 'newreview', component: createReviewList('new') }
      ]
    },
    { path: '/demand',
      component: Demands,
      children: [
        { path: '', name: 'defaultdemand', redirect: 'popular' },
        { path: 'popular', name: 'populardemand', component: createDemandList() },
        { path: 'new', name: 'newestdemand', component: createDemandList('new') }
      ]
    },
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

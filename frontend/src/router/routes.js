// import componments
import Home from '../view/Home'
import Challenge from '../view/Challenge'
import Demands from '../view/Demands'
import Profile from '../view/Profile'
import RutView from '../view/RutView'
import Connect from '../components/Connect'
import Create from '../components/Create'
import ItemView from '../view/ItemView'

// config routes
let routes = [
    { path: '/', component: Home, name: 'Home', meta: {auth: true} },
    { path: '/challenge', component: Challenge, name: 'Challenge', meta: {auth: true} },
    { path: '/demand', component: Demands, name: 'Demands' },
    { path: '/connect', component: Connect, name: 'Connect' },
    { path: '/create', component: Create, name: 'Create' },
    { path: '/profile/:id', component: Profile, name: 'Profile' },
    { path: '/readuplist/:id', component: RutView, name: 'Rutview' },
    { path: '/item/:id', component: ItemView, name: 'Itemview' }
]

export default routes

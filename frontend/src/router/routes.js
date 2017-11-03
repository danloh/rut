// import componments 
import Home from '../view/Home'
import Challenge from '../view/Challenge'
import Demands from '../view/Demands'
import Profile from '../view/Profile'
import RutView from '../view/RutView'
import Connect from '../components/Connect'
import Create from '../components/Create'

// config routes
let routes = [
    { path: '/', component: Home, name: 'Home' },
    { path: '/challenge', component: Challenge, name: 'Challenge' },
    { path: '/demand', component: Demands, name: 'Demands' },
    { path: '/connect', component: Connect, name: 'Connect' },
    { path: '/create', component: Create, name: 'Create' },
    { path: '/profile/:id', component: Profile, name: 'Profile' },
    { path: '/readuplist/:id', component: RutView, name: 'Rutview' }
];

export default routes;

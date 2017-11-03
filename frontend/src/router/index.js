import Vue from 'vue'
import Router from 'vue-router'
import routes from './routes'
import store from '../store'

Vue.use(Router)

const router = new Router({
  routes
})

// check auth when login required( define in meta)
router.beforeEach((to, from, next) => {
    if (to.meta.auth) {
        store.dispatch('VERIFY').then((v) => {
            if(v){
                next()
            }else{
                store.commit('MOD_NEXT', to.path);
                next({ path: '/connect' });
            }
        })
    }else{
        next()
    }
})

export default router;

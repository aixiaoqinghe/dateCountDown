import Vue from 'vue'
import VueRouter from 'vue-router'

import homeIndex from '../views/home/index.vue'
import loginIndex from '../views/login/index.vue'
import registerIndex from '../views/register/index.vue'

import countDown from '@/views/home/countDown.vue'
import homeHome from '@/views/home/home.vue'
import homeMark from '@/views/home/mark.vue'
import homeMyself from '@/views/home/myself.vue'
import homeSetting from '@/views/home/setting.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/',
      component: homeIndex,
      redirect: '/home',
      children: [
        { path: '/home', component: homeHome },
        { path: '/mark', component: homeMark },
        { path: '/myself', component: homeMyself },
        { path: '/setting', component: homeSetting },
        { path: '/countDown', component: countDown }
      ]
    },
    { path: '/login', component: loginIndex },
    { path: '/register', component: registerIndex }
  ]

})

export default router

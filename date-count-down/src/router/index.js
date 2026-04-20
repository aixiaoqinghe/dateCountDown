import Vue from 'vue'
import Router from 'vue-router'
import login from '@/views/login/index.vue'
import register from '@/views/register/index.vue'
import homeIndex from '@/views/home/index.vue'
import homeHome from '@/views/home/home.vue'
import markHome from '@/views/home/mark.vue'
import countDown from '@/views/home/countDown.vue'
import mine from '@/views/home/myself.vue'
import setting from '@/views/home/setting.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
    {
      path: '/home',
      name: 'homeIndex',
      component: homeIndex,
      children: [
        {
          path: '',
          name: 'homeHome',
          component: homeHome
        },
        {
          path: 'mark',
          name: 'markHome',
          component: markHome
        },
        {
          path: 'countDown',
          name: 'countDown',
          component: countDown
        },
        {
          path: 'mine',
          name: 'mine',
          component: mine
        },
        {
          path: 'setting',
          name: 'setting',
          component: setting
        }
      ]
    }
  ]
})

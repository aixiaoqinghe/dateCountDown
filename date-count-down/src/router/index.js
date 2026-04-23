// 导入路由相关依赖
import { createRouter, createWebHistory } from 'vue-router'

// 导入页面组件
// 登录和注册页面
import login from '@/views/login/index.vue'
import register from '@/views/register/index.vue'
import verify from '@/views/verify/index.vue'
import completeInfo from '@/views/completeInfo/index.vue'

// 主页相关组件
import homeIndex from '@/views/home/index.vue' // 主页容器，包含底部导航栏
import homeHome from '@/views/home/home.vue' // 首页内容
import markHome from '@/views/home/mark.vue' // 商城页面
import countDown from '@/views/home/countDown.vue' // 倒计时页面
import mine from '@/views/home/mine.vue' // 个人中心页面
import setting from '@/views/home/setting.vue' // 设置页面

// 创建路由实例
const router = createRouter({
  // 使用 HTML5 历史模式
  history: createWebHistory(),
  // 路由配置
  routes: [
    // 根路径重定向到主页
    {
      path: '/',
      redirect: '/home'
    },
    // 登录页面路由
    {
      path: '/login',
      name: 'login',
      component: login
    },
    // 注册页面路由
    {
      path: '/register',
      name: 'register',
      component: register
    },
    // 验证码页面路由
    {
      path: '/verify',
      name: 'verify',
      component: verify
    },
    // 完善信息页面路由
    {
      path: '/complete-info',
      name: 'completeInfo',
      component: completeInfo
    },
    // 主页路由（包含子路由）
    {
      path: '/home',
      name: 'homeIndex',
      component: homeIndex, // 主页容器，包含底部导航栏
      children: [
        // 首页子路由（默认显示）
        {
          path: '',
          name: 'homeHome',
          component: homeHome
        },
        // 商城页面子路由
        {
          path: 'mark',
          name: 'markHome',
          component: markHome
        },
        // 倒计时页面子路由
        {
          path: 'countDown',
          name: 'countDown',
          component: countDown
        },
        // 个人中心页面子路由
        {
          path: 'mine',
          name: 'mine',
          component: mine
        },
        // 设置页面子路由
        {
          path: 'setting',
          name: 'setting',
          component: setting
        }
      ]
    }
  ]
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 不需要登录检查，让组件自己处理登录状态
  // 这样可以确保底部导航栏始终显示
  next()
})

// 导出路由实例
export default router

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
import feedback from '@/views/feedback/index.vue' // 反馈意见页面

// 创建路由实例
const router = createRouter({
  // 使用 HTML5 历史模式
  history: createWebHistory(),
  // 路由配置
  routes: [
    // 根路径重定向，根据登录状态决定
    {
      path: '/',
      redirect: () => {
        const isLoggedIn = localStorage.getItem('userInfo') !== null
        return isLoggedIn ? '/home' : '/login'
      }
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
    },
    // 反馈意见页面路由
    {
      path: '/feedback',
      name: 'feedback',
      component: feedback
    }
  ]
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 检查用户是否已登录（通过localStorage中的userInfo判断）
  const isLoggedIn = localStorage.getItem('userInfo') !== null

  // 定义不需要登录的页面
  const noAuthPages = ['login', 'register', 'verify', 'completeInfo']

  // 如果用户未登录且访问的不是不需要登录的页面，跳转到登录页
  if (!isLoggedIn && !noAuthPages.includes(to.name)) {
    next('/login')
  } else if (isLoggedIn && to.name === 'login') {
    next('/home')
  } else {
    next()
  }
})

// 导出路由实例
export default router

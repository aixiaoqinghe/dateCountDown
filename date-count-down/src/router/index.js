// 导入路由相关依赖
import { createRouter, createWebHistory } from 'vue-router'

// 导入页面组件（使用懒加载 + 代码分割）
// 登录和注册页面（首屏关键，优先加载）
const login = () => import(/* webpackChunkName: "auth" */ '@/views/login/index.vue')
const register = () => import(/* webpackChunkName: "auth" */ '@/views/register/index.vue')
const verify = () => import(/* webpackChunkName: "auth" */ '@/views/verify/index.vue')
const completeInfo = () => import(/* webpackChunkName: "auth" */ '@/views/completeInfo/index.vue')

// 主页相关组件（按需加载）
const homeIndex = () => import(/* webpackChunkName: "home" */ '@/views/home/index.vue') // 主页容器
const homeHome = () => import(/* webpackChunkName: "home" */ '@/views/home/home.vue') // 首页内容
const markHome = () => import(/* webpackChunkName: "home" */ '@/views/home/mark.vue') // 商城页面
const countDown = () => import(/* webpackChunkName: "home" */ '@/views/home/countDown.vue') // 倒计时页面
const mine = () => import(/* webpackChunkName: "mine" */ '@/views/home/mine.vue') // 个人中心页面
const setting = () => import(/* webpackChunkName: "mine" */ '@/views/home/setting.vue') // 设置页面
const feedback = () => import(/* webpackChunkName: "feedback" */ '@/views/feedback/index.vue') // 反馈意见页面

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
      meta: { keepAlive: true }, // ✅ 缓存主页容器
      children: [
        // 首页子路由（默认显示）
        {
          path: '',
          name: 'homeHome',
          component: homeHome,
          meta: { keepAlive: true } // ✅ 缓存首页组件
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
          component: countDown,
          meta: { keepAlive: true } // ✅ 添加缓存
        },
        // 个人中心页面子路由
        {
          path: 'mine',
          name: 'mine',
          component: mine,
          meta: { keepAlive: true } // ✅ 添加缓存
        },
        // 设置页面子路由
        {
          path: 'setting',
          name: 'setting',
          component: setting,
          meta: { keepAlive: true } // ✅ 添加缓存
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

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@/styles/common.less'
import 'vant/lib/index.css'
import vantUi from '@/utils/vant-ui.js'
import lazyLoad from '@/directives/lazyLoad.js'

// ✅ 全局重写 fetch，自动添加 baseURL
const BASE_URL = 'https://aixiaoqinghe.pythonanywhere.com'
const originalFetch = window.fetch
window.fetch = async (url, options = {}) => {
  // 如果是相对路径，添加 baseURL
  const fullUrl = url.startsWith('/api/') ? `${BASE_URL}${url}` : url

  // 如果有 token，自动添加到请求头
  const token = localStorage.getItem('access_token')
  if (token) {
    options.headers = options.headers || {}
    options.headers.Authorization = `Bearer ${token}`
  }

  return originalFetch(fullUrl, options)
}

const app = createApp(App)
app.use(router)
app.use(vantUi)
app.directive('lazy', lazyLoad)
app.mount('#app')

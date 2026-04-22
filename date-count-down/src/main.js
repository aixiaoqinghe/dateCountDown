import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@/styles/common.less'
import 'vant/lib/index.css'
import vantUi from '@/utils/vant-ui.js'

const app = createApp(App)
app.use(router)
app.use(vantUi)
app.mount('#app')

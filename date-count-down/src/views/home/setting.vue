<template>
  <div class="setting-container">
    <!-- 顶部通知栏 -->
    <div class="top-notification" v-if="showNotification && currentNotification" @click="showNotificationDetail">
      <div class="notification-content">
        <span class="notification-icon">📢</span>
        <div class="scrolling-text">
          {{ currentNotification.message }}
        </div>
      </div>
      <button class="notification-close" @click.stop="closeNotification">×</button>
    </div>

    <!-- 通知详情弹窗 -->
    <div class="notification-detail-modal" v-if="showNotificationModal && currentNotification">
      <div class="modal-content">
        <div class="modal-header">
          <h3>系统通知详情</h3>
          <button class="modal-close" @click="closeNotificationModal">×</button>
        </div>
        <div class="modal-body">
          <div class="notification-detail-icon">📢</div>
          <h4 class="notification-title">{{ currentNotification.title }}</h4>
          <p class="notification-date">{{ formatDate(currentNotification.start_time) }}</p>
          <div class="notification-content-detail">
            <p v-for="(paragraph, index) in currentNotification.content.split('\n')" :key="index">{{ paragraph }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-btn" @click="closeNotificationModal">我知道了</button>
        </div>
      </div>
    </div>

    <!-- 主题设置弹窗 -->
    <div class="theme-modal" v-if="showThemeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>主题设置</h3>
          <button class="modal-close" @click="closeThemeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="theme-options">
            <div v-for="option in themeOptions" :key="option.value" class="theme-option" @click="selectedTheme = option.value">
              <div class="theme-preview" :class="option.value + '-theme-preview'"></div>
              <div class="theme-info">
                <h4>{{ option.label }}</h4>
                <p v-if="option.value === 'light'">浅色背景，深色文字</p>
                <p v-else>深色背景，浅色文字</p>
              </div>
              <div class="theme-radio" :class="{ active: selectedTheme === option.value }"></div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeThemeModal">取消</button>
          <button class="confirm-btn" @click="applyTheme">确定</button>
        </div>
      </div>
    </div>

    <h2>设置</h2>

    <!-- 其他设置项 -->
    <div class="feature-section">
      <h4 class="section-title">通用设置</h4>
      <div class="feature-item" @click="openThemeModal">
        <span class="feature-icon">🌙</span>
        <span class="feature-name">主题设置</span>
        <span class="feature-arrow">›</span>
      </div>
      <div class="feature-item">
        <span class="feature-icon">🔤</span>
        <span class="feature-name">字体设置</span>
        <span class="feature-arrow">›</span>
      </div>
      <div class="feature-item">
        <span class="feature-icon">🌐</span>
        <span class="feature-name">语言设置</span>
        <span class="feature-arrow">›</span>
      </div>
      <div class="feature-item">
        <span class="feature-icon">🗑️</span>
        <span class="feature-name">清除缓存</span>
        <span class="feature-arrow">›</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { showLoadingToast, showSuccessToast } from 'vant'
// 注意：实际项目中需要安装axios并导入
// import axios from 'axios'

export default {
  name: 'homeSetting',
  setup () {
    const showNotification = ref(false)
    const showNotificationModal = ref(false)
    const notifications = ref([])
    const currentNotification = ref(null)
    let checkInterval = null

    // 主题设置
    const currentTheme = ref(localStorage.getItem('theme') || 'light')
    const showThemeModal = ref(false)
    const themeOptions = [
      { value: 'light', label: '浅色主题' },
      { value: 'dark', label: '深色主题' }
    ]
    const selectedTheme = ref(currentTheme.value)

    // 格式化日期
    const formatDate = function (dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    // 获取通知（模拟后端API返回）
    const fetchNotifications = async function () {
      try {
        // 实际项目中使用以下代码
        // const response = await axios.get('/api/notifications')
        // notifications.value = response.data

        // 模拟后端返回的数据
        notifications.value = [
          {
            id: 1,
            title: '系统维护通知',
            content: '尊敬的用户：\n您好！为了提供更好的服务体验，本应用将于2026年5月1日进行系统维护，预计维护时间为1天。\n维护期间，您可能无法使用部分功能，给您带来的不便敬请谅解。\n维护完成后，我们将为您提供更加稳定和优质的服务。\n感谢您的理解与支持！',
            message: '系统通知：本应用将于2026年5月1日进行系统维护，预计维护时间为1天。',
            start_time: '2026-04-25T00:00:00',
            end_time: '2026-05-02T00:00:00',
            priority: 10
          },
          {
            id: 2,
            title: '新版本通知',
            content: '尊敬的用户：\n您好！我们很高兴地通知您，本应用V2.0版本已正式发布。\n本次更新新增了多种倒计时模板，优化了用户界面，提升了系统性能。\n请及时更新到最新版本，享受更好的使用体验。\n感谢您一直以来的支持！',
            message: '新版本通知：V2.0版本已发布，新增多种倒计时模板。',
            start_time: '2026-04-20T00:00:00',
            end_time: '2026-05-20T00:00:00',
            priority: 8
          }
        ]

        // 显示优先级最高的通知
        if (notifications.value.length > 0) {
          currentNotification.value = notifications.value[0]
          showNotification.value = true
        } else {
          showNotification.value = false
        }
      } catch (error) {
        console.error('获取通知失败:', error)
      }
    }

    // 显示通知详情
    const showNotificationDetail = function () {
      if (currentNotification.value) {
        showNotificationModal.value = true
      }
    }

    // 关闭通知
    const closeNotification = function () {
      showNotification.value = false
    }

    // 关闭通知详情弹窗
    const closeNotificationModal = function () {
      showNotificationModal.value = false
    }

    // 主题设置方法
    const openThemeModal = function () {
      selectedTheme.value = currentTheme.value
      showThemeModal.value = true
    }

    const closeThemeModal = function () {
      showThemeModal.value = false
    }

    const applyTheme = function () {
      showLoadingToast('正在切换主题...')

      // 模拟网络请求延迟
      setTimeout(() => {
        currentTheme.value = selectedTheme.value
        localStorage.setItem('theme', selectedTheme.value)

        // 应用主题到文档
        if (selectedTheme.value === 'dark') {
          document.documentElement.classList.add('dark-theme')
        } else {
          document.documentElement.classList.remove('dark-theme')
        }

        showSuccessToast('主题切换成功')
        showThemeModal.value = false
      }, 1000)
    }

    onMounted(() => {
      // 初始加载通知
      fetchNotifications()

      // 每5分钟检查一次通知
      checkInterval = setInterval(() => {
        fetchNotifications()
      }, 5 * 60 * 1000)

      // 初始化主题
      if (currentTheme.value === 'dark') {
        document.documentElement.classList.add('dark-theme')
      }
    })

    onUnmounted(() => {
      if (checkInterval) {
        clearInterval(checkInterval)
      }
    })

    return {
      showNotification,
      showNotificationModal,
      currentNotification,
      formatDate,
      showNotificationDetail,
      closeNotification,
      closeNotificationModal,
      // 主题设置
      currentTheme,
      showThemeModal,
      themeOptions,
      selectedTheme,
      openThemeModal,
      closeThemeModal,
      applyTheme
    }
  }
}
</script>

<style scoped>
.setting-container {
  padding: 20px;
  min-height: 70vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
}

.setting-container h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 32px;
  font-weight: 600;
  color: #2c3e50;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin-top: 60px; /* 为顶部通知栏留出空间 */
}

/* 顶部通知栏 */
.top-notification {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 204, 0, 0.8); /* 透明黄色背景 */
  color: white;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  animation: slideDown 0.3s ease;
  height: 40px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.top-notification:hover {
  background: rgba(255, 204, 0, 0.9);
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
  }
  to {
    transform: translateY(0);
  }
}

.notification-content {
  flex: 1;
  overflow: hidden;
  position: relative;
  height: 20px;
  display: flex;
  align-items: center;
}

.notification-icon {
  font-size: 14px;
  margin-right: 10px;
  flex-shrink: 0;
}

.scrolling-text {
  position: absolute;
  white-space: nowrap;
  animation: scroll 20s linear infinite;
  font-size: 14px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

@keyframes scroll {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}

.notification-close {
  background: none;
  border: none;
  color: #ffcc00;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
  margin-left: 15px;
}

.notification-close:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

/* 通知详情弹窗 */
.notification-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.modal-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: #95a5a6;
}

.modal-close:hover {
  background: #f8f9fa;
  color: #2c3e50;
  transform: rotate(90deg);
}

.modal-body {
  padding: 30px 20px;
  text-align: center;
}

.notification-detail-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.notification-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.notification-date {
  font-size: 14px;
  color: #95a5a6;
  margin: 0 0 20px 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.notification-content-detail {
  text-align: left;
  line-height: 1.6;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.notification-content-detail p {
  margin: 10px 0;
  color: #34495e;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  text-align: center;
}

.modal-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 30px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.modal-btn:hover {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 功能列表样式 */
.feature-section {
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #95a5a6;
  margin-bottom: 10px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding-left: 10px;
}

.feature-item {
  display: flex;
  align-items: center;
  padding: 12px 10px;
  background: white;
  border-radius: 8px;
  margin-bottom: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-item:hover {
  background: #f8f9fa;
  transform: translateX(4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 18px;
  margin-right: 12px;
  width: 24px;
  text-align: center;
}

.feature-name {
  flex: 1;
  font-size: 14px;
  color: #2c3e50;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.feature-arrow {
  font-size: 18px;
  color: #bdc3c7;
  font-weight: 300;
}

/* 主题设置弹窗 */
.theme-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease;
}

.theme-options {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

.theme-option {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.theme-option:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.theme-preview {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  margin-right: 15px;
  border: 2px solid #e0e0e0;
}

.light-theme-preview {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.dark-theme-preview {
  background: linear-gradient(135deg, #2c3e50 0%, #1a252f 100%);
}

.theme-info {
  flex: 1;
}

.theme-info h4 {
  margin: 0 0 5px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.theme-info p {
  margin: 0;
  font-size: 14px;
  color: #7f8c8d;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.theme-radio {
  width: 20px;
  height: 20px;
  border: 2px solid #bdc3c7;
  border-radius: 50%;
  position: relative;
  transition: all 0.3s ease;
}

.theme-radio.active {
  border-color: #3498db;
}

.theme-radio.active::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 12px;
  height: 12px;
  background: #3498db;
  border-radius: 50%;
}

.cancel-btn {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #bdc3c7;
  border-radius: 6px;
  background: white;
  color: #2c3e50;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin-right: 10px;
}

.cancel-btn:hover {
  background: #f8f9fa;
  border-color: #95a5a6;
}

.confirm-btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  background: #3498db;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.confirm-btn:hover {
  background: #2980b9;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 深色主题 */
.dark-theme {
  --background-color: #1a1a1a;
  --text-color: #e0e0e0;
  --card-background: #2c2c2c;
  --border-color: #444;
  --hover-color: #3a3a3a;
}

.dark-theme .setting-container {
  background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
}

.dark-theme .setting-container h2 {
  color: #e0e0e0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.dark-theme .feature-section {
  background: rgba(44, 44, 44, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.dark-theme .section-title {
  color: #95a5a6;
}

.dark-theme .feature-item {
  background: #3a3a3a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.dark-theme .feature-item:hover {
  background: #444;
}

.dark-theme .feature-name {
  color: #e0e0e0;
}

.dark-theme .feature-arrow {
  color: #666;
}

.dark-theme .top-notification {
  background: rgba(255, 204, 0, 0.6);
}

.dark-theme .top-notification:hover {
  background: rgba(255, 204, 0, 0.8);
}

.dark-theme .modal-content {
  background: #2c2c2c;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.dark-theme .modal-header h3 {
  color: #e0e0e0;
}

.dark-theme .modal-close {
  color: #95a5a6;
}

.dark-theme .modal-close:hover {
  background: #3a3a3a;
  color: #e0e0e0;
}

.dark-theme .notification-title {
  color: #e0e0e0;
}

.dark-theme .notification-content-detail p {
  color: #ccc;
}

.dark-theme .modal-btn {
  background: #4a6fa5;
}

.dark-theme .modal-btn:hover {
  background: #3a5a8a;
}

.dark-theme .theme-option {
  background: #3a3a3a;
}

.dark-theme .theme-option:hover {
  background: #444;
}

.dark-theme .theme-info h4 {
  color: #e0e0e0;
}

.dark-theme .theme-info p {
  color: #95a5a6;
}

.dark-theme .cancel-btn {
  background: #3a3a3a;
  border-color: #555;
  color: #e0e0e0;
}

.dark-theme .cancel-btn:hover {
  background: #444;
  border-color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .setting-container h2 {
    font-size: 24px;
  }

  .feature-item {
    padding: 10px;
  }

  .feature-icon {
    font-size: 16px;
  }

  .feature-name {
    font-size: 13px;
  }

  .scrolling-text {
    font-size: 12px;
  }

  .modal-content {
    width: 95%;
    margin: 20px;
  }

  .modal-body {
    padding: 20px 15px;
  }

  .theme-preview {
    width: 50px;
    height: 50px;
  }

  .theme-info h4 {
    font-size: 14px;
  }

  .theme-info p {
    font-size: 12px;
  }
}
</style>

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

    <!-- 字体设置弹窗 -->
    <div class="font-modal" v-if="showFontModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>字体设置</h3>
          <button class="modal-close" @click="closeFontModal">×</button>
        </div>
        <div class="modal-body">
          <div class="font-options">
            <div v-for="option in fontOptions" :key="option.value" class="font-option" @click="selectedFont = option.value" :style="{ fontFamily: option.fontFamily }">
              <div class="font-info">
                <h4>{{ option.label }}</h4>
                <p class="font-preview">这是字体预览效果，测试中文字体</p>
              </div>
              <div class="font-radio" :class="{ active: selectedFont === option.value }"></div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeFontModal">取消</button>
          <button class="confirm-btn" @click="applyFont">确定</button>
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
      <div class="feature-item" @click="openFontModal">
          <span class="feature-icon">📝</span>
          <span class="feature-name">字体设置</span>
          <span class="feature-arrow">›</span>
        </div>
        <div class="feature-item" @click="openFontSizeModal">
          <span class="feature-icon">🔍</span>
          <span class="feature-name">字体大小</span>
          <span class="feature-arrow">›</span>
        </div>
        <div class="feature-item" @click="goToFeedback">
        <span class="feature-icon">📢</span>
        <span class="feature-name">意见反馈</span>
        <span class="feature-arrow">›</span>
      </div>
      <div class="feature-item" @click="showLanguageSetting">
        <span class="feature-icon">🌐</span>
        <span class="feature-name">语言设置</span>
        <span class="feature-arrow">›</span>
      </div>
      <div class="feature-item" @click="checkVersionUpdate">
        <span class="feature-icon">📱</span>
        <span class="feature-name">版本更新</span>
        <span class="feature-arrow">›</span>
      </div>

      <!-- 字体大小设置弹窗 -->
      <div v-if="showFontSizeModal" class="font-size-modal" @click="closeFontSizeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>字体大小设置</h3>
            <button class="modal-close" @click="closeFontSizeModal">×</button>
          </div>
          <div class="modal-body">
            <div class="font-size-preview">
              <p :style="{ fontSize: currentFontSize + 'px' }">字体大小预览：这是一段测试文字，用于预览字体大小效果。</p>
            </div>
            <div class="font-size-control">
              <van-slider
                v-model="currentFontSize"
                :min="fontSizeRange.min"
                :max="fontSizeRange.max"
                :step="1"
                :bar-height="10"
                active-color="#3498db"
                show-input
                input-size="small"
              />
              <div class="font-size-range">
                <span>{{ fontSizeRange.min }}px</span>
                <span>{{ fontSizeRange.max }}px</span>
              </div>
            </div>
            <div class="font-size-info">
              <p>当前字体大小：{{ currentFontSize }}px</p>
            </div>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="resetFontSize">重置</button>
            <button class="confirm-btn" @click="applyFontSize">确定</button>
          </div>
        </div>
      </div>

      <!-- 版本更新弹窗 -->
      <div class="version-modal" v-if="showVersionModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>版本信息</h3>
            <button class="modal-close" @click="closeVersionModal">×</button>
          </div>
          <div class="modal-body">
            <div class="version-info">
              <p class="current-version">当前版本：v{{ currentVersion }}</p>
              <p v-if="hasUpdate" class="new-version">最新版本：v{{ latestVersion }}</p>
              <div v-if="hasUpdate" class="update-info">
                <h4>更新内容：</h4>
                <ul>
                  <li v-for="(item, index) in updateContent" :key="index">{{ item }}</li>
                </ul>
              </div>
              <p v-else class="no-update">当前已是最新版本</p>
            </div>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="closeVersionModal">关闭</button>
            <button v-if="hasUpdate" class="confirm-btn" @click="showUpdateConfirmModal = true">更新</button>
          </div>
        </div>
      </div>

      <!-- 更新确认弹窗 -->
      <div class="update-confirm-modal" v-if="showUpdateConfirmModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>确认更新</h3>
            <button class="modal-close" @click="showUpdateConfirmModal = false">×</button>
          </div>
          <div class="modal-body">
            <p class="update-time">更新预计需要 {{ updateTime }} 分钟</p>
            <p class="update-note">更新期间暂时无法使用该应用</p>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="showUpdateConfirmModal = false">取消</button>
            <button class="confirm-btn" @click="startUpdate">确认</button>
          </div>
        </div>
      </div>

      <!-- 更新进度弹窗 -->
      <div class="update-progress-modal" v-if="showUpdateProgressModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>正在更新</h3>
            <button class="modal-close" @click="cancelUpdate" :disabled="true">×</button>
          </div>
          <div class="modal-body">
            <div class="progress-container">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: updateProgress + '%' }">
                  <div class="progress-icon">🚀</div>
                </div>
              </div>
              <div class="progress-text">{{ updateProgress }}%</div>
            </div>
            <p class="update-status">{{ updateStatus }}</p>
          </div>
        </div>
      </div>

      <!-- 更新成功弹窗 -->
      <div class="update-success-modal" v-if="showUpdateSuccessModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>更新成功</h3>
            <button class="modal-close" @click="closeUpdateSuccessModal">×</button>
          </div>
          <div class="modal-body">
            <div class="success-icon">🎉</div>
            <p class="success-message">更新成功，欢迎使用 v{{ latestVersion }} 版本</p>
          </div>
          <div class="modal-footer">
            <button class="confirm-btn" @click="closeUpdateSuccessModal">立即体验</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { showLoadingToast, showSuccessToast, showToast } from 'vant'
// 注意：实际项目中需要安装axios并导入
// import axios from 'axios'

export default {
  name: 'homeSetting',
  setup () {
    const router = useRouter()

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

    // 字体设置
    const currentFont = ref(localStorage.getItem('font') || 'default')
    const showFontModal = ref(false)
    const fontOptions = [
      { value: 'default', label: '默认字体', fontFamily: 'Arial, sans-serif' },
      { value: 'simsun', label: '宋体', fontFamily: 'SimSun, serif' },
      { value: 'kaiti', label: '楷书', fontFamily: 'KaiTi, serif' },
      { value: 'simhei', label: '黑体', fontFamily: 'SimHei, sans-serif' },
      { value: 'fangsong', label: '仿宋', fontFamily: 'FangSong, serif' },
      { value: 'microsoftyahei', label: '微软雅黑', fontFamily: 'Microsoft YaHei, sans-serif' }
    ]
    const selectedFont = ref(currentFont.value)

    // 字体大小设置
    const currentFontSize = ref(parseInt(localStorage.getItem('fontSize') || '16'))
    const showFontSizeModal = ref(false)
    const fontSizeRange = {
      min: 12,
      max: 24
    }

    // 版本更新相关
    const currentVersion = ref('1.0.0')
    const latestVersion = ref('2.0.0')
    const hasUpdate = ref(true)
    const updateContent = ref([
      '新增多种倒计时模板',
      '优化用户界面',
      '提升系统性能',
      '修复已知bug'
    ])
    const showVersionModal = ref(false)
    const showUpdateConfirmModal = ref(false)
    const showUpdateProgressModal = ref(false)
    const showUpdateSuccessModal = ref(false)
    const updateTime = ref(2)
    const updateProgress = ref(0)
    const updateStatus = ref('正在准备更新...')
    let updateInterval = null

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

    // 语言设置方法
    const showLanguageSetting = function () {
      showToast('语言设置功能待开发')
    }

    // 字体设置方法
    const openFontModal = function () {
      selectedFont.value = currentFont.value
      showFontModal.value = true
    }

    const closeFontModal = function () {
      showFontModal.value = false
    }

    const applyFont = function () {
      showLoadingToast('正在切换字体...')

      // 模拟网络请求延迟
      setTimeout(() => {
        currentFont.value = selectedFont.value
        localStorage.setItem('font', selectedFont.value)

        // 应用字体到文档
        const fontOption = fontOptions.find(option => option.value === selectedFont.value)
        if (fontOption) {
          // 同时设置多个根元素的字体，确保所有元素都能继承
          document.documentElement.style.fontFamily = fontOption.fontFamily
          document.body.style.fontFamily = fontOption.fontFamily

          // 创建或更新全局样式规则，确保所有元素都使用新字体，但不影响图标
          let styleElement = document.getElementById('font-style')
          if (!styleElement) {
            styleElement = document.createElement('style')
            styleElement.id = 'font-style'
            document.head.appendChild(styleElement)
          }
          styleElement.textContent = `*:not(.van-icon) { font-family: ${fontOption.fontFamily} !important; }`

          console.log('字体已切换为:', fontOption.fontFamily)
        }

        showSuccessToast('字体切换成功')
        showFontModal.value = false
      }, 1000)
    }

    // 字体大小设置方法
    const openFontSizeModal = function () {
      showFontSizeModal.value = true
    }

    const closeFontSizeModal = function () {
      showFontSizeModal.value = false
    }

    const applyFontSize = function () {
      showLoadingToast('正在调整字体大小...')

      // 模拟网络请求延迟
      setTimeout(() => {
        localStorage.setItem('fontSize', currentFontSize.value)

        // 应用字体大小到文档
        document.documentElement.style.fontSize = currentFontSize.value + 'px'

        // 创建或更新全局样式规则，确保所有元素都使用新字体大小，但不影响图标
        let fontSizeStyleElement = document.getElementById('font-size-style')
        if (!fontSizeStyleElement) {
          fontSizeStyleElement = document.createElement('style')
          fontSizeStyleElement.id = 'font-size-style'
          document.head.appendChild(fontSizeStyleElement)
        }
        fontSizeStyleElement.textContent = `*:not(.van-icon) { font-size: ${currentFontSize.value}px !important; }`

        showSuccessToast('字体大小调整成功')
        showFontSizeModal.value = false
      }, 1000)
    }

    const resetFontSize = function () {
      currentFontSize.value = 16
      localStorage.setItem('fontSize', '16')

      // 应用默认字体大小到文档
      document.documentElement.style.fontSize = '16px'

      // 更新全局样式规则
      const fontSizeStyleElement = document.getElementById('font-size-style')
      if (fontSizeStyleElement) {
        fontSizeStyleElement.textContent = '*:not(.van-icon) { font-size: 16px !important; }'
      }

      showSuccessToast('字体大小已重置为默认值')
    }

    // 跳转到反馈页面
    const goToFeedback = function () {
      router.push('/feedback')
    }

    // 版本更新相关函数
    const checkVersionUpdate = function () {
      // 模拟检查版本更新
      showVersionModal.value = true
    }

    const closeVersionModal = function () {
      showVersionModal.value = false
    }

    const startUpdate = function () {
      showUpdateConfirmModal.value = false
      showUpdateProgressModal.value = true
      updateProgress.value = 0
      updateStatus.value = '正在准备更新...'

      // 模拟更新进度
      updateInterval = setInterval(() => {
        updateProgress.value += 5

        if (updateProgress.value < 20) {
          updateStatus.value = '正在下载更新包...'
        } else if (updateProgress.value < 60) {
          updateStatus.value = '正在解压更新包...'
        } else if (updateProgress.value < 90) {
          updateStatus.value = '正在安装更新...'
        } else {
          updateStatus.value = '正在完成更新...'
        }

        if (updateProgress.value >= 100) {
          clearInterval(updateInterval)
          showUpdateProgressModal.value = false
          showUpdateSuccessModal.value = true
        }
      }, 300)
    }

    const cancelUpdate = function () {
      if (updateInterval) {
        clearInterval(updateInterval)
      }
      showUpdateProgressModal.value = false
    }

    const closeUpdateSuccessModal = function () {
      showUpdateSuccessModal.value = false
      // 模拟更新后的操作，例如刷新页面或跳转到首页
      currentVersion.value = latestVersion.value
      hasUpdate.value = false
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

      // 初始化字体
      const fontOption = fontOptions.find(option => option.value === currentFont.value)
      if (fontOption) {
        document.documentElement.style.fontFamily = fontOption.fontFamily
        document.body.style.fontFamily = fontOption.fontFamily

        // 创建或更新全局样式规则，确保所有元素都使用新字体，但不影响图标
        let styleElement = document.getElementById('font-style')
        if (!styleElement) {
          styleElement = document.createElement('style')
          styleElement.id = 'font-style'
          document.head.appendChild(styleElement)
        }
        styleElement.textContent = `*:not(.van-icon) { font-family: ${fontOption.fontFamily} !important; }`

        console.log('初始化字体为:', fontOption.fontFamily)
      }

      // 初始化字体大小
      document.documentElement.style.fontSize = currentFontSize.value + 'px'

      // 创建或更新全局样式规则，确保所有元素都使用新字体大小，但不影响图标
      let fontSizeStyleElement = document.getElementById('font-size-style')
      if (!fontSizeStyleElement) {
        fontSizeStyleElement = document.createElement('style')
        fontSizeStyleElement.id = 'font-size-style'
        document.head.appendChild(fontSizeStyleElement)
      }
      fontSizeStyleElement.textContent = `*:not(.van-icon) { font-size: ${currentFontSize.value}px !important; }`

      console.log('初始化字体大小为:', currentFontSize.value, 'px')
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
      applyTheme,
      // 语言设置
      showLanguageSetting,
      // 字体设置
      currentFont,
      showFontModal,
      fontOptions,
      selectedFont,
      openFontModal,
      closeFontModal,
      applyFont,
      // 字体大小设置
      currentFontSize,
      showFontSizeModal,
      fontSizeRange,
      openFontSizeModal,
      closeFontSizeModal,
      applyFontSize,
      resetFontSize,
      // 反馈功能
      goToFeedback,
      // 版本更新相关
      currentVersion,
      latestVersion,
      hasUpdate,
      updateContent,
      showVersionModal,
      showUpdateConfirmModal,
      showUpdateProgressModal,
      showUpdateSuccessModal,
      updateTime,
      updateProgress,
      updateStatus,
      checkVersionUpdate,
      closeVersionModal,
      startUpdate,
      cancelUpdate,
      closeUpdateSuccessModal
    }
  }
}
</script>
<style scoped>
@import '../../styles/setting.css';
</style>

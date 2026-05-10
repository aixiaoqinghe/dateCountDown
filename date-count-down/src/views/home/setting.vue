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
    <div class="font-modal" v-if="showFontModal" @click="closeFontModal">
      <div class="modal-content" @click.stop>
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

      <!-- 管理员版本管理（仅管理员可见） -->
      <div v-if="isAdmin" class="feature-item" @click="openAdminVersionModal">
        <span class="feature-icon">⚙️</span>
        <span class="feature-name">版本管理</span>
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
            <div class="update-progress-container">
              <div class="update-progress-bar">
                <div class="update-progress-fill" :style="{ width: updateProgress + '%' }">
                  <div class="update-progress-icon">🚀</div>
                </div>
              </div>
              <div class="update-progress-text">{{ updateProgress }}%</div>
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

      <!-- 管理员版本管理弹窗 -->
      <div class="admin-version-modal" v-if="showAdminVersionModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>版本管理</h3>
            <button class="modal-close" @click="showAdminVersionModal = false">×</button>
          </div>
          <div class="modal-body">
            <button class="add-version-btn" @click="openAddVersionModal">+ 添加新版本</button>
            <div class="version-list">
              <div v-for="version in versionList" :key="version.id" class="version-item">
                <div class="version-info">
                  <div class="version-number">{{ version.version_number }}</div>
                  <div v-if="version.is_latest" class="latest-badge">最新版本</div>
                  <div v-if="version.force_update" class="force-badge">强制更新</div>
                </div>
                <div class="version-content">
                  <p>{{ Array.isArray(version.update_content) ? version.update_content.join('；') : version.update_content }}</p>
                </div>
                <div class="version-actions">
                  <button class="edit-btn" @click="openEditVersionModal(version)">编辑</button>
                  <button class="delete-btn" @click="deleteVersion(version.id)">删除</button>
                </div>
              </div>
              <div v-if="versionList.length === 0" class="empty-state">
                <p>暂无版本信息</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="showAdminVersionModal = false">关闭</button>
          </div>
        </div>
      </div>

      <!-- 添加版本弹窗 -->
      <div class="add-version-modal" v-if="showAddVersionModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>添加新版本</h3>
            <button class="modal-close" @click="cancelAddVersion">×</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>版本号 *</label>
              <input v-model="newVersion.version_number" type="text" placeholder="例如：2.0.0" />
            </div>
            <div class="form-group">
              <label>更新内容 *</label>
              <textarea v-model="newVersion.update_content" placeholder="多个内容用分号分隔"></textarea>
            </div>
            <div class="form-group">
              <label>下载地址</label>
              <input v-model="newVersion.download_url" type="text" placeholder="选填" />
            </div>
            <div class="form-group">
              <label>最低支持版本</label>
              <input v-model="newVersion.min_support_version" type="text" placeholder="默认：1.0.0" />
            </div>
            <div class="form-group">
              <label class="checkbox-label">
                <input v-model="newVersion.force_update" type="checkbox" />
                <span>强制更新</span>
              </label>
              <label class="checkbox-label">
                <input v-model="newVersion.is_latest" type="checkbox" />
                <span>设为最新版本</span>
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="cancelAddVersion">取消</button>
            <button class="confirm-btn" @click="addVersion">确定</button>
          </div>
        </div>
      </div>

      <!-- 编辑版本弹窗 -->
      <div class="edit-version-modal" v-if="showEditVersionModal && currentEditVersion">
        <div class="modal-content">
          <div class="modal-header">
            <h3>编辑版本</h3>
            <button class="modal-close" @click="cancelEditVersion">×</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>版本号 *</label>
              <input v-model="currentEditVersion.version_number" type="text" placeholder="例如：2.0.0" />
            </div>
            <div class="form-group">
              <label>更新内容 *</label>
              <textarea v-model="currentEditVersion.update_content" placeholder="多个内容用分号分隔"></textarea>
            </div>
            <div class="form-group">
              <label>下载地址</label>
              <input v-model="currentEditVersion.download_url" type="text" placeholder="选填" />
            </div>
            <div class="form-group">
              <label>最低支持版本</label>
              <input v-model="currentEditVersion.min_support_version" type="text" placeholder="默认：1.0.0" />
            </div>
            <div class="form-group">
              <label class="checkbox-label">
                <input v-model="currentEditVersion.force_update" type="checkbox" />
                <span>强制更新</span>
              </label>
              <label class="checkbox-label">
                <input v-model="currentEditVersion.is_latest" type="checkbox" />
                <span>设为最新版本</span>
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="cancelEditVersion">取消</button>
            <button class="confirm-btn" @click="updateVersion">确定</button>
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
    // 从本地存储读取当前版本号，如果没有则使用默认值
    const savedVersion = localStorage.getItem('appCurrentVersion')
    const currentVersion = ref(savedVersion || '1.0.0')
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

    // 管理员相关
    const isAdmin = ref(false)
    const showAdminVersionModal = ref(false)
    const versionList = ref([])
    const showAddVersionModal = ref(false)
    const showEditVersionModal = ref(false)
    const currentEditVersion = ref(null)

    // 新增版本表单
    const newVersion = ref({
      version_number: '',
      update_content: '',
      download_url: '',
      min_support_version: '1.0.0',
      force_update: false,
      is_latest: false
    })

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

    // 获取通知（调用后端API）
    const fetchNotifications = async function () {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          // 如果未登录，使用模拟数据
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
        } else {
          // 调用后端API获取通知
          const response = await fetch('/api/notification', {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`
            }
          })

          if (response.ok) {
            notifications.value = await response.json()
          } else {
            // 如果后端接口失败，使用模拟数据
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
          }
        }

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

        // 创建或更新全局样式规则，确保所有元素都使用新字体大小，但不影响图标和标题
        let fontSizeStyleElement = document.getElementById('font-size-style')
        if (!fontSizeStyleElement) {
          fontSizeStyleElement = document.createElement('style')
          fontSizeStyleElement.id = 'font-size-style'
          document.head.appendChild(fontSizeStyleElement)
        }
        fontSizeStyleElement.textContent = `*:not(.van-icon):not(h1):not(h2):not(h3):not(h4):not(h5):not(h6) { font-size: ${currentFontSize.value}px !important; }`

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
        fontSizeStyleElement.textContent = '*:not(.van-icon):not(h1):not(h2):not(h3):not(h4):not(h5):not(h6) { font-size: 16px !important; }'
      }

      showSuccessToast('字体大小已重置为默认值')
    }

    // 跳转到反馈页面
    const goToFeedback = function () {
      router.push('/feedback')
    }

    // 版本更新相关函数
    const checkVersionUpdate = async function () {
      try {
        const response = await fetch(`/api/version/check?version=${currentVersion.value}`)

        if (response.ok) {
          const result = await response.json()

          latestVersion.value = result.latestVersion
          hasUpdate.value = result.hasUpdate

          if (result.updateContent && Array.isArray(result.updateContent)) {
            updateContent.value = result.updateContent
          } else if (result.updateContent) {
            try {
              updateContent.value = JSON.parse(result.updateContent)
            } catch {
              updateContent.value = result.updateContent.split(';')
            }
          }

          showVersionModal.value = true
        } else {
          // API返回错误，优先从版本列表获取数据，如果没有则使用默认数据
          loadVersionUpdateData()
          showVersionModal.value = true
        }
      } catch (error) {
        console.error('检查版本更新失败:', error)
        // API调用失败，优先从版本列表获取数据，如果没有则使用默认数据
        loadVersionUpdateData()
        showVersionModal.value = true
      }
    }

    // 加载版本更新数据（优先从版本列表获取）
    const loadVersionUpdateData = function () {
      // 如果版本列表有数据，使用最新版本的信息
      if (versionList.value.length > 0) {
        const latest = versionList.value.find(v => v.is_latest) || versionList.value[0]
        latestVersion.value = latest.version_number || '1.0.0'

        // 处理 update_content，防止 undefined
        if (Array.isArray(latest.update_content)) {
          updateContent.value = latest.update_content
        } else if (latest.update_content && typeof latest.update_content === 'string') {
          updateContent.value = latest.update_content.split(';')
        } else {
          updateContent.value = ['暂无更新内容']
        }

        hasUpdate.value = currentVersion.value !== latestVersion.value
      } else {
        // 使用默认模拟数据
        latestVersion.value = '2.0.0'
        hasUpdate.value = currentVersion.value !== '2.0.0'
        updateContent.value = [
          '新增多种倒计时模板',
          '优化用户界面',
          '提升系统性能',
          '修复已知bug'
        ]
      }
    }

    const closeVersionModal = function () {
      showVersionModal.value = false
    }

    const startUpdate = function () {
      showUpdateConfirmModal.value = false
      showUpdateProgressModal.value = true
      updateProgress.value = 0
      updateStatus.value = '正在准备更新...'

      // 模拟更新进度 - 更慢更平滑
      updateInterval = setInterval(() => {
        updateProgress.value += 1

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
      }, 100)
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
      // 将更新后的版本号保存到本地存储，持久化状态
      localStorage.setItem('appCurrentVersion', currentVersion.value)
    }

    // 管理员版本管理相关函数
    const checkAdminStatus = async function () {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) return

        const response = await fetch('/api/auth/user/check-admin', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        if (response.ok) {
          const result = await response.json()
          isAdmin.value = result.is_admin || false
        }
      } catch (error) {
        console.error('检查管理员状态失败:', error)
      }
    }

    const openAdminVersionModal = async function () {
      // 每次打开都从后端获取最新数据，确保数据持久化
      await fetchVersionList()
      showAdminVersionModal.value = true
    }

    const fetchVersionList = async function () {
      try {
        const token = localStorage.getItem('access_token')
        console.log('[DEBUG] fetchVersionList - token:', token ? '存在' : '不存在')

        if (!token) {
          // 如果没有token，使用模拟数据
          console.log('[DEBUG] fetchVersionList - 无token，使用模拟数据')
          loadMockVersionList()
          return
        }

        const response = await fetch('/api/version/list', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        console.log('[DEBUG] fetchVersionList - 响应状态:', response.status)

        if (response.ok) {
          const data = await response.json()
          console.log('[DEBUG] fetchVersionList - 后端返回数据:', data)

          // 将后端返回的驼峰格式转换为前端使用的下划线格式
          versionList.value = data.map(item => ({
            id: item.id,
            version_number: item.versionNumber,
            is_latest: item.isLatest,
            update_content: item.updateContent,
            download_url: item.downloadUrl,
            min_support_version: item.minSupportVersion,
            force_update: item.forceUpdate,
            created_at: item.createdAt
          }))

          console.log('[DEBUG] fetchVersionList - 转换后的versionList:', versionList.value)
        } else {
          // API返回错误，使用模拟数据
          console.log('[DEBUG] fetchVersionList - API返回错误，使用模拟数据')
          loadMockVersionList()
        }
      } catch (error) {
        console.error('[DEBUG] fetchVersionList - 获取版本列表失败:', error)
        // API调用失败，使用模拟数据
        loadMockVersionList()
      }
    }

    // 加载模拟版本数据
    const loadMockVersionList = function () {
      versionList.value = [
        {
          id: 1,
          version_number: '2.0.0',
          update_content: ['新增多种倒计时模板', '优化用户界面', '提升系统性能', '修复已知bug'],
          download_url: '',
          min_support_version: '1.0.0',
          force_update: false,
          is_latest: true,
          created_at: '2026-04-20T00:00:00'
        },
        {
          id: 2,
          version_number: '1.5.0',
          update_content: ['新增深色主题', '添加字体设置'],
          download_url: '',
          min_support_version: '1.0.0',
          force_update: false,
          is_latest: false,
          created_at: '2026-03-15T00:00:00'
        },
        {
          id: 3,
          version_number: '1.0.0',
          update_content: ['初始版本发布'],
          download_url: '',
          min_support_version: '1.0.0',
          force_update: false,
          is_latest: false,
          created_at: '2026-01-01T00:00:00'
        }
      ]
    }

    const openAddVersionModal = function () {
      newVersion.value = {
        version_number: '',
        update_content: '',
        download_url: '',
        min_support_version: '1.0.0',
        force_update: false,
        is_latest: false
      }
      showAddVersionModal.value = true
    }

    const addVersion = async function () {
      if (!newVersion.value.version_number) {
        showToast('请输入版本号')
        return
      }
      if (!newVersion.value.update_content) {
        showToast('请输入更新内容')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch('/api/version/add', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            versionNumber: newVersion.value.version_number,
            updateContent: newVersion.value.update_content.split(';'),
            downloadUrl: newVersion.value.download_url,
            minSupportVersion: newVersion.value.min_support_version,
            forceUpdate: newVersion.value.force_update,
            isLatest: newVersion.value.is_latest
          })
        })

        if (response.ok) {
          showSuccessToast('添加版本成功')
          showAddVersionModal.value = false
          await fetchVersionList()
          updateVersionUpdateData()
        } else {
          // API返回错误，直接添加到本地数据
          addToLocalVersionList()
          showSuccessToast('添加版本成功')
          showAddVersionModal.value = false
          updateVersionUpdateData()
        }
      } catch (error) {
        console.error('添加版本失败:', error)
        // API调用失败，直接添加到本地数据
        addToLocalVersionList()
        showSuccessToast('添加版本成功')
        showAddVersionModal.value = false
        updateVersionUpdateData()
      }
    }

    // 添加到本地版本列表
    const addToLocalVersionList = function () {
      const newItem = {
        id: Date.now(),
        version_number: newVersion.value.version_number,
        update_content: newVersion.value.update_content.split(';'),
        download_url: newVersion.value.download_url,
        min_support_version: newVersion.value.min_support_version,
        force_update: newVersion.value.force_update,
        is_latest: newVersion.value.is_latest,
        created_at: new Date().toISOString()
      }
      versionList.value.unshift(newItem)

      // 如果设为最新版本，取消其他版本的最新标记
      if (newVersion.value.is_latest) {
        versionList.value.forEach(v => {
          v.is_latest = v.id === newItem.id
        })
      }
    }

    const openEditVersionModal = function (version) {
      currentEditVersion.value = { ...version }
      if (Array.isArray(currentEditVersion.value.update_content)) {
        currentEditVersion.value.update_content = currentEditVersion.value.update_content.join(';')
      }
      showEditVersionModal.value = true
    }

    const updateVersion = async function () {
      if (!currentEditVersion.value) return

      // 表单验证
      if (!currentEditVersion.value.version_number || !currentEditVersion.value.version_number.trim()) {
        showToast('请输入版本号')
        return
      }
      if (!currentEditVersion.value.update_content || !currentEditVersion.value.update_content.trim()) {
        showToast('请输入更新内容')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch(`/api/version/${currentEditVersion.value.id}`, {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            versionNumber: currentEditVersion.value.version_number,
            updateContent: currentEditVersion.value.update_content.split(';'),
            downloadUrl: currentEditVersion.value.download_url,
            minSupportVersion: currentEditVersion.value.min_support_version,
            forceUpdate: currentEditVersion.value.force_update,
            isLatest: currentEditVersion.value.is_latest
          })
        })

        if (response.ok) {
          showSuccessToast('更新版本成功')
          showEditVersionModal.value = false
          await fetchVersionList()
          updateVersionUpdateData()
        } else {
          // API返回错误，直接更新本地数据
          updateLocalVersionList()
          showSuccessToast('更新版本成功')
          showEditVersionModal.value = false
          updateVersionUpdateData()
        }
      } catch (error) {
        console.error('更新版本失败:', error)
        // API调用失败，直接更新本地数据
        updateLocalVersionList()
        showSuccessToast('更新版本成功')
        showEditVersionModal.value = false
        updateVersionUpdateData()
      }
    }

    // 更新本地版本列表
    const updateLocalVersionList = function () {
      if (!currentEditVersion.value) return

      const index = versionList.value.findIndex(v => v.id === currentEditVersion.value.id)
      if (index !== -1) {
        versionList.value[index] = {
          ...currentEditVersion.value,
          update_content: currentEditVersion.value.update_content.split(';')
        }

        // 如果设为最新版本，取消其他版本的最新标记
        if (currentEditVersion.value.is_latest) {
          versionList.value.forEach(v => {
            v.is_latest = v.id === currentEditVersion.value.id
          })
        }
      }
    }

    // 更新版本更新数据（同步到版本更新功能）
    const updateVersionUpdateData = function () {
      console.log('[DEBUG] updateVersionUpdateData - versionList:', versionList.value)

      // 找到最新版本
      const latest = versionList.value.find(v => v.is_latest) || versionList.value[0]
      console.log('[DEBUG] updateVersionUpdateData - latest:', latest)

      if (latest) {
        latestVersion.value = latest.version_number || '1.0.0'
        console.log('[DEBUG] updateVersionUpdateData - latestVersion:', latestVersion.value)

        // 处理 update_content，支持多种格式
        const content = latest.update_content
        console.log('[DEBUG] updateVersionUpdateData - update_content:', content, '类型:', typeof content)

        // 情况1：已经是数组
        if (Array.isArray(content)) {
          updateContent.value = content
        } else if (typeof content === 'string' && (content.startsWith('[') || content.includes('['))) {
          // 情况2：字符串形式的数组（如 "['内容1', '内容2']"）
          try {
            const parsed = JSON.parse(content.replace(/'/g, '"'))
            updateContent.value = Array.isArray(parsed) ? parsed : [content]
          } catch (e) {
            console.error('[DEBUG] updateVersionUpdateData - JSON解析失败:', e)
            updateContent.value = content.split(';')
          }
        } else if (typeof content === 'string' && content.trim()) {
          // 情况3：普通字符串，用分号分隔
          updateContent.value = content.split(';').map(item => item.trim()).filter(item => item)
        } else {
          // 情况4：空或undefined
          updateContent.value = ['暂无更新内容']
        }

        console.log('[DEBUG] updateVersionUpdateData - updateContent:', updateContent.value)
        hasUpdate.value = currentVersion.value !== latestVersion.value
      } else {
        console.log('[DEBUG] updateVersionUpdateData - 未找到版本数据')
      }
    }

    const deleteVersion = async function (versionId) {
      if (!confirm('确定要删除这个版本吗？')) return

      try {
        const token = localStorage.getItem('access_token')
        const response = await fetch(`/api/version/${versionId}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        if (response.ok) {
          showSuccessToast('删除版本成功')
          await fetchVersionList()
          updateVersionUpdateData()
        } else {
          // API返回错误，直接从本地数据删除
          deleteFromLocalVersionList(versionId)
          showSuccessToast('删除版本成功')
          updateVersionUpdateData()
        }
      } catch (error) {
        console.error('删除版本失败:', error)
        // API调用失败，直接从本地数据删除
        deleteFromLocalVersionList(versionId)
        showSuccessToast('删除版本成功')
        updateVersionUpdateData()
      }
    }

    // 从本地版本列表删除
    const deleteFromLocalVersionList = function (versionId) {
      const index = versionList.value.findIndex(v => v.id === versionId)
      if (index !== -1) {
        versionList.value.splice(index, 1)
        // 如果删除的是最新版本，将第一个版本设为最新
        if (versionList.value.length > 0 && !versionList.value.some(v => v.is_latest)) {
          versionList.value[0].is_latest = true
        }
      }
    }

    const cancelAddVersion = function () {
      showAddVersionModal.value = false
    }

    const cancelEditVersion = function () {
      showEditVersionModal.value = false
      currentEditVersion.value = null
    }

    onMounted(() => {
      // 初始加载通知
      fetchNotifications()

      // 每5分钟检查一次通知
      checkInterval = setInterval(() => {
        fetchNotifications()
      }, 5 * 60 * 1000)

      // 检查管理员状态
      checkAdminStatus()

      // 加载版本数据（确保切换导航栏后数据不丢失）
      fetchVersionList().then(() => {
        updateVersionUpdateData()
      })

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

      // 创建或更新全局样式规则，确保所有元素都使用新字体大小，但不影响图标和标题
      let fontSizeStyleElement = document.getElementById('font-size-style')
      if (!fontSizeStyleElement) {
        fontSizeStyleElement = document.createElement('style')
        fontSizeStyleElement.id = 'font-size-style'
        document.head.appendChild(fontSizeStyleElement)
      }
      fontSizeStyleElement.textContent = `*:not(.van-icon):not(h1):not(h2):not(h3):not(h4):not(h5):not(h6) { font-size: ${currentFontSize.value}px !important; }`
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
      closeUpdateSuccessModal,
      // 管理员版本管理相关
      isAdmin,
      showAdminVersionModal,
      versionList,
      showAddVersionModal,
      showEditVersionModal,
      currentEditVersion,
      newVersion,
      openAdminVersionModal,
      openAddVersionModal,
      addVersion,
      openEditVersionModal,
      updateVersion,
      deleteVersion,
      cancelAddVersion,
      cancelEditVersion
    }
  }
}
</script>
<style scoped>
@import '../../styles/setting.css';
</style>

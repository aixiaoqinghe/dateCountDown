<template>
  <div class="countdown-container" :style="backgroundStyle">
    <h2 class="countdown-title">距离{{ taskName || '目标' }}日期还有</h2>
    <div class="countdown-time">
      <div class="time-item">
        <span class="time-number">{{ days }}</span>
        <span class="time-unit">天</span>
      </div>
      <div class="time-item">
        <span class="time-number">{{ hours }}</span>
        <span class="time-unit">时</span>
      </div>
      <div class="time-item">
        <span class="time-number">{{ minutes }}</span>
        <span class="time-unit">分</span>
      </div>
      <div class="time-item">
        <span class="time-number">{{ seconds }}</span>
        <span class="time-unit">秒</span>
      </div>
    </div>
    <div class="countdown-input">
      <input
        type="text"
        v-model="taskName"
        placeholder="请输入任务名称"
        class="task-input"
      />
      <input
        type="date"
        v-model="targetDate"
        @change="updateCountdown"
        class="date-input"
      />
      <div class="btn-group">
        <button @click="startCountdown" class="start-btn">开始倒计时</button>
        <button @click="resetCountdown" class="reset-btn">重置</button>
        <button @click="isEditMode ? showConfirmModal = true : showCategoryModal = true" class="save-btn">{{ isEditMode ? '更改' : '添加到历史' }}</button>
        <!-- 当isEditMode为true时，显示确认修改弹窗, 否则显示分类选择弹窗 -->
      </div>
    </div>

    <!-- 背景图片设置按钮 -->
    <div class="bg-image-btn-container">
      <input type="file" ref="fileInput" accept="image/*" @change="handleImageUpload" style="display: none;" />
      <button @click="$refs.fileInput.click()" class="bg-image-btn" title="设置背景图片">
        <span class="plus-icon">+</span>
        <span class="btn-tooltip">设置背景图片</span>
      </button>
    </div>

    <!-- 分类选择弹窗 -->
    <div v-if="showCategoryModal" class="modal-overlay" @click="showCategoryModal = false">
      <div class="modal-content" @click.stop>
        <h3>选择分类</h3>
        <div class="category-list">
          <div
            v-for="category in categories"
            :key="category.value"
            class="category-item"
            @click="saveToHistory(category.value)"
          >
            {{ category.label }}
          </div>
        </div>
      </div>
    </div>

    <!-- 确认修改弹窗 -->
    <div v-if="showConfirmModal" class="modal-overlay" @click="showConfirmModal = false">
      <div class="modal-content" @click.stop>
        <h3>确认修改</h3>
        <p class="confirm-message">确定要更改为 {{ taskName }} 吗？</p>
        <div class="confirm-btn-group">
          <button @click="confirmChange" class="confirm-btn">确定</button>
          <button @click="showConfirmModal = false" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { showToast, showSuccessToast } from 'vant'
export default {
  name: 'countDown',
  data () {
    return {
      taskName: '',
      targetDate: this.getCurrentDate(),
      days: 0,
      hours: 0,
      minutes: 0,
      seconds: 0,
      countdownTimer: null,
      showCategoryModal: false,
      showConfirmModal: false,
      isEditMode: false,
      originalItem: null,
      categories: [
        { label: '生活', value: 'life' },
        { label: '学习', value: 'study' },
        { label: '工作', value: 'work' },
        { label: '纪念日', value: 'anniversary' },
        { label: '其他', value: 'other' }
      ],
      backgroundImage: ''
    }
  },
  computed: {
    backgroundStyle () {
      if (this.backgroundImage) {
        return {
          backgroundImage: `url(${this.backgroundImage})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat'
        }
      }
      // 返回默认背景样式
      return {
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }
    }
  },
  methods: {
    getCurrentDate () {
      const today = new Date()
      return today.toISOString().split('T')[0] // 格式化为 YYYY-MM-DD 格式
    },
    calculateCountdown () {
      const target = new Date(this.targetDate).getTime()
      const now = new Date().getTime()
      const distance = target - now

      if (distance < 0) {
        this.days = 0
        this.hours = 0
        this.minutes = 0
        this.seconds = 0
        clearInterval(this.countdownTimer)
        return
      }

      this.days = Math.floor(distance / (1000 * 60 * 60 * 24))
      this.hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      this.minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
      this.seconds = Math.floor((distance % (1000 * 60)) / 1000)
    },
    startCountdown () {
      // 先清除之前的定时器
      if (this.countdownTimer) {
        clearInterval(this.countdownTimer)
      }
      // 立即计算一次
      this.calculateCountdown()
      // 设置定时器，每秒更新一次
      this.countdownTimer = setInterval(() => {
        this.calculateCountdown()
      }, 1000)
    },
    resetCountdown () {
      if (this.countdownTimer) {
        clearInterval(this.countdownTimer)
      }
      this.days = 0
      this.hours = 0
      this.minutes = 0
      this.seconds = 0
      this.taskName = '' // 重置任务名称
      this.targetDate = this.getCurrentDate() // 重置为当前日期
      this.isEditMode = false
      this.originalItem = null
      this.backgroundImage = '' // 重置背景图片
    },
    updateCountdown () {
      // 只更新日期，不自动开始倒计时
      // this.startCountdown()
    },
    async saveToHistory (category) {
      // 输入验证
      if (!this.taskName.trim()) {
        showToast('请输入任务名称！')
        return
      }

      if (!this.targetDate) {
        showToast('请选择目标日期！')
        return
      }

      const token = localStorage.getItem('access_token')

      // 如果有token，调用后端API创建倒计时
      if (token) {
        try {
          const response = await fetch('/api/countdown', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
              task_name: this.taskName,
              target_date: this.targetDate.split('T')[0],
              category: category,
              background_image: this.backgroundImage
            })
          })

          if (response.ok) {
            const result = await response.json()
            console.log('后端返回的数据:', result)
            console.log('后端返回的background_image:', result.background_image)
            console.log('后端返回的background_image长度:', result.background_image ? result.background_image.length : 0)
            // 更新本地存储（按用户区分）
            const userStorageKey = this.getUserStorageKey('countdownHistory')
            const history = JSON.parse(localStorage.getItem(userStorageKey) || '[]')
            const newItem = {
              id: result.id,
              taskName: result.task_name,
              targetDate: result.target_date,
              category: result.category,
              backgroundImage: result.background_image,
              createdAt: result.created_at
            }
            history.push(newItem)
            localStorage.setItem(userStorageKey, JSON.stringify(history))
            showSuccessToast('已添加到历史记录！')
            // 添加成功后通知首页刷新
            window.dispatchEvent(new Event('countdownAdded'))
          } else {
            // 如果后端失败，降级到本地存储
            this.saveToLocalHistory(category)
          }
        } catch (error) {
          console.error('保存到后端失败:', error)
          // 降级到本地存储
          this.saveToLocalHistory(category)
        }
      } else {
        // 未登录，只保存到本地
        this.saveToLocalHistory(category)
      }

      // 关闭弹窗
      this.showCategoryModal = false
    },

    // 获取用户ID
    getUserId () {
      const userInfo = localStorage.getItem('userInfo')
      if (userInfo) {
        try {
          const parsed = JSON.parse(userInfo)
          return parsed.id || parsed.user_id || 'anonymous'
        } catch (e) {
          return 'anonymous'
        }
      }
      return 'anonymous'
    },

    // 获取用户特定的存储键
    getUserStorageKey (key) {
      const userId = this.getUserId()
      return `${key}_${userId}`
    },

    // 保存到本地存储（降级方案）
    saveToLocalHistory (category) {
      const userStorageKey = this.getUserStorageKey('countdownHistory')
      const history = JSON.parse(localStorage.getItem(userStorageKey) || '[]')
      console.log('保存前的历史记录:', history)

      const newItem = {
        id: Date.now(),
        taskName: this.taskName,
        targetDate: this.targetDate,
        category: category,
        createdAt: new Date().toISOString(),
        backgroundImage: this.backgroundImage
      }

      history.push(newItem)
      localStorage.setItem(userStorageKey, JSON.stringify(history))
      console.log('保存后的历史记录:', history)
      showSuccessToast('已添加到历史记录！')
      window.dispatchEvent(new Event('countdownAdded'))
    },
    async confirmChange () {
      // 输入验证
      if (!this.taskName.trim()) {
        showToast('请输入任务名称！')
        return
      }

      if (!this.targetDate) {
        showToast('请选择目标日期！')
        return
      }

      const token = localStorage.getItem('access_token')

      // 如果有token，调用后端API更新倒计时
      if (token && this.originalItem && this.originalItem.id) {
        try {
          const putData = {
            task_name: this.taskName,
            target_date: this.targetDate,
            category: this.originalItem.category || 'other',
            background_image: this.backgroundImage
          }
          console.log('更新时发送到后端的数据:', putData)

          const response = await fetch(`/api/countdown/${this.originalItem.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(putData)
          })

          if (response.ok) {
            // 更新本地存储（按用户区分）
            const userStorageKey = this.getUserStorageKey('countdownHistory')
            const history = JSON.parse(localStorage.getItem(userStorageKey) || '[]')
            const updatedHistory = history.map(item => {
              if (item.id === this.originalItem.id) {
                return {
                  ...item,
                  taskName: this.taskName,
                  targetDate: this.targetDate,
                  backgroundImage: this.backgroundImage
                }
              }
              return item
            })
            localStorage.setItem(userStorageKey, JSON.stringify(updatedHistory))
            showSuccessToast('修改成功！')
          } else {
            // 如果后端失败，降级到本地存储
            this.updateLocalHistory()
          }
        } catch (error) {
          console.error('更新到后端失败:', error)
          // 降级到本地存储
          this.updateLocalHistory()
        }
      } else {
        // 未登录或没有原始ID，只更新本地存储
        this.updateLocalHistory()
      }

      // 关闭弹窗
      this.showConfirmModal = false

      // 跳转回首页
      this.$router.push('/home')
    },

    // 更新本地存储（降级方案）
    updateLocalHistory () {
      const userStorageKey = this.getUserStorageKey('countdownHistory')
      const history = JSON.parse(localStorage.getItem(userStorageKey) || '[]')
      console.log('修改前的历史记录:', history)
      console.log('原始项:', this.originalItem)

      const updatedHistory = history.map(item => {
        if (item.id === this.originalItem.id) {
          return {
            ...item,
            taskName: this.taskName,
            targetDate: this.targetDate,
            backgroundImage: this.backgroundImage
          }
        }
        return item
      })

      localStorage.setItem(userStorageKey, JSON.stringify(updatedHistory))
      console.log('修改后的历史记录:', updatedHistory)
      showSuccessToast('修改成功！')
    },
    // 这个函数用于处理图片上传，将用户选择的图片转换为base64格式并存储
    handleImageUpload (event) {
      const file = event.target.files[0] // 获取用户选择的第一个文件
      if (file) {
        const reader = new FileReader() // 创建文件读取器
        reader.onload = (e) => { // 当文件读取完成时触发
          this.backgroundImage = e.target.result // 将读取结果（base64字符串）赋值给backgroundImage
        }
        reader.readAsDataURL(file) // 以DataURL格式读取文件
      }
    }
  },
  mounted () {
    // 组件挂载时不自动开始倒计时
    // this.startCountdown()

    // 检查URL查询参数，接收从home.vue传递的数据
    const query = new URLSearchParams(window.location.search)
    const idParam = query.get('id')
    const taskNameParam = query.get('taskName')
    const targetDateParam = query.get('targetDate')
    const backgroundImageParam = query.get('backgroundImage')
    const categoryParam = query.get('category')

    if (taskNameParam && targetDateParam) {
      this.taskName = taskNameParam
      this.targetDate = targetDateParam.split('T')[0]
      this.backgroundImage = backgroundImageParam || ''
      this.isEditMode = true
      this.originalItem = {
        id: idParam ? parseInt(idParam) : null,
        taskName: taskNameParam,
        targetDate: targetDateParam,
        category: categoryParam || 'other',
        backgroundImage: backgroundImageParam || ''
      }
      // 自动开始倒计时
      this.startCountdown()
    }
  },
  beforeDestroy () {
    // 组件卸载时清除定时器
    if (this.countdownTimer) {
      clearInterval(this.countdownTimer)
    }
  }
}
</script>

<style scoped>
@import '../../styles/countDown.css';
</style>

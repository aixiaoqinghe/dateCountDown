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
    saveToHistory (category) {
      // 输入验证
      if (!this.taskName.trim()) {
        showToast('请输入任务名称！')
        return
      }

      if (!this.targetDate) {
        showToast('请选择目标日期！')
        return
      }

      // 获取现有历史记录
      const history = JSON.parse(localStorage.getItem('countdownHistory') || '[]')
      console.log('保存前的历史记录:', history)

      // 创建新的历史记录项
      const newItem = {
        id: Date.now(), // 唯一ID
        taskName: this.taskName,
        targetDate: this.targetDate,
        category: category,
        createdAt: new Date().toISOString(),
        backgroundImage: this.backgroundImage // 保存背景图片
      }

      // 添加到历史记录
      history.push(newItem)

      // 保存到localStorage
      localStorage.setItem('countdownHistory', JSON.stringify(history))
      console.log('保存后的历史记录:', history)

      // 关闭弹窗
      this.showCategoryModal = false

      // 提示用户保存成功
      showSuccessToast('已添加到历史记录！')
    },
    confirmChange () {
      // 输入验证
      if (!this.taskName.trim()) {
        showToast('请输入任务名称！')
        return
      }

      if (!this.targetDate) {
        showToast('请选择目标日期！')
        return
      }

      // 获取现有历史记录
      const history = JSON.parse(localStorage.getItem('countdownHistory') || '[]')
      console.log('修改前的历史记录:', history)
      console.log('原始项:', this.originalItem)

      // 找到要更新的项并更新
      const updatedHistory = history.map(item => {
        if (item.taskName === this.originalItem.taskName && item.targetDate === this.originalItem.targetDate) {
          return {
            ...item,
            taskName: this.taskName,
            targetDate: this.targetDate,
            backgroundImage: this.backgroundImage // 更新背景图片
          }
        }
        return item
      })

      // 保存到localStorage
      localStorage.setItem('countdownHistory', JSON.stringify(updatedHistory))
      console.log('修改后的历史记录:', updatedHistory)

      // 关闭弹窗
      this.showConfirmModal = false

      // 提示用户修改成功
      showSuccessToast('修改成功！')

      // 跳转回首页
      this.$router.push('/home')
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
    const taskNameParam = query.get('taskName')
    const targetDateParam = query.get('targetDate')
    const backgroundImageParam = query.get('backgroundImage')

    if (taskNameParam && targetDateParam) {
      this.taskName = taskNameParam
      this.targetDate = targetDateParam
      this.backgroundImage = backgroundImageParam || ''
      this.isEditMode = true
      this.originalItem = {
        taskName: taskNameParam,
        targetDate: targetDateParam
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

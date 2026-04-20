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
        alert('请输入任务名称！')
        return
      }

      if (!this.targetDate) {
        alert('请选择目标日期！')
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
      alert('已添加到历史记录！')
    },
    confirmChange () {
      // 输入验证
      if (!this.taskName.trim()) {
        alert('请输入任务名称！')
        return
      }

      if (!this.targetDate) {
        alert('请选择目标日期！')
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
      alert('修改成功！')

      // 跳转回首页
      this.$router.push('/home')
    },
    handleImageUpload (event) {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.backgroundImage = e.target.result
        }
        reader.readAsDataURL(file)
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
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 容器样式 */
.countdown-container {
  padding: 20px;
  text-align: center;
  min-height: 70vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.countdown-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: moveBackground 20s linear infinite;
  z-index: 0;
}

/* 背景图片覆盖 */
.countdown-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  z-index: 0;
}

@keyframes moveBackground {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* 标题样式 */
.countdown-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 40px;
  color: #2c3e50;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 倒计时时间容器 */
.countdown-time {
  display: flex;
  justify-content: center;
  gap: 25px;
  margin-bottom: 50px;
  z-index: 1;
  flex-wrap: wrap;
}

/* 时间项样式 */
.time-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px 15px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  min-width: 110px;
}

.time-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 时间数字样式 */
.time-number {
  font-size: 56px;
  font-weight: 700;
  color: #3498db;
  font-family: 'Courier New', monospace;
  position: relative;
  display: inline-block;
  min-width: 80px;
}

.time-number::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #3498db, #e74c3c);
  border-radius: 3px;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.time-item:hover .time-number::after {
  transform: scaleX(1);
  transform-origin: left;
}

/* 时间单位样式 */
.time-unit {
  font-size: 18px;
  color: #7f8c8d;
  margin-top: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 输入区域样式 */
.countdown-input {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  z-index: 1;
  width: 100%;
  max-width: 400px;
}

/* 任务输入框样式 */
.task-input {
  padding: 15px 20px;
  font-size: 18px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  min-width: 220px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.task-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
  transform: translateY(-2px);
}

/* 日期输入框样式 */
.date-input {
  padding: 15px 20px;
  font-size: 18px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  min-width: 220px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.date-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
  transform: translateY(-2px);
}

/* 按钮组样式 */
.btn-group {
  display: flex;
  gap: 15px;
  margin-top: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

/* 按钮通用样式 */
.start-btn, .reset-btn, .save-btn {
  padding: 12px 24px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  position: relative;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 开始按钮样式 */
.start-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.start-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

/* 重置按钮样式 */
.reset-btn {
  background: linear-gradient(135deg, #95a5a6, #7f8c8d);
  color: white;
  box-shadow: 0 4px 12px rgba(149, 165, 166, 0.3);
}

.reset-btn:hover {
  background: linear-gradient(135deg, #7f8c8d, #6c757d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(149, 165, 166, 0.4);
}

/* 保存按钮样式 */
.save-btn {
  background: linear-gradient(135deg, #27ae60, #229954);
  color: white;
  box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
}

.save-btn:hover {
  background: linear-gradient(135deg, #229954, #1e8449);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(39, 174, 96, 0.4);
}

/* 背景图片按钮容器 */
.bg-image-btn-container {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

/* 背景图片按钮 */
.bg-image-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid #3498db;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.bg-image-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 加号图标 */
.plus-icon {
  font-size: 24px;
  font-weight: bold;
  color: #3498db;
}

/* 按钮提示 */
.btn-tooltip {
  position: absolute;
  right: 100%;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  margin-right: 10px;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 100;
}

.bg-image-btn:hover .btn-tooltip {
  opacity: 1;
  visibility: visible;
  transform: translateY(-50%) translateX(-5px);
}

/* 弹窗遮罩样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 弹窗内容样式 */
.modal-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 弹窗标题样式 */
.modal-content h3 {
  margin-bottom: 20px;
  color: #2c3e50;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
}

/* 确认消息样式 */
.confirm-message {
  margin-bottom: 30px;
  color: #34495e;
  font-size: 16px;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 确认按钮组样式 */
.confirm-btn-group {
  display: flex;
  gap: 15px;
  justify-content: center;
}

/* 确认按钮样式 */
.confirm-btn {
  padding: 12px 24px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

/* 取消按钮样式 */
.cancel-btn {
  padding: 12px 24px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  background: linear-gradient(135deg, #95a5a6, #7f8c8d);
  color: white;
  box-shadow: 0 4px 12px rgba(149, 165, 166, 0.3);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.cancel-btn:hover {
  background: linear-gradient(135deg, #7f8c8d, #6c757d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(149, 165, 166, 0.4);
}

/* 分类列表样式 */
.category-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 分类项样式 */
.category-item {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 16px;
}

.category-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .countdown-title {
    font-size: 24px;
  }

  .countdown-time {
    gap: 15px;
  }

  .time-item {
    min-width: 80px;
    padding: 15px 10px;
  }

  .time-number {
    font-size: 40px;
  }

  .time-unit {
    font-size: 14px;
  }

  .task-input,
  .date-input {
    min-width: 200px;
    font-size: 16px;
  }

  .btn-group {
    flex-direction: column;
    align-items: center;
  }

  .start-btn,
  .reset-btn,
  .save-btn {
    width: 200px;
  }

  .bg-image-btn {
    width: 35px;
    height: 35px;
  }

  .plus-icon {
    font-size: 20px;
  }
}
</style>

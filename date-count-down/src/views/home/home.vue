<template>
  <div class="home-container">
    <h1 class="home-title">任务栏</h1>
    <div class="countdown-list">
      <!-- 显示已存储的倒计时记录 -->
      <div
        v-for="item in sortedCountdowns"
        :key="item.id"
        class="countdown-card"
        :class="item.category"
        @click="navigateToCountdown(item)"
        :style="item.backgroundImage ? { backgroundImage: `url(${item.backgroundImage})`, backgroundSize: 'cover', backgroundPosition: 'center', backgroundRepeat: 'no-repeat' } : {}"
      >
        <div class="countdown-days">{{ item.days }}</div>
        <div class="countdown-info">
          <h3 class="card-title">{{ item.taskName }}</h3>
          <p class="card-date">{{ formatDate(item.targetDate) }}</p>
          <p class="card-days">{{ item.days }}天后</p>
          <span class="card-category">{{ getCategoryLabel(item.category) }}</span>
        </div>
      </div>
      <!-- 添加新任务的按钮 -->
      <div class="countdown-card add-card" @click="navigateToCountdown()">
        <div class="add-icon">+</div>
        <div class="add-text">添加新任务</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'homeHome',
  data () {
    return {
      countdowns: []
    }
  },
  computed: {
    // 计算并排序倒计时记录
    sortedCountdowns () {
      return this.countdowns
        .map(item => {
          // 计算距离目标日期的天数
          const target = new Date(item.targetDate).getTime()
          const now = new Date().getTime()
          const distance = target - now
          const days = Math.max(0, Math.floor(distance / (1000 * 60 * 60 * 24)))
          return {
            ...item,
            days
          }
        })
        .sort((a, b) => a.days - b.days) // 按照距离排序，最近的在前
    }
  },
  methods: {
    // 获取分类标签
    getCategoryLabel (category) {
      const categories = {
        life: '生活',
        study: '学习',
        work: '工作',
        anniversary: '纪念日',
        other: '其他'
      }
      return categories[category] || '其他'
    },
    // 格式化日期
    formatDate (dateString) {
      const date = new Date(dateString)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    },
    // 导航到倒计时页面
    navigateToCountdown (item) {
      if (item) {
        this.$router.push({
          path: '/home/countDown',
          query: {
            taskName: item.taskName,
            targetDate: item.targetDate,
            category: item.category,
            backgroundImage: item.backgroundImage || ''
          }
        })
      } else {
        this.$router.push('/home/countDown')
      }
    },
    // 加载存储的倒计时记录
    loadCountdowns () {
      const history = JSON.parse(localStorage.getItem('countdownHistory') || '[]')
      console.log('加载的历史记录:', history)
      this.countdowns = history
    }
  },
  mounted () {
    // 组件挂载时加载数据
    this.loadCountdowns()
  },
  // 监听页面可见性，当页面重新可见时刷新数据
  created () {
    window.addEventListener('visibilitychange', () => {
      if (!document.hidden) {
        this.loadCountdowns()
      }
    })
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

.home-container {
  padding: 20px;
  min-height: 70vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.home-container::before {
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

@keyframes moveBackground {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* 标题样式 */
.home-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 30px;
  color: #2c3e50;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
}

/* 倒计时列表样式 */
.countdown-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  z-index: 1;
  position: relative;
}

/* 倒计时卡片样式 */
.countdown-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  overflow: hidden;
}

.countdown-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 卡片内容区域，确保文字在背景图片上清晰可见 */
.countdown-info {
  flex: 1;
  text-align: left;
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.7);
  padding: 15px;
  border-radius: 8px;
}

/* 天数显示样式 */
.countdown-days {
  font-size: 48px;
  font-weight: 700;
  color: #2c3e50;
  font-family: 'Courier New', monospace;
  min-width: 100px;
  text-align: center;
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.7);
  padding: 10px;
  border-radius: 8px;
}

/* 不同分类的颜色 */
.countdown-card.life {
  border-left: 6px solid #3498db;
}

.countdown-card.study {
  border-left: 6px solid #f39c12;
}

.countdown-card.work {
  border-left: 6px solid #27ae60;
}

.countdown-card.anniversary {
  border-left: 6px solid #e74c3c;
}

.countdown-card.other {
  border-left: 6px solid #9b59b6;
}

/* 任务名称样式 */
.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 日期样式 */
.card-date {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 4px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 天数文本样式 */
.card-days {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 8px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 分类样式 */
.card-category {
  font-size: 12px;
  color: #95a5a6;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 添加卡片样式 */
.add-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 150px;
  border: 2px dashed #bdc3c7;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-card:hover {
  border-color: #3498db;
  background: rgba(52, 152, 219, 0.05);
}

/* 添加图标样式 */
.add-icon {
  font-size: 48px;
  font-weight: 300;
  color: #bdc3c7;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.add-card:hover .add-icon {
  color: #3498db;
  transform: scale(1.1);
}

/* 添加文本样式 */
.add-text {
  font-size: 16px;
  color: #7f8c8d;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  transition: all 0.3s ease;
}

.add-card:hover .add-text {
  color: #3498db;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-title {
    font-size: 24px;
  }

  .countdown-list {
    grid-template-columns: 1fr;
  }

  .countdown-card {
    flex-direction: column;
    text-align: center;
  }

  .countdown-days {
    font-size: 36px;
    margin-bottom: 15px;
  }

  .countdown-info {
    text-align: center;
  }
}
</style>

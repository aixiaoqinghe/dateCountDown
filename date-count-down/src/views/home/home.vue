<template>
  <div class="home-container" :class="{ 'delete-mode': isDeleteMode }">
    <div class="home-header">
      <h1 class="home-title">任务栏</h1>
      <div v-if="isDeleteMode" class="delete-controls">
        <button @click="selectAll" class="control-btn">全选</button>
        <button @click="confirmDelete" class="delete-btn">删除</button>
        <button @click="cancelDelete" class="control-btn">取消</button>
      </div>
      <div v-else class="header-actions">
        <button @click="enterDeleteMode" class="delete-icon-btn" title="删除任务">
          <span class="delete-icon">🗑️</span>
          <span class="delete-tooltip">删除</span>
        </button>
      </div>
    </div>
    <div class="countdown-list">
      <!-- 显示已存储的倒计时记录 -->
      <div
        v-for="item in sortedCountdowns"
        :key="item.id"
        class="countdown-card"
        :class="item.category"
        @click="isDeleteMode ? () => {} : navigateToCountdown(item)"
        :style="getCardStyle(item)"
      >
        <!-- 复选框 -->
        <input
          v-if="isDeleteMode"
          type="checkbox"
          class="card-checkbox"
          v-model="selectedItems"
          :value="item.id"
          @click.stop
        />
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

    <!-- 删除确认弹窗 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-content" @click.stop>
        <h3>确认删除</h3>
        <p class="confirm-message">确定要删除选中的 {{ selectedItems.length }} 个任务吗？</p>
        <div class="confirm-btn-group">
          <button @click="performDelete" class="confirm-btn">确定</button>
          <button @click="showDeleteModal = false" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { showToast, showSuccessToast } from 'vant'
export default {
  name: 'homeHome',
  data () {
    return {
      countdowns: [], // 存储所有倒计时任务
      isDeleteMode: false, // 控制是否进入删除模式
      selectedItems: [], // 存储选中的任务ID数组
      showDeleteModal: false // 控制删除确认弹窗的显示
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
    // 获取卡片样式（处理背景图片）
    getCardStyle (item) {
      if (item.backgroundImage && item.backgroundImage.trim()) {
        return {
          backgroundImage: `url(${item.backgroundImage})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat'
        }
      }
      return {}
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
            id: item.id,
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
    // 获取当前用户唯一标识（用于区分不同用户的数据）
    getUserId () {
      const userInfo = localStorage.getItem('userInfo')
      if (userInfo) {
        try {
          const parsed = JSON.parse(userInfo)
          return parsed.id || parsed.user_id || 'anonymous'
        } catch {
          return 'anonymous'
        }
      }
      return 'anonymous'
    },

    // 获取用户专属的本地存储key
    getUserStorageKey (key) {
      const userId = this.getUserId()
      return `${key}_${userId}`
    },

    // 加载存储的倒计时记录
    async loadCountdowns () {
      const token = localStorage.getItem('access_token')
      const userStorageKey = this.getUserStorageKey('countdownHistory')

      if (token) {
        // 如果有token，尝试从后端获取数据
        try {
          const response = await fetch('/api/countdown', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })

          if (response.ok) {
            const data = await response.json()
            // 将后端返回的字段名转换为前端使用的格式
            const formattedData = data.map(item => ({
              id: item.id,
              taskName: item.task_name,
              targetDate: item.target_date,
              category: item.category,
              backgroundImage: item.background_image,
              createdAt: item.created_at
            }))
            this.countdowns = formattedData
            // 同时保存到本地存储作为缓存（按用户区分）
            localStorage.setItem(userStorageKey, JSON.stringify(formattedData))
            return
          }
        } catch (error) {
          console.error('从后端获取数据失败:', error)
        }
      }

      // 如果没有token或后端请求失败，使用本地存储（按用户区分）
      const history = JSON.parse(localStorage.getItem(userStorageKey) || '[]')
      this.countdowns = history
    },

    // 进入删除模式
    enterDeleteMode () {
      this.isDeleteMode = true
      this.selectedItems = []
    },
    // 取消删除模式
    cancelDelete () {
      this.isDeleteMode = false
      this.selectedItems = []
    },
    // 全选
    selectAll () {
      if (this.selectedItems.length === this.sortedCountdowns.length) {
        // 取消全选
        this.selectedItems = []
      } else {
        // 全选
        this.selectedItems = this.sortedCountdowns.map(item => item.id)
      }
    },
    // 确认删除
    confirmDelete () {
      if (this.selectedItems.length === 0) {
        showToast('请选择要删除的任务')
        return
      }
      this.showDeleteModal = true
    },
    // 执行删除
    async performDelete () {
      const token = localStorage.getItem('access_token')

      // 如果有token，并行调用后端删除API（优化性能）
      if (token) {
        try {
          // 使用Promise.all并行删除，大幅提升速度
          const deletePromises = this.selectedItems.map(id =>
            fetch(`/api/countdown/${id}`, {
              method: 'DELETE',
              headers: {
                Authorization: `Bearer ${token}`
              }
            })
          )
          await Promise.all(deletePromises)
        } catch (error) {
          console.error('从后端删除失败:', error)
        }
      }

      // 更新本地存储（按用户区分）
      const updatedHistory = this.countdowns.filter(item => !this.selectedItems.includes(item.id))
      const userStorageKey = this.getUserStorageKey('countdownHistory')
      localStorage.setItem(userStorageKey, JSON.stringify(updatedHistory))
      // 重新加载数据
      this.loadCountdowns()
      // 关闭弹窗
      this.showDeleteModal = false
      // 退出删除模式
      this.isDeleteMode = false
      this.selectedItems = []
      // 提示用户
      showSuccessToast('删除成功！')
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
@import '../../styles/home.css';
</style>

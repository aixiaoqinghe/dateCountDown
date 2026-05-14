<template>
  <div class="home-container" :class="{ 'delete-mode': isDeleteMode }">
    <div class="home-header">
      <h1 class="home-title">任务</h1>
      <!-- 添加搜索 -->
      <div class="search-box">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜索任务..."
          class="search-input"
          @input="handleSearchInput"
        />
        <span class="search-icon">🔍</span>
      </div>
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

    <!-- 骨架屏加载状态 -->
    <Skeleton v-if="!isLoaded" />

    <div v-else class="countdown-list">
      <!-- 显示已存在的倒计时记录 -->
      <div
        v-for="item in (filteredCountdowns.length > 0 ? filteredCountdowns : sortedCountdowns)"
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
import { debounce } from '@/utils/throttle.js'
import Skeleton from '@/components/Skeleton.vue'
import { get, del } from '@/api/request.js'
export default {
  name: 'homeHome',
  components: {
    Skeleton
  },
  data () {
    return {
      countdowns: [],
      isDeleteMode: false,
      selectedItems: [],
      showDeleteModal: false,
      lastLoadTime: 0,
      cacheDuration: 300000,
      searchQuery: '',
      filteredCountdowns: [],
      isLoaded: false,
      sortedCache: null,
      cacheKey: null
    }
  },
  created () {
    this.debouncedSearch = debounce(this.performSearch, 300)
    this.updateSortedCache()
  },
  watch: {
    countdowns: {
      deep: true,
      handler () {
        this.updateSortedCache()
      }
    }
  },
  computed: {
    sortedCountdowns () {
      return this.sortedCache || this.countdowns.map(item => {
        const target = new Date(item.targetDate).getTime()
        const now = Date.now()
        const distance = target - now
        const days = Math.max(0, Math.floor(distance / (1000 * 60 * 60 * 24)))
        return {
          ...item,
          days
        }
      }).sort((a, b) => a.days - b.days)
    }
  },
  methods: {
    updateSortedCache () {
      const currentKey = JSON.stringify(this.countdowns)
      if (this.cacheKey === currentKey) {
        return
      }

      this.sortedCache = this.countdowns.map(item => {
        const target = new Date(item.targetDate).getTime()
        const now = Date.now()
        const distance = target - now
        const days = Math.max(0, Math.floor(distance / (1000 * 60 * 60 * 24)))
        return {
          ...item,
          days
        }
      }).sort((a, b) => a.days - b.days)

      this.cacheKey = currentKey
    },
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
    formatDate (dateString) {
      const date = new Date(dateString)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    },
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
    async loadCountdowns () {
      try {
        const now = Date.now()
        if (now - this.lastLoadTime < this.cacheDuration && this.countdowns.length > 0) {
          console.log('[性能优化] 使用缓存数据')
          return
        }

        console.log('[性能优化] 从后端加载数据，更新缓存')
        const data = await get('/api/countdown')

        if (data && Array.isArray(data)) {
          this.countdowns = data.map(item => ({
            ...item,
            taskName: item.task_name,
            targetDate: item.target_date,
            backgroundImage: item.background_image
          }))
        } else {
          this.countdowns = []
        }

        this.lastLoadTime = now
        this.isLoaded = true
      } catch (error) {
        console.error('从后端获取数据失败', error)
        this.countdowns = []
        this.isLoaded = true
      }
    },
    enterDeleteMode () {
      this.isDeleteMode = true
    },
    cancelDelete () {
      this.isDeleteMode = false
      this.selectedItems = []
    },
    selectAll () {
      if (this.selectedItems.length === this.countdowns.length) {
        this.selectedItems = []
      } else {
        this.selectedItems = this.countdowns.map(item => item.id)
      }
    },
    confirmDelete () {
      if (this.selectedItems.length === 0) {
        showToast('请选择要删除的任务')
        return
      }
      this.showDeleteModal = true
    },
    async performDelete () {
      try {
        for (const id of this.selectedItems) {
          await del(`/api/countdown/${id}`)
        }
        showSuccessToast('删除成功')
        this.countdowns = this.countdowns.filter(item => !this.selectedItems.includes(item.id))
        this.selectedItems = []
        this.showDeleteModal = false
        this.isDeleteMode = false
      } catch (error) {
        console.error('删除失败:', error)
        showToast('删除失败')
      }
    },
    performSearch () {
      if (!this.searchQuery.trim()) {
        this.filteredCountdowns = []
        return
      }

      const query = this.searchQuery.toLowerCase()
      this.filteredCountdowns = this.sortedCountdowns.filter(item =>
        item.taskName.toLowerCase().includes(query)
      )
    },
    handleSearchInput () {
      this.debouncedSearch()
    }
  },
  mounted () {
    this.loadCountdowns()

    window.addEventListener('countdownAdded', () => {
      this.loadCountdowns()
    })

    this.visibilityHandler = debounce(() => {
      if (!document.hidden) {
        this.loadCountdowns()
      }
    }, 1000)
    window.addEventListener('visibilitychange', this.visibilityHandler)
  },
  beforeUnmount () {
    window.removeEventListener('visibilitychange', this.visibilityHandler)
  }
}
</script>

<style scoped>
@import '../../styles/home.css';
</style>

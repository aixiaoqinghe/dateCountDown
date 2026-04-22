<template>
  <div class="mark-container">
    <!-- 搜索框 -->
    <van-search
      v-model="value"
      placeholder="请输入搜索关键词"
      wrap-with-form
      show-action
      @search="onSearch"
      @cancel="onCancel"
      input-align="center"
      shape="round"
    />

    <!-- 主内容区域 -->
    <div class="content-wrapper">
      <!-- 侧边导航栏 -->
      <div class="sidebar-container">
        <van-sidebar v-model="active">
          <van-sidebar-item title="背景" />
          <van-sidebar-item title="字体" />
          <van-sidebar-item title="颜色" />
        </van-sidebar>
      </div>

      <!-- 右侧内容区域 -->
      <div class="content-area">
        <!-- 背景设置内容 -->
        <div v-if="active === 0" class="setting-content">
          <h3>背景设置</h3>
          <!-- 背景设置相关内容将在此处添加 -->
          <div class="placeholder">背景设置内容区域</div>
        </div>

        <!-- 字体设置内容 -->
        <div v-else-if="active === 1" class="setting-content">
          <h3>字体设置</h3>
          <!-- 字体设置相关内容将在此处添加 -->
          <div class="placeholder">字体设置内容区域</div>
        </div>

        <!-- 颜色设置内容 -->
        <div v-else-if="active === 2" class="setting-content">
          <h3>颜色设置</h3>
          <!-- 颜色设置相关内容将在此处添加 -->
          <div class="placeholder">颜色设置内容区域</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { showToast } from 'vant'
export default {
  name: 'homeMark',
  setup () {
    // 搜索相关状态
    const value = ref('')

    // 侧边导航栏激活状态
    const active = ref(0)

    // 搜索处理函数
    const onSearch = (val) => showToast(`搜索:${val || '无'}`)

    // 取消搜索处理函数
    const onCancel = () => showToast('取消')

    return {
      value,
      active,
      onSearch,
      onCancel
    }
  }
}
</script>

<style scoped>
.mark-container {
  padding: 20px;
}

/* 主内容区域布局 */
.content-wrapper {
  display: flex;
  margin-top: 20px;
  gap: 20px;
}

/* 侧边导航栏样式 */
.sidebar-container {
  width: 120px;
}

.van-sidebar {
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.van-sidebar-item {
  font-size: 16px;
  padding: 12px 20px;
  transition: all 0.3s ease;
}

.van-sidebar-item--active {
  background-color: #3498db;
  color: #ffffff;
}

/* 右侧内容区域样式 */
.content-area {
  flex: 1;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  min-height: 400px;
}

.setting-content h3 {
  margin-bottom: 20px;
  color: #333;
}

/* 占位符样式 */
.placeholder {
  padding: 40px 20px;
  background-color: #ffffff;
  border-radius: 8px;
  text-align: center;
  color: #999;
  font-size: 16px;
  border: 1px dashed #e0e0e0;
}
</style>

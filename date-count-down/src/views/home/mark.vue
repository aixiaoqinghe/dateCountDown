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

    <!-- 功能开发中弹窗 -->
    <div v-if="showDevModal" class="dev-modal-overlay" @click="closeDevModal">
      <div class="dev-modal" @click.stop>
        <div class="dev-modal-icon">
          <span class="emoji">😔</span>
        </div>
        <h3 class="dev-modal-title">功能开发中</h3>
        <p class="dev-modal-text">
          非常抱歉，您尝试使用的功能目前还在开发中。<br>
          我们正在努力完善，敬请期待！
        </p>
        <div class="dev-modal-decoration">
          <span>✨</span>
          <span>💪</span>
          <span>🚀</span>
        </div>
        <button class="dev-modal-btn" @click="closeDevModal">
          知道了
        </button>
      </div>
    </div>

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
          <div class="bg-section">
            <h4>推荐背景</h4>
            <div class="bg-options">
              <div class="bg-option" :class="{ active: selectedBg === 'default' }" @click="selectBg('default')" :style="{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }"><span class="bg-label">默认</span><span v-if="selectedBg === 'default'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === '#3498db' }" @click="selectBg('#3498db')" :style="{ background: '#3498db' }"><span class="bg-label">蓝色</span><span v-if="selectedBg === '#3498db'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === '#2ecc71' }" @click="selectBg('#2ecc71')" :style="{ background: '#2ecc71' }"><span class="bg-label">绿色</span><span v-if="selectedBg === '#2ecc71'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === '#e74c3c' }" @click="selectBg('#e74c3c')" :style="{ background: '#e74c3c' }"><span class="bg-label">红色</span><span v-if="selectedBg === '#e74c3c'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === '#f39c12' }" @click="selectBg('#f39c12')" :style="{ background: '#f39c12' }"><span class="bg-label">橙色</span><span v-if="selectedBg === '#f39c12'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === '#9b59b6' }" @click="selectBg('#9b59b6')" :style="{ background: '#9b59b6' }"><span class="bg-label">紫色</span><span v-if="selectedBg === '#9b59b6'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === 'gradient1' }" @click="selectBg('gradient1')" :style="{ background: 'linear-gradient(135deg, #182848 0%, #4b6cb7 100%)' }"><span class="bg-label">深蓝渐变</span><span v-if="selectedBg === 'gradient1'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === 'gradient2' }" @click="selectBg('gradient2')" :style="{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }"><span class="bg-label">粉紫渐变</span><span v-if="selectedBg === 'gradient2'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === 'gradient3' }" @click="selectBg('gradient3')" :style="{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }"><span class="bg-label">天蓝渐变</span><span v-if="selectedBg === 'gradient3'" class="check-icon">✓</span></div>
              <div class="bg-option" :class="{ active: selectedBg === 'gradient4' }" @click="selectBg('gradient4')" :style="{ background: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)' }"><span class="bg-label">清新渐变</span><span v-if="selectedBg === 'gradient4'" class="check-icon">✓</span></div>
            </div>
          </div>
          <div class="bg-section">
            <h4>自定义背景</h4>
            <div class="custom-bg-area">
              <input type="file" ref="fileInput" accept="image/*" @change="handleCustomBgUpload" style="display: none;" />
              <div class="custom-bg-btn" @click="triggerFileInput">
                <span class="upload-icon">+</span>
                <span class="upload-text">上传图片</span>
                <span v-if="selectedBg && selectedBg.startsWith('data:image')" class="delete-icon" @click.stop="deleteCustomBg">
                  ×
                </span>
              </div>
              <p class="custom-tip">支持 JPG、PNG、GIF 格式</p>
            </div>
          </div>
          <div class="confirm-section">
            <button class="reset-btn" @click="resetToDefault">恢复默认</button>
            <button class="confirm-btn" @click="confirmBgChange">修改背景</button>
          </div>
        </div>

        <!-- 字体设置内容 -->
        <div v-else-if="active === 1" class="setting-content">
          <div class="under-development">
            <div class="development-icon">🛠️</div>
            <h3>字体设置</h3>
            <p class="development-text">功能开发中</p>
            <div class="progress-container">
              <div class="progress-bar">
                <div class="progress-fill">
                  <span class="progress-icon">📝</span>
                </div>
              </div>
              <span class="progress-text">开发进度</span>
            </div>
            <p class="development-hint">敬请期待...</p>
          </div>
        </div>

        <!-- 颜色设置内容 -->
        <div v-else-if="active === 2" class="setting-content">
          <div class="under-development">
            <div class="development-icon">🎨</div>
            <h3>颜色设置</h3>
            <p class="development-text">功能开发中</p>
            <div class="progress-container">
              <div class="progress-bar">
                <div class="progress-fill">
                  <span class="progress-icon">🎨</span>
                </div>
              </div>
              <span class="progress-text">开发进度</span>
            </div>
            <p class="development-hint">敬请期待...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'homeMark',
  setup () {
    // 搜索相关状态
    const value = ref('')

    // 侧边导航栏激活状态
    const active = ref(0)

    // 背景选择状态
    const selectedBg = ref(localStorage.getItem('appBackground') || 'default')

    // 开发中弹窗状态
    const showDevModal = ref(false)

    // 打开开发中弹窗
    const openDevModal = () => {
      showDevModal.value = true
    }

    // 关闭开发中弹窗
    const closeDevModal = () => {
      showDevModal.value = false
    }

    // 选择背景
    const selectBg = (bg) => {
      openDevModal()
    }

    // 处理自定义背景上传
    const handleCustomBgUpload = (event) => {
      openDevModal()
    }

    // 确认修改背景
    const confirmBgChange = () => {
      openDevModal()
    }

    // 恢复默认背景
    const resetToDefault = () => {
      openDevModal()
    }

    // 删除自定义背景
    const deleteCustomBg = () => {
      openDevModal()
    }

    // 触发文件选择对话框
    const triggerFileInput = () => {
      openDevModal()
    }

    return {
      value,
      active,
      selectedBg,
      selectBg,
      handleCustomBgUpload,
      confirmBgChange,
      deleteCustomBg,
      triggerFileInput,
      resetToDefault,
      showDevModal,
      closeDevModal
    }
  }
}
</script>

<style scoped>
@import '../../styles/mark.css';
</style>

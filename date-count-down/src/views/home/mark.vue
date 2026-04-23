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
import { showToast, showSuccessToast } from 'vant'
export default {
  name: 'homeMark',
  setup () {
    // 搜索相关状态
    const value = ref('')

    // 侧边导航栏激活状态
    const active = ref(0)

    // 背景选择状态
    const selectedBg = ref(localStorage.getItem('appBackground') || 'default')

    // 搜索处理函数
    const onSearch = (val) => showToast(`搜索:${val || '无'}`)

    // 取消搜索处理函数
    const onCancel = () => showToast('取消')

    // 选择背景
    const selectBg = (bg) => {
      selectedBg.value = bg
    }

    // 处理自定义背景上传
    const handleCustomBgUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          selectedBg.value = e.target.result
          showSuccessToast('图片上传成功')
        }
        reader.readAsDataURL(file)
      }
    }

    // 确认修改背景
    const confirmBgChange = () => {
      try {
        console.log('confirmBgChange called')
        if (!selectedBg.value) {
          console.log('no background selected')
          showToast('请选择背景')
          return
        }

        console.log('saving background')
        // 保存背景设置到本地存储
        console.log('selectedBg.value:', selectedBg.value)
        localStorage.setItem('appBackground', selectedBg.value)
        console.log('background saved to localStorage:', localStorage.getItem('appBackground'))

        // 直接修改 body 和 #app 元素的背景样式
        const appElement = document.getElementById('app')
        if (selectedBg.value === 'default') {
          const defaultBg = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
          document.body.style.background = defaultBg
          if (appElement) appElement.style.background = defaultBg
        } else if (selectedBg.value === 'gradient1') {
          const bg = 'linear-gradient(135deg, #182848 0%, #4b6cb7 100%)'
          document.body.style.background = bg
          if (appElement) appElement.style.background = bg
        } else if (selectedBg.value === 'gradient2') {
          const bg = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
          document.body.style.background = bg
          if (appElement) appElement.style.background = bg
        } else if (selectedBg.value === 'gradient3') {
          const bg = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
          document.body.style.background = bg
          if (appElement) appElement.style.background = bg
        } else if (selectedBg.value === 'gradient4') {
          const bg = 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
          document.body.style.background = bg
          if (appElement) appElement.style.background = bg
        } else if (selectedBg.value.startsWith('#')) {
          document.body.style.background = selectedBg.value
          if (appElement) appElement.style.background = selectedBg.value
        } else {
          document.body.style.background = `url(${selectedBg.value})`
          document.body.style.backgroundSize = 'cover'
          document.body.style.backgroundPosition = 'center'
          document.body.style.backgroundRepeat = 'no-repeat'
          if (appElement) {
            appElement.style.background = `url(${selectedBg.value})`
            appElement.style.backgroundSize = 'cover'
            appElement.style.backgroundPosition = 'center'
            appElement.style.backgroundRepeat = 'no-repeat'
          }
        }

        // 显示修改成功提示
        showSuccessToast('背景修改成功')
      } catch (error) {
        console.error('Error in confirmBgChange:', error)
        showToast('修改背景失败')
      }
    }

    // 恢复默认背景
    const resetToDefault = () => {
      try {
        // 保存默认背景设置到本地存储
        localStorage.setItem('appBackground', 'default')
        selectedBg.value = 'default'

        // 直接修改 body 和 #app 元素的背景样式为默认背景
        const defaultBg = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        document.body.style.background = defaultBg
        const appElement = document.getElementById('app')
        if (appElement) appElement.style.background = defaultBg

        // 显示恢复成功提示
        showSuccessToast('已恢复默认背景')
      } catch (error) {
        console.error('Error in resetToDefault:', error)
        showToast('恢复默认背景失败')
      }
    }

    // 删除自定义背景
    const deleteCustomBg = () => {
      selectedBg.value = ''
      showToast('已删除自定义背景')
    }

    // 触发文件选择对话框
    const triggerFileInput = () => {
      document.querySelector('input[type="file"]').click()
    }

    return {
      value,
      active,
      selectedBg,
      onSearch,
      onCancel,
      selectBg,
      handleCustomBgUpload,
      confirmBgChange,
      deleteCustomBg,
      triggerFileInput,
      resetToDefault
    }
  }
}
</script>

<style scoped>
@import '../../styles/mark.css';
</style>

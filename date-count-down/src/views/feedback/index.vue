<template>
  <div class="feedback-container">
    <div class="feedback-header">
      <button class="back-btn" @click="goBack">←</button>
      <h2>意见反馈</h2>
      <div class="placeholder"></div>
    </div>

    <div class="feedback-content">
      <!-- 评分组件 -->
      <div class="feedback-rating">
        <h3>请对我们的应用进行评分</h3>
        <van-rate v-model="feedbackRating" :size="40" color="#ffb400" />
      </div>

      <!-- 反馈类型选择 -->
      <div class="feedback-type">
        <h3>反馈类型</h3>
        <div class="feedback-type-options">
          <div v-for="item in feedbackTypes" :key="item.value" class="feedback-type-option">
            <input type="radio" :id="'type-' + item.value" name="feedbackType" :value="item.value" v-model="feedbackType" />
            <label :for="'type-' + item.value">{{ item.label }}</label>
          </div>
        </div>
      </div>

      <!-- 反馈内容 -->
      <div class="feedback-text">
        <h3>反馈内容</h3>
        <textarea
          v-model="feedbackContent"
          placeholder="请输入您的反馈内容"
          maxlength="200"
          class="feedback-textarea"
        ></textarea>
        <div class="word-count">{{ feedbackContent.length }}/200</div>
      </div>

      <!-- 提交按钮 -->
      <button class="submit-btn" @click="submitFeedback">提交反馈</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showSuccessToast } from 'vant'

export default {
  name: 'homeFeedback',
  setup () {
    const router = useRouter()

    // 监听主题变化
    const updateTheme = () => {
      const theme = localStorage.getItem('theme') || 'light'
      if (theme === 'dark') {
        document.documentElement.classList.add('dark-theme')
      } else {
        document.documentElement.classList.remove('dark-theme')
      }
    }

    // 监听字体变化
    const updateFont = () => {
      const selectedFont = localStorage.getItem('font') || 'default'
      document.documentElement.setAttribute('data-font', selectedFont)
    }

    // 反馈功能
    const feedbackRating = ref(0)
    const feedbackContent = ref('')
    const feedbackType = ref('')
    const feedbackTypes = [
      { value: 'suggestion', label: '功能建议' },
      { value: 'bug', label: 'bug反馈' },
      { value: 'performance', label: '性能问题' },
      { value: 'ui', label: '界面设计' },
      { value: 'experience', label: '用户体验' },
      { value: 'other', label: '其他' }
    ]

    // 返回上一页
    const goBack = function () {
      router.back()
    }

    // 提交反馈
    const submitFeedback = function () {
      if (feedbackRating.value === 0) {
        showToast('请先进行评分')
        return
      }

      if (!feedbackContent.value.trim()) {
        showToast('请输入反馈内容')
        return
      }

      if (!feedbackType.value) {
        showToast('请选择反馈类型')
        return
      }

      // 模拟网络请求延迟
      setTimeout(() => {
        // 这里可以添加实际的反馈提交逻辑
        console.log('提交的反馈:', {
          rating: feedbackRating.value,
          content: feedbackContent.value,
          type: feedbackType.value,
          date: new Date().toISOString()
        })

        showSuccessToast('反馈提交成功，感谢您的建议！')

        // 提交成功后返回上一页
        setTimeout(() => {
          router.back()
        }, 1000)
      }, 1000)
    }

    onMounted(() => {
      updateTheme()
      updateFont()

      // 监听本地存储变化，实时更新主题和字体
      window.addEventListener('storage', (event) => {
        if (event.key === 'theme') {
          updateTheme()
        } else if (event.key === 'font') {
          updateFont()
        }
      })
    })

    return {
      feedbackRating,
      feedbackContent,
      feedbackType,
      feedbackTypes,
      goBack,
      submitFeedback
    }
  }
}
</script>

<style>
.feedback-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding-top: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feedback-content {
  width: 100%;
  max-width: 500px;
  padding: 20px;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

.feedback-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  backdrop-filter: blur(10px);
  height: 40px;
}

.back-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #333;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #f8f9fa;
  color: #3498db;
}

.feedback-header h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.placeholder {
  width: 30px;
}

.feedback-rating {
  margin-bottom: 30px;
  text-align: center;
}

.feedback-rating h3 {
  margin-bottom: 20px;
  font-size: 16px;
  color: #333;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.feedback-type {
  margin-bottom: 30px;
}

.feedback-type h3 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #333;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.feedback-type-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px 0;
}

.feedback-type-option {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.feedback-type-option:hover {
  background: #f8f9fa;
  border-color: #3498db;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.feedback-type-option input[type="radio"] {
  width: 18px;
  height: 18px;
  margin-right: 12px;
  accent-color: #3498db;
  cursor: pointer;
  z-index: 1;
}

.feedback-type-option label {
  flex: 1;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
}

.feedback-type-option:hover label {
  color: #3498db;
}

.feedback-text {
  margin-bottom: 30px;
}

.feedback-text h3 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #333;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.feedback-textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  resize: none;
  font-size: 14px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  min-height: 120px;
  position: relative;
  z-index: 2;
  pointer-events: auto;
}

.feedback-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.word-count {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.submit-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
  position: relative;
  z-index: 2;
  pointer-events: auto;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #2980b9 0%, #1f618d 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(52, 152, 219, 0.4);
}

.submit-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
}

/* 深色主题 */
.dark-theme .feedback-container {
  background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
}

.dark-theme .feedback-header {
  background: rgba(44, 44, 44, 0.95);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.dark-theme .back-btn {
  color: #e0e0e0;
}

.dark-theme .back-btn:hover {
  background: #3a3a3a;
  color: #3498db;
}

.dark-theme .feedback-header h2 {
  color: #e0e0e0;
}

.dark-theme .feedback-rating h3 {
  color: #e0e0e0;
}

.dark-theme .feedback-type h3 {
  color: #e0e0e0;
}

.dark-theme .feedback-type-option {
  background: rgba(58, 58, 58, 0.9);
  border-color: #444;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.dark-theme .feedback-type-option:hover {
  background: #444;
  border-color: #3498db;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.dark-theme .feedback-type-option label {
  color: #e0e0e0;
}

.dark-theme .feedback-type-option:hover label {
  color: #3498db;
}

.dark-theme .feedback-type-option input[type="radio"] {
  accent-color: #3498db;
}

.dark-theme .feedback-text h3 {
  color: #e0e0e0;
}

.dark-theme .feedback-textarea {
  color: #e0e0e0;
  background: #3a3a3a;
  border-color: #444;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.dark-theme .feedback-textarea:focus {
  border-color: #3498db;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.dark-theme .word-count {
  color: #777;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .feedback-content {
    padding: 15px;
  }

  .feedback-rating h3,
  .feedback-type h3,
  .feedback-text h3 {
    font-size: 15px;
  }

  .feedback-type-option {
    padding: 12px;
  }

  .feedback-textarea {
    padding: 12px;
  }

  .submit-btn {
    padding: 12px;
    font-size: 15px;
  }
}

</style>

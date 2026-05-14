<template>
  <div class="verify-container">
    <!-- 返回按钮 -->
    <button class="back-btn" @click="handleBack">
      &larr; 返回
    </button>
    <h2>验证码验证</h2>
    <div class="verify-content">
      <p class="verify-desc">请输入下方验证码</p>
      <!-- 图片验证码区域 -->
      <div class="code-display">
        <img
          :src="captchaUrl"
          alt="验证码"
          @click="refreshCaptcha"
          class="captcha-image"
        >
        <button class="refresh-btn" @click="refreshCaptcha">刷新</button>
      </div>
      <input
        type="text"
        class="code-input"
        v-model="inputCode"
        placeholder="请输入验证码"
        maxlength="6"
        @keyup.enter="handleVerify"
      >
      <div class="button-group">
        <button class="cancel-btn" @click="handleCancel">取消</button>
        <button class="confirm-btn" @click="handleVerify">确认</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast, showSuccessToast } from 'vant'

export default {
  name: 'verifyIndex',
  setup () {
    const router = useRouter()
    const route = useRoute()
    const inputCode = ref('')
    const captchaUrl = ref('/api/captcha?' + Date.now())

    // 从路由参数中获取注册信息
    const registerForm = ref({
      username: route.query.username || '',
      email: route.query.email || '',
      password: route.query.password || '',
      confirmPassword: route.query.confirmPassword || ''
    })

    // 刷新验证码
    const refreshCaptcha = () => {
      captchaUrl.value = '/api/captcha?' + Date.now()
      inputCode.value = '' // 清空输入
    }

    // 组件挂载时加载验证码图片
    onMounted(() => {
      // 图片会自动从 src 属性加载
    })

    // 处理验证
    const handleVerify = async () => {
      // 验证验证码
      if (!inputCode.value) {
        showToast('请输入验证码')
        return
      }

      // 调用后端注册接口（包含验证码验证）
      try {
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: registerForm.value.username,
            email: registerForm.value.email,
            password: registerForm.value.password,
            captcha: inputCode.value
          })
        })

        const result = await response.json()

        if (response.ok) {
          // 注册成功
          showSuccessToast('注册成功')
          router.push('/home')
        } else {
          showToast(result.message || '注册失败')
          refreshCaptcha() // 刷新验证码
        }
      } catch (error) {
        showToast('网络错误')
      }
    }

    // 处理取消
    const handleCancel = () => {
      router.push('/register')
    }

    // 处理返回按钮点击
    const handleBack = () => {
      router.push('/home')
    }

    return {
      inputCode,
      captchaUrl,
      handleVerify,
      handleCancel,
      handleBack,
      refreshCaptcha
    }
  }
}
</script>

<style scoped>
/* 验证码页面样式 */
.verify-container {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* 返回按钮样式 */
.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #2c3e50;
  z-index: 2;
}

.back-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 背景装饰 */
.verify-container::before {
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
.verify-container h2 {
  font-size: 32px;
  font-weight: 600;
  color: #2c3e50;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin-bottom: 30px;
  position: relative;
  z-index: 1;
}

/* 验证内容样式 */
.verify-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 400px;
  position: relative;
  z-index: 1;
  animation: formFadeIn 0.5s ease;
}

@keyframes formFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 验证描述 */
.verify-desc {
  margin-bottom: 20px;
  color: #7f8c8d;
  font-size: 16px;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 验证码显示区域 */
.code-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

/* 验证码图片 */
.captcha-image {
  width: 120px;
  height: 40px;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid #bdc3c7;
}

/* 刷新按钮 */
.refresh-btn {
  padding: 10px 16px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
}

.refresh-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
}

/* 验证码输入框 */
.code-input {
  width: 100%;
  padding: 15px 20px;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  font-size: 18px;
  text-align: center;
  letter-spacing: 4px;
  margin-bottom: 30px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  transition: all 0.3s ease;
}

.code-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

/* 按钮组 */
.button-group {
  display: flex;
  gap: 15px;
}

/* 按钮样式 */
.cancel-btn, .confirm-btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.cancel-btn {
  background: #f8f9fa;
  color: #7f8c8d;
  border: 1px solid #bdc3c7;
}

.cancel-btn:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.confirm-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

.confirm-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .verify-container {
    padding: 15px;
  }

  .verify-container h2 {
    font-size: 24px;
  }

  .verify-content {
    padding: 25px;
    margin: 0 10px;
  }

  .code-display {
    padding: 15px;
  }

  .captcha-image {
    width: 100px;
    height: 35px;
  }

  .refresh-btn {
    padding: 8px 12px;
    font-size: 12px;
  }

  .code-input {
    padding: 12px 16px;
    font-size: 16px;
  }

  .cancel-btn, .confirm-btn {
    padding: 12px;
    font-size: 14px;
  }
}

@media (min-width: 769px) {
  .verify-container {
    padding: 40px;
  }

  .verify-content {
    padding: 45px;
  }
}
</style>

<template>
  <div class="login-container">
    <!-- 返回按钮 -->
    <button class="back-btn" @click="handleBack">
      &larr; 返回
    </button>
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="loginForm.username" required>
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="loginForm.password" required>
      </div>
      <button type="submit" class="login-btn">登录</button>
      <p class="register-link">
        还没有账号?<router-link to="/register">去注册</router-link>
        <span class="forgot-password" @click="showForgotPasswordModal = true">忘记密码</span>
      </p>

      <!-- 忘记密码模态框 -->
      <div class="forgot-password-modal" v-if="showForgotPasswordModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>忘记密码</h3>
            <button class="modal-close" @click="showForgotPasswordModal = false">×</button>
          </div>
          <div class="modal-body" v-if="forgotPasswordStep === 1">
            <p>请选择验证方式</p>
            <div class="verify-options">
              <div class="verify-option" @click="selectedVerifyMethod = 'phone'; forgotPasswordStep = 2">
                <span class="verify-icon">📱</span>
                <span class="verify-text">手机号验证</span>
              </div>
              <div class="verify-option" @click="selectedVerifyMethod = 'email'; forgotPasswordStep = 2">
                <span class="verify-icon">📧</span>
                <span class="verify-text">邮箱验证</span>
              </div>
            </div>
          </div>
          <div class="modal-body" v-else-if="forgotPasswordStep === 2">
            <div class="form-group">
              <label v-if="selectedVerifyMethod === 'phone'">手机号</label>
              <label v-else>邮箱</label>
              <input
                type="text"
                v-model="forgotPasswordForm.contact"
                placeholder="请输入手机号/邮箱"
              >
            </div>
            <button type="button" class="verify-btn" @click="checkContact">下一步</button>
          </div>
          <div class="modal-body" v-else-if="forgotPasswordStep === 3">
            <div class="form-group">
              <label>验证码</label>
              <div class="code-input-container">
                <input type="text" v-model="forgotPasswordForm.code" placeholder="请输入验证码">
                <button type="button" class="send-code-btn" @click="sendCode" :disabled="countdown > 0">
                  {{ countdown > 0 ? `${countdown}秒后重发` : '发送验证码' }}
                </button>
              </div>
            </div>
            <button type="button" class="verify-btn" @click="verifyCode">验证</button>
          </div>
          <div class="modal-body" v-else-if="forgotPasswordStep === 4">
            <div class="form-group">
              <label>新密码</label>
              <input type="password" v-model="forgotPasswordForm.newPassword" placeholder="请输入新密码">
            </div>
            <div class="form-group">
              <label>确认新密码</label>
              <input type="password" v-model="forgotPasswordForm.confirmPassword" placeholder="请再次输入新密码">
            </div>
            <button type="button" class="verify-btn" @click="resetPassword">重置密码</button>
          </div>
          <div class="modal-footer">
            <button type="button" class="cancel-btn" @click="resetForgotPassword">返回</button>
          </div>
        </div>
      </div>
    </form>

  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showSuccessToast, showToast } from 'vant'
export default {
  name: 'loginIndex',
  setup () {
    const router = useRouter()
    const loginForm = ref({
      username: '',
      password: ''
    })

    // 忘记密码相关状态
    const showForgotPasswordModal = ref(false)
    const forgotPasswordStep = ref(1)
    const selectedVerifyMethod = ref('')
    const countdown = ref(0)
    let countdownTimer = null

    const forgotPasswordForm = ref({
      contact: '',
      code: '',
      newPassword: '',
      confirmPassword: ''
    })

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

    const handleLogin = () => {
      // 简单的表单验证
      if (!loginForm.value.username || !loginForm.value.password) {
        showToast('请输入用户名和密码')
        return
      }

      // 验证邮箱格式（如果输入的是邮箱）
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

      // 先检查本地存储中是否已存在用户信息
      let userInfo = null
      const storedUser = localStorage.getItem('userInfo')
      if (storedUser) {
        userInfo = JSON.parse(storedUser)
        // 更新用户名和邮箱
        userInfo.username = loginForm.value.username
        userInfo.email = emailRegex.test(loginForm.value.username) ? loginForm.value.username : `${loginForm.value.username}@example.com`
      } else {
        // 如果本地存储中没有用户信息，创建新的
        userInfo = {
          username: loginForm.value.username,
          email: emailRegex.test(loginForm.value.username) ? loginForm.value.username : `${loginForm.value.username}@example.com`
        }
      }

      // 保存用户信息到本地存储
      localStorage.setItem('userInfo', JSON.stringify(userInfo))

      // 显示登录成功提示
      showSuccessToast('登录成功')

      // 跳转到首页
      router.push('/home')
    }

    // 处理返回按钮点击
    const handleBack = () => {
      // 跳转到首页
      router.push('/home')
    }

    // 忘记密码相关函数
    const resetForgotPassword = () => {
      showForgotPasswordModal.value = false
      forgotPasswordStep.value = 1
      selectedVerifyMethod.value = ''
      forgotPasswordForm.value = {
        contact: '',
        code: '',
        newPassword: '',
        confirmPassword: ''
      }
      if (countdownTimer) {
        clearInterval(countdownTimer)
        countdown.value = 0
      }
    }

    const checkContact = () => {
      const contact = forgotPasswordForm.value.contact
      if (!contact) {
        showToast('请输入手机号/邮箱')
        return
      }

      // 检查手机号/邮箱是否已注册
      const storedUser = localStorage.getItem('userInfo')
      if (!storedUser) {
        showToast('当前账号不存在，请重新输入')
        return
      }

      const userInfo = JSON.parse(storedUser)
      let isRegistered = false

      if (selectedVerifyMethod.value === 'phone') {
        // 简单模拟手机号验证
        isRegistered = contact.length === 11
      } else {
        // 简单模拟邮箱验证
        const emailRegex = /^[^@]+@[^@]+\.[^@]+$/
        isRegistered = emailRegex.test(contact) && contact === userInfo.email
      }

      if (!isRegistered) {
        showToast(`当前${selectedVerifyMethod.value === 'phone' ? '手机号' : '邮箱'}并没有创建过账号，请重新输入`)
        return
      }

      // 进入验证码步骤
      forgotPasswordStep.value = 3
    }

    const sendCode = () => {
      // 模拟发送验证码
      showToast('验证码已发送')

      // 开始倒计时
      countdown.value = 60
      if (countdownTimer) {
        clearInterval(countdownTimer)
      }
      countdownTimer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
          clearInterval(countdownTimer)
        }
      }, 1000)
    }

    const verifyCode = () => {
      const code = forgotPasswordForm.value.code
      if (!code) {
        showToast('请输入验证码')
        return
      }

      // 简单模拟验证码验证
      if (code.length !== 6) {
        showToast('验证码错误')
        return
      }

      // 进入重置密码步骤
      forgotPasswordStep.value = 4
    }

    const resetPassword = () => {
      const { newPassword, confirmPassword } = forgotPasswordForm.value

      if (!newPassword || !confirmPassword) {
        showToast('请输入新密码和确认密码')
        return
      }

      if (newPassword !== confirmPassword) {
        showToast('两次输入的密码不一致')
        return
      }

      // 保存新密码到本地存储
      const storedUser = localStorage.getItem('userInfo')
      if (storedUser) {
        const userInfo = JSON.parse(storedUser)
        userInfo.password = newPassword
        localStorage.setItem('userInfo', JSON.stringify(userInfo))

        showToast('密码重置成功')
        resetForgotPassword()
      }
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
      loginForm,
      handleLogin,
      handleBack,
      // 忘记密码相关
      showForgotPasswordModal,
      forgotPasswordStep,
      selectedVerifyMethod,
      countdown,
      forgotPasswordForm,
      resetForgotPassword,
      checkContact,
      sendCode,
      verifyCode,
      resetPassword
    }
  }
}
</script>

<style>
/* 登录页面样式 */
.login-container {
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
  white-space: nowrap;
  min-width: 60px;
}

.back-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 背景装饰 */
.login-container::before {
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
.login-container h2 {
  font-size: 32px;
  font-weight: 600;
  color: #2c3e50;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin-bottom: 30px;
  position: relative;
  z-index: 1;
}

/* 表单样式 */
.login-container form {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 30px;
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

/* 表单组样式 */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: rgba(255, 255, 255, 0.8);
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
  background: white;
}

/* 登录按钮样式 */
.login-btn {
  width: 100%;
  padding: 14px;
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
  margin-top: 10px;
}

.login-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

.login-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

/* 注册链接样式 */
.register-link {
  text-align: center;
  margin-top: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 14px;
  color: #7f8c8d;
}

.register-link a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.register-link a:hover {
  color: #2980b9;
  text-decoration: underline;
}

/* 忘记密码链接样式 */
.forgot-password {
  margin-left: 20px;
  color: #3498db;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.forgot-password:hover {
  color: #2980b9;
  text-decoration: underline;
}

/* 忘记密码模态框样式 */
.forgot-password-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.forgot-password-modal .modal-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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

.forgot-password-modal .modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.forgot-password-modal .modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
}

.forgot-password-modal .modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.forgot-password-modal .modal-close:hover {
  background: #f5f7fa;
  color: #2c3e50;
}

.forgot-password-modal .modal-body {
  margin-bottom: 20px;
}

.forgot-password-modal .modal-body p {
  margin-bottom: 20px;
  color: #2c3e50;
  font-size: 16px;
}

/* 验证方式选项 */
.verify-options {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.verify-option {
  display: flex;
  align-items: center;
  padding: 15px;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f5f7fa;
}

.verify-option:hover {
  border-color: #3498db;
  background: #e3f2fd;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

.verify-icon {
  font-size: 24px;
  margin-right: 15px;
}

.verify-text {
  font-size: 16px;
  color: #2c3e50;
}

/* 验证码输入容器 */
.code-input-container {
  display: flex;
  gap: 10px;
}

.code-input-container input {
  flex: 1;
}

.send-code-btn {
  padding: 0 16px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.send-code-btn:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.send-code-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

/* 验证按钮 */
.verify-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
  margin-top: 10px;
}

.verify-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

/* 模态框底部 */
.forgot-password-modal .modal-footer {
  display: flex;
  justify-content: flex-end;
}

.cancel-btn {
  padding: 8px 16px;
  background: #f5f7fa;
  color: #2c3e50;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.cancel-btn:hover {
  background: #e3f2fd;
  border-color: #3498db;
  color: #3498db;
}

/* 深色主题下的模态框样式 */
.dark-theme .forgot-password-modal .modal-content {
  background: #2c2c2c;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.dark-theme .forgot-password-modal .modal-header h3 {
  color: #e0e0e0;
}

.dark-theme .forgot-password-modal .modal-close {
  color: #999;
}

.dark-theme .forgot-password-modal .modal-close:hover {
  background: #3a3a3a;
  color: #e0e0e0;
}

.dark-theme .forgot-password-modal .modal-body p {
  color: #e0e0e0;
}

.dark-theme .verify-option {
  background: #3a3a3a;
  border-color: #444;
}

.dark-theme .verify-option:hover {
  border-color: #3498db;
  background: #444;
}

.dark-theme .verify-text {
  color: #e0e0e0;
}

.dark-theme .cancel-btn {
  background: #3a3a3a;
  border-color: #444;
  color: #e0e0e0;
}

.dark-theme .cancel-btn:hover {
  background: #444;
  border-color: #3498db;
  color: #3498db;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    padding: 15px;
  }

  .login-container h2 {
    font-size: 24px;
  }

  .login-container form {
    padding: 20px;
    margin: 0 10px;
  }

  .form-group input {
    padding: 10px 14px;
    font-size: 14px;
  }

  .login-btn {
    padding: 12px;
    font-size: 14px;
  }
}

@media (min-width: 769px) {
  .login-container {
    padding: 40px;
  }

  .login-container form {
    padding: 35px;
  }
}

/* 深色主题 */
.dark-theme .login-container {
  background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
}

.dark-theme .back-btn {
  background: rgba(58, 58, 58, 0.8);
  border-color: #444;
  color: #e0e0e0;
}

.dark-theme .back-btn:hover {
  background: #444;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.dark-theme .login-container h2 {
  color: #e0e0e0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.dark-theme .login-container form {
  background: rgba(44, 44, 44, 0.95);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.dark-theme .form-group label {
  color: #e0e0e0;
}

.dark-theme .form-group input {
  background: #3a3a3a;
  border-color: #444;
  color: #e0e0e0;
}

.dark-theme .form-group input:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
  background: #444;
}

.dark-theme .register-link {
  color: #999;
}

.dark-theme .register-link a {
  color: #3498db;
}

.dark-theme .register-link a:hover {
  color: #2980b9;
}

/* 字体切换 */
[data-font="sans-serif"] .login-container h2,
[data-font="sans-serif"] .form-group label,
[data-font="sans-serif"] .form-group input,
[data-font="sans-serif"] .login-btn,
[data-font="sans-serif"] .register-link {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

[data-font="serif"] .login-container h2,
[data-font="serif"] .form-group label,
[data-font="serif"] .form-group input,
[data-font="serif"] .login-btn,
[data-font="serif"] .register-link {
  font-family: 'Times New Roman', serif;
}

[data-font="monospace"] .login-container h2,
[data-font="monospace"] .form-group label,
[data-font="monospace"] .form-group input,
[data-font="monospace"] .login-btn,
[data-font="monospace"] .register-link {
  font-family: 'Courier New', monospace;
}

</style>

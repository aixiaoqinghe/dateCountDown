<template>
  <div class="register-container">
    <!-- 返回按钮 -->
    <button class="back-btn" @click="handleBack">
      &larr; 返回
    </button>
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="registerForm.username" required>
      </div>
      <div class="form-group">
        <label for="email">邮箱</label>
        <input type="email" id="email" v-model="registerForm.email" required>
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="registerForm.password" required>
      </div>
      <div class="form-group">
        <label for="confirmPassword">确认密码</label>
        <input type="password" id="confirmPassword" v-model="registerForm.confirmPassword" required>
      </div>
      <button type="submit" class="register-btn">注册</button>
      <p class="login-link">
        已有账号？<router-link to="/login">去登录</router-link>
      </p>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
export default {
  name: 'registerIndex',
  setup () {
    const router = useRouter()
    const registerForm = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const handleRegister = () => {
      // 简单的表单验证
      if (!registerForm.value.username || !registerForm.value.email || !registerForm.value.password || !registerForm.value.confirmPassword) {
        showToast('请填写完整的注册信息')
        return
      }

      // 验证邮箱格式
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
      if (!emailRegex.test(registerForm.value.email)) {
        showToast('邮箱格式不合法')
        return
      }

      // 验证密码是否匹配
      if (registerForm.value.password !== registerForm.value.confirmPassword) {
        showToast('两次输入的密码不同')
        return
      }

      // 跳转到验证码页面，并传递注册信息
      router.push({
        path: '/verify',
        query: {
          username: registerForm.value.username,
          email: registerForm.value.email,
          password: registerForm.value.password,
          confirmPassword: registerForm.value.confirmPassword
        }
      })
    }

    // 处理返回按钮点击
    const handleBack = () => {
      // 跳转到个人中心页面（未登录状态）
      router.push('/home/mine')
    }

    return {
      registerForm,
      handleRegister,
      handleBack
    }
  }
}
</script>

<style scoped>
/* 注册页面样式 */
.register-container {
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
.register-container::before {
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
.register-container h2 {
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
.register-container form {
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
  border-color: #27ae60;
  box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1);
  background: white;
}

/* 注册按钮样式 */
.register-btn {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  background: linear-gradient(135deg, #27ae60, #229954);
  color: white;
  box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin-top: 10px;
}

.register-btn:hover {
  background: linear-gradient(135deg, #229954, #1e8449);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(39, 174, 96, 0.4);
}

.register-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
}

/* 登录链接样式 */
.login-link {
  text-align: center;
  margin-top: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 14px;
  color: #7f8c8d;
}

.login-link a {
  color: #27ae60;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.login-link a:hover {
  color: #229954;
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-container {
    padding: 15px;
  }

  .register-container h2 {
    font-size: 24px;
  }

  .register-container form {
    padding: 20px;
    margin: 0 10px;
  }

  .form-group input {
    padding: 10px 14px;
    font-size: 14px;
  }

  .register-btn {
    padding: 12px;
    font-size: 14px;
  }
}

@media (min-width: 769px) {
  .register-container {
    padding: 40px;
  }

  .register-container form {
    padding: 35px;
  }
}

/* 验证码弹窗样式 */
.code-content {
  padding: 10px 0;
}

.code-desc {
  margin-bottom: 15px;
  color: #7f8c8d;
  font-size: 14px;
  text-align: center;
}

.code-display {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.code-text {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 4px;
  color: #2c3e50;
  font-family: 'Courier New', monospace;
}

.code-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  font-size: 16px;
  text-align: center;
  letter-spacing: 4px;
}

.code-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

/* 验证码弹窗样式 */
.popup-content {
  background: white;
  border-radius: 12px;
  padding: 20px;
  position: relative;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.popup-header h3 {
  margin: 0;
  font-size: 18px;
  color: #2c3e50;
  font-weight: 600;
}

.close-btn {
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

.close-btn:hover {
  background: #f8f9fa;
  color: #2c3e50;
}

.popup-footer {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.cancel-btn, .confirm-btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.cancel-btn {
  background: #f8f9fa;
  color: #7f8c8d;
  border: 1px solid #bdc3c7;
}

.cancel-btn:hover {
  background: #e9ecef;
}

.confirm-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
}
</style>

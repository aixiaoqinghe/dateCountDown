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
      </p>
    </form>

  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
export default {
  name: 'loginIndex',
  setup () {
    const router = useRouter()
    const loginForm = ref({
      username: '',
      password: ''
    })
    const handleLogin = () => {
      // 简单的表单验证
      if (!loginForm.value.username || !loginForm.value.password) {
        showToast('请输入用户名和密码')
        return
      }

      // 验证邮箱格式（如果输入的是邮箱）
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (emailRegex.test(loginForm.value.username)) {
        // 如果输入的是邮箱，使用邮箱作为用户名
        // 模拟登录成功（调用后端API）
        const userInfo = {
          username: loginForm.value.username,
          email: loginForm.value.username
        }
        // 保留用户信息到本地存储
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
      } else {
        // 如果输入的是用户名，使用用户名生成邮箱
        // 模拟登录成功（调用后端API）
        const userInfo = {
          username: loginForm.value.username,
          email: `${loginForm.value.username}@example.com`
        }
        // 保留用户信息到本地存储
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
      }

      // 显示登录成功提示
      showToast('登录成功')

      // 跳转到个人中心页面
      router.push('home/mine')
    }

    // 处理返回按钮点击
    const handleBack = () => {
      // 跳转到个人中心页面（未登录状态）
      router.push('/home/mine')
    }

    return {
      loginForm,
      handleLogin,
      handleBack
    }
  }
}
</script>

<style scoped>
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
</style>

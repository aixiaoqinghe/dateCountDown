<template>
  <div class="verification-code">
    <div class="code-content">
      <p class="code-desc">请输入下方验证码</p>
      <div class="code-display">
        <span class="code-text">{{ code }}</span>
        <button class="refresh-btn" @click="refreshCode">刷新</button>
      </div>
      <input
        type="text"
        class="code-input"
        v-model="inputCode"
        placeholder="请输入验证码"
        maxlength="6"
      >
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'VerificationCode',
  emits: ['verify'],
  setup (props, { emit }) {
    const code = ref('')
    const inputCode = ref('')

    // 生成随机验证码
    const generateCode = () => {
      const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      let result = ''
      for (let i = 0; i < 6; i++) {
        result += chars[Math.floor(Math.random() * chars.length)]
      }
      code.value = result
    }

    // 刷新验证码
    const refreshCode = () => {
      generateCode()
    }

    // 验证验证码
    const verifyCode = () => {
      if (!inputCode.value) {
        return false
      }
      return inputCode.value.toUpperCase() === code.value
    }

    onMounted(() => {
      generateCode()
    })

    return {
      code,
      inputCode,
      refreshCode,
      verifyCode
    }
  }
}
</script>

<style scoped>
.verification-code {
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
  justify-content: space-between;
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

.refresh-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: #2980b9;
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
</style>

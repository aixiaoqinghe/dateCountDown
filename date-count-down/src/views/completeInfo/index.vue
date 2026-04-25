<template>
  <div class="complete-info-container">
    <!-- 返回按钮 -->
    <button class="back-btn" @click="handleBack">
      &larr; 返回
    </button>
    <h2>完善个人信息</h2>
    <div class="info-content">
      <!-- 头像选择 -->
      <div class="avatar-section">
        <h3>选择头像</h3>
        <div class="avatar-container">
          <div
            v-for="(avatar, index) in avatars"
            :key="index"
            class="avatar-item"
            :class="{ active: selectedAvatar === index }"
            @click="selectAvatar(index)"
          >
            <img :src="avatar" alt="头像" />
          </div>
          <!-- 上传头像按钮 -->
          <div class="avatar-item upload-avatar" @click="triggerFileInput">
            <input
              type="file"
              ref="fileInput"
              style="display: none"
              accept="image/*"
              @change="handleImageUpload"
            >
            <div class="upload-icon">+</div>
            <div class="upload-text">上传</div>
          </div>
        </div>
      </div>

      <!-- 昵称输入 -->
      <div class="form-group">
        <label for="nickname">昵称</label>
        <input
          type="text"
          id="nickname"
          v-model="userInfo.nickname"
          placeholder="请输入昵称"
          @blur="checkNickname"
        >
        <p v-if="nicknameError" class="error-message">{{ nicknameError }}</p>
      </div>

      <!-- 手机号绑定 -->
      <div class="form-group">
        <label for="phone">手机号</label>
        <div class="phone-input-container">
          <input
            type="tel"
            id="phone"
            v-model="userInfo.phone"
            placeholder="请输入手机号"
            maxlength="11"
          >
          <button
            class="code-btn"
            :disabled="isSendingCode || !isPhoneValid"
            @click="sendVerificationCode"
          >
            {{ codeBtnText }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="verificationCode">验证码</label>
        <input
          type="text"
          id="verificationCode"
          v-model="userInfo.verificationCode"
          placeholder="请输入验证码"
          maxlength="6"
        >
      </div>

      <button class="submit-btn" @click="submitInfo">完成</button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showSuccessToast } from 'vant'

export default {
  name: 'completeInfoIndex',
  setup () {
    const router = useRouter()
    const fileInput = ref(null)

    // 从本地存储获取用户信息
    const userInfo = ref({
      nickname: '',
      phone: '',
      verificationCode: '',
      avatar: ''
    })

    // 头像选项
    const avatars = ref([
      'https://a0ai.marscode.cn/api/ide/v1/text_to_image?prompt=user%20avatar%201%20simple%20flat%20design&image_size=square',
      'https://a0ai.marscode.cn/api/ide/v1/text_to_image?prompt=user%20avatar%202%20simple%20flat%20design&image_size=square',
      'https://a0ai.marscode.cn/api/ide/v1/text_to_image?prompt=user%20avatar%203%20simple%20flat%20design&image_size=square',
      'https://a0ai.marscode.cn/api/ide/v1/text_to_image?prompt=user%20avatar%204%20simple%20flat%20design&image_size=square',
      'https://a0ai.marscode.cn/api/ide/v1/text_to_image?prompt=user%20avatar%205%20simple%20flat%20design&image_size=square',
      'https://a0ai.marscode.cn/api/ide/v1/text_to_image?prompt=user%20avatar%206%20simple%20flat%20design&image_size=square'
    ])

    const selectedAvatar = ref(0)
    const nicknameError = ref('')
    const isSendingCode = ref(false)
    const codeBtnText = ref('获取验证码')
    const countdown = ref(60)

    // 模拟已存在的昵称列表
    const existingNicknames = ref(['admin', 'user123', 'test', 'demo'])

    // 计算手机号是否有效
    const isPhoneValid = computed(() => {
      const phoneRegex = /^1[3-9]\d{9}$/
      return phoneRegex.test(userInfo.value.phone)
    })

    // 选择头像
    const selectAvatar = (index) => {
      selectedAvatar.value = index
      userInfo.value.avatar = avatars.value[index]
    }

    // 触发文件选择
    const triggerFileInput = () => {
      fileInput.value.click()
    }

    // 处理图片上传
    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        // 检查文件类型
        if (!file.type.startsWith('image/')) {
          showToast('请上传图片文件')
          return
        }

        // 检查文件大小（限制为2MB）
        if (file.size > 2 * 1024 * 1024) {
          showToast('图片大小不能超过2MB')
          return
        }

        // 创建FileReader读取文件
        const reader = new FileReader()
        reader.onload = (e) => {
          // 将图片转换为base64格式存储
          userInfo.value.avatar = e.target.result
          // 清除选中的默认头像
          selectedAvatar.value = -1
        }
        reader.readAsDataURL(file)
      }
    }

    // 检查昵称是否已存在
    const checkNickname = () => {
      const nickname = userInfo.value.nickname.trim()
      if (nickname) {
        if (existingNicknames.value.includes(nickname)) {
          nicknameError.value = '该昵称已存在，请重新输入'
        } else {
          nicknameError.value = ''
        }
      } else {
        nicknameError.value = ''
      }
    }

    // 发送验证码
    const sendVerificationCode = () => {
      if (!isPhoneValid.value) {
        showToast('请输入正确的手机号')
        return
      }

      // 模拟发送验证码
      isSendingCode.value = true
      codeBtnText.value = `${countdown.value}秒后重新获取`

      const timer = setInterval(() => {
        countdown.value--
        codeBtnText.value = `${countdown.value}秒后重新获取`

        if (countdown.value <= 0) {
          clearInterval(timer)
          isSendingCode.value = false
          codeBtnText.value = '获取验证码'
          countdown.value = 60
        }
      }, 1000)

      showToast('验证码已发送')
    }

    // 提交信息
    const submitInfo = () => {
      // 验证表单
      if (!userInfo.value.avatar) {
        showToast('请选择头像')
        return
      }

      if (!userInfo.value.nickname) {
        // 如果用户不输入昵称，默认为"XXX用户"，其中XXX是用户的id号
        const userId = Math.floor(Math.random() * 10000)
        userInfo.value.nickname = `${userId}用户`
      } else if (nicknameError.value) {
        showToast(nicknameError.value)
        return
      }

      if (!userInfo.value.phone) {
        showToast('请输入手机号')
        return
      }

      if (!isPhoneValid.value) {
        showToast('请输入正确的手机号')
        return
      }

      if (!userInfo.value.verificationCode) {
        showToast('请输入验证码')
        return
      }

      // 模拟验证验证码
      if (userInfo.value.verificationCode !== '123456') {
        showToast('验证码错误')
        return
      }

      // 获取当前用户信息
      const currentUser = JSON.parse(localStorage.getItem('userInfo') || '{}')

      // 合并用户信息
      const updatedUser = {
        ...currentUser,
        ...userInfo.value,
        avatar: avatars.value[selectedAvatar.value]
      }

      // 保存更新后的用户信息
      localStorage.setItem('userInfo', JSON.stringify(updatedUser))

      // 显示成功提示
      showSuccessToast('信息完善成功')

      // 跳转到首页
      router.push('/home')
    }

    // 处理返回按钮点击
    const handleBack = () => {
      // 跳转到首页
      router.push('/home')
    }

    // 组件挂载时初始化
    onMounted(() => {
      // 默认选择第一个头像
      userInfo.value.avatar = avatars.value[0]
    })

    return {
      userInfo,
      avatars,
      selectedAvatar,
      nicknameError,
      isSendingCode,
      codeBtnText,
      isPhoneValid,
      fileInput,
      selectAvatar,
      triggerFileInput,
      handleImageUpload,
      checkNickname,
      sendVerificationCode,
      submitInfo,
      handleBack
    }
  }
}
</script>

<style scoped>
/* 完善信息页面样式 */
.complete-info-container {
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
.complete-info-container::before {
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
.complete-info-container h2 {
  font-size: 32px;
  font-weight: 600;
  color: #2c3e50;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin-bottom: 30px;
  position: relative;
  z-index: 1;
}

/* 信息内容样式 */
.info-content {
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

/* 头像部分 */
.avatar-section {
  margin-bottom: 30px;
}

.avatar-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 15px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.avatar-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.avatar-item {
  width: 100%;
  aspect-ratio: 1;
  border: 2px solid #e0e0e0;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.avatar-item.active {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}

.avatar-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 上传头像按钮样式 */
.avatar-item.upload-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(245, 247, 250, 0.8);
  border: 2px dashed #bdc3c7;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar-item.upload-avatar:hover {
  background: rgba(245, 247, 250, 1);
  border-color: #3498db;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.upload-icon {
  font-size: 24px;
  font-weight: bold;
  color: #95a5a6;
  margin-bottom: 5px;
}

.upload-text {
  font-size: 12px;
  color: #7f8c8d;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.avatar-item.upload-avatar.active {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
  background: rgba(245, 247, 250, 1);
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

/* 错误信息 */
.error-message {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 手机号输入容器 */
.phone-input-container {
  display: flex;
  gap: 10px;
}

.phone-input-container input {
  flex: 1;
}

/* 验证码按钮 */
.code-btn {
  padding: 0 20px;
  border: 1px solid #3498db;
  border-radius: 8px;
  background: white;
  color: #3498db;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.code-btn:hover:not(:disabled) {
  background: #3498db;
  color: white;
}

.code-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 提交按钮 */
.submit-btn {
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
  margin-top: 20px;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

.submit-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .complete-info-container {
    padding: 15px;
  }

  .complete-info-container h2 {
    font-size: 24px;
  }

  .info-content {
    padding: 20px;
    margin: 0 10px;
  }

  .form-group input {
    padding: 10px 14px;
    font-size: 14px;
  }

  .submit-btn {
    padding: 12px;
    font-size: 14px;
  }
}

@media (min-width: 769px) {
  .complete-info-container {
    padding: 40px;
  }

  .info-content {
    padding: 35px;
  }
}
</style>

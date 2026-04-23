<template>
  <div class="mine-container">
    <h2>个人中心</h2>
    <!-- 登录状态显示 -->
    <div v-if="userInfo" class="user-info">
      <!-- 用户头像和基本信息 -->
      <div class="user-header">
        <div class="avatar-container">
          <img :src="userInfo.avatar || defaultAvatar" alt="用户头像" class="user-avatar" />
        </div>
        <div class="user-basic-info">
          <div class="name-signature">
            <h3>{{ userInfo.nickname || userInfo.username }}</h3>
            <div class="signature-container">
              <p class="user-signature">{{ userInfo.signature || '暂无签名' }}</p>
              <button class="edit-signature-btn" @click="toggleEditSignature">
                <span class="edit-icon">✏️</span>
              </button>
            </div>
          </div>
          <div class="id-email-qrcode">
            <div class="id-email">
              <p class="user-id">ID: {{ userId }}</p>
              <p class="user-email">{{ userInfo.email }}</p>
            </div>
            <div class="qrcode-small" @click="toggleQrcodeModal">
              <img :src="qrcodeUrl" alt="个人二维码" class="qrcode-mini" />
            </div>
          </div>
        </div>
      </div>

      <!-- 签名编辑弹窗 -->
      <div v-if="isEditingSignature" class="signature-edit-modal">
        <div class="modal-content">
          <h4>编辑个性化签名</h4>
          <textarea
            v-model="editSignature"
            placeholder="请输入个性化签名"
            class="signature-textarea"
            maxlength="50"
          ></textarea>
          <div class="edit-actions">
            <button @click="saveSignature" class="save-btn">保存</button>
            <button @click="cancelEditSignature" class="cancel-btn">取消</button>
          </div>
        </div>
      </div>

      <!-- 二维码弹窗 -->
      <div v-if="showQrcodeModal" class="qrcode-modal">
        <div class="modal-content">
          <h4>个人二维码</h4>
          <div class="qrcode-large-container">
            <img :src="qrcodeUrl" alt="个人二维码" class="qrcode-large" />
            <p class="qrcode-tip">扫描二维码添加好友</p>
          </div>
          <button @click="closeQrcodeModal" class="close-btn">关闭</button>
        </div>
      </div>

      <!-- 修改密码弹窗 -->
      <div v-if="showChangePasswordModal" class="change-password-modal">
        <div class="modal-content">
          <h4>修改密码</h4>
          <div class="form-group">
            <label for="oldPassword">旧密码</label>
            <input type="password" id="oldPassword" v-model="passwordForm.oldPassword" placeholder="请输入旧密码" />
          </div>
          <div class="form-group">
            <label for="newPassword">新密码</label>
            <input type="password" id="newPassword" v-model="passwordForm.newPassword" placeholder="请输入新密码" />
          </div>
          <div class="form-group">
            <label for="confirmPassword">确认新密码</label>
            <input type="password" id="confirmPassword" v-model="passwordForm.confirmPassword" placeholder="请确认新密码" />
          </div>
          <div class="edit-actions">
            <button @click="savePassword" class="save-btn">保存</button>
            <button @click="closeChangePasswordModal" class="cancel-btn">取消</button>
          </div>
        </div>
      </div>

      <!-- 修改个人资料弹窗 -->
      <div v-if="showEditProfileModal" class="edit-profile-modal">
        <div class="modal-content">
          <h4>修改个人资料</h4>
          <div class="form-group">
            <label for="editNickname">昵称</label>
            <input type="text" id="editNickname" v-model="editProfileForm.nickname" placeholder="请输入昵称" />
          </div>
          <div class="form-group">
            <label for="editSignature">签名</label>
            <textarea id="editSignature" v-model="editProfileForm.signature" placeholder="请输入签名" class="signature-textarea" maxlength="50"></textarea>
          </div>
          <div class="edit-actions">
            <button @click="saveProfile" class="save-btn">保存</button>
            <button @click="closeEditProfileModal" class="cancel-btn">取消</button>
          </div>
        </div>
      </div>

      <!-- 关于应用弹窗 -->
      <div v-if="showAboutModal" class="about-modal">
        <div class="modal-content">
          <h4>关于应用</h4>
          <div class="about-content">
            <p>应用名称：日期倒计时</p>
            <p>版本：1.0.0</p>
            <p>描述：一个简单实用的日期倒计时应用</p>
            <p>开发者：Date Countdown Team</p>
          </div>
          <button @click="closeAboutModal" class="close-btn">关闭</button>
        </div>
      </div>

      <!-- 功能列表 -->
      <div class="feature-list">
        <div class="feature-section">
          <h4 class="section-title">账户设置</h4>
          <div class="feature-item" @click="toggleChangePasswordModal">
            <span class="feature-icon">🔐</span>
            <span class="feature-name">修改密码</span>
            <span class="feature-arrow">›</span>
          </div>
          <div class="feature-item" @click="toggleEditProfileModal">
            <span class="feature-icon">📝</span>
            <span class="feature-name">修改个人资料</span>
            <span class="feature-arrow">›</span>
          </div>
        </div>

        <div class="feature-section">
          <h4 class="section-title">其他</h4>
          <div class="feature-item" @click="showAbout">
            <span class="feature-icon">ℹ️</span>
            <span class="feature-name">关于应用</span>
            <span class="feature-arrow">›</span>
          </div>
        </div>
      </div>

      <button @click="logout" class="logout-btn">退出登录</button>
    </div>
    <!-- 未登录状态显示 -->
    <div v-else class="login-prompt">
      <p>请先登录</p>
      <router-link to="/login" class="login-btn">去登录</router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
export default {
  name: 'homeMyself',
  setup () {
    const router = useRouter()
    const userInfo = ref(null)
    const isEditingSignature = ref(false)
    const showQrcodeModal = ref(false)
    const showChangePasswordModal = ref(false)
    const showEditProfileModal = ref(false)
    const showAboutModal = ref(false)
    const editSignature = ref('')
    const defaultAvatar = 'https://a0ai.marscode.cn/api/ide/v1/text_to_image?prompt=default%20user%20avatar%20simple%20flat%20design&image_size=square'

    // 密码修改表单
    const passwordForm = ref({
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    })

    // 个人资料修改表单
    const editProfileForm = ref({
      nickname: '',
      signature: ''
    })

    // 生成用户ID（基于用户名和邮箱的简单哈希）
    const userId = computed(() => {
      if (!userInfo.value) return ''
      const str = userInfo.value.username + userInfo.value.email
      let hash = 0
      for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i)
        hash = ((hash << 5) - hash) + char
        hash = hash & hash
      }
      return Math.abs(hash).toString().substring(0, 8)
    })

    // 生成二维码URL（使用在线API）
    const qrcodeUrl = computed(() => {
      if (!userInfo.value) return ''
      const userData = `用户: ${userInfo.value.nickname || userInfo.value.username}\nID: ${userId.value}\n邮箱: ${userInfo.value.email}`
      const encodedData = encodeURIComponent(userData)
      return `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodedData}`
    })

    // 检查登录状态
    const checkLoginStatus = () => {
      const storedUser = localStorage.getItem('userInfo')
      if (storedUser) {
        try {
          // 有用户信息，已登录
          userInfo.value = JSON.parse(storedUser)
        } catch (error) {
          console.error('解析用户信息失败:', error)
          userInfo.value = null
        }
      } else {
        // 无用户信息，未登录，显示登录提示
        userInfo.value = null
      }
    }

    const toggleEditSignature = function () {
      if (userInfo.value) {
        isEditingSignature.value = true
        editSignature.value = userInfo.value.signature || ''
      }
    }

    // 保存签名
    const saveSignature = function () {
      if (userInfo.value) {
        userInfo.value.signature = editSignature.value.trim()
        // 更新本地存储
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
        isEditingSignature.value = false
      }
    }

    // 取消编辑签名
    const cancelEditSignature = function () {
      isEditingSignature.value = false
      editSignature.value = ''
    }

    // 切换二维码弹窗
    const toggleQrcodeModal = function () {
      if (userInfo.value) {
        showQrcodeModal.value = true
      }
    }

    // 关闭二维码弹窗
    const closeQrcodeModal = function () {
      showQrcodeModal.value = false
    }

    // 切换修改密码弹窗
    const toggleChangePasswordModal = function () {
      if (userInfo.value) {
        showChangePasswordModal.value = true
        passwordForm.value = {
          oldPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
      }
    }

    // 关闭修改密码弹窗
    const closeChangePasswordModal = function () {
      showChangePasswordModal.value = false
    }

    // 保存密码修改
    const savePassword = function () {
      // 简单验证
      if (!passwordForm.value.oldPassword) {
        alert('请输入旧密码')
        return
      }
      if (!passwordForm.value.newPassword) {
        alert('请输入新密码')
        return
      }
      if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
        alert('两次输入的密码不一致')
        return
      }
      // 模拟密码修改
      alert('密码修改成功')
      showChangePasswordModal.value = false
    }

    // 切换修改个人资料弹窗
    const toggleEditProfileModal = function () {
      if (userInfo.value) {
        showEditProfileModal.value = true
        editProfileForm.value = {
          nickname: userInfo.value.nickname || '',
          signature: userInfo.value.signature || ''
        }
      }
    }

    // 关闭修改个人资料弹窗
    const closeEditProfileModal = function () {
      showEditProfileModal.value = false
    }

    // 保存个人资料修改
    const saveProfile = function () {
      if (userInfo.value) {
        // 更新用户信息
        userInfo.value.nickname = editProfileForm.value.nickname.trim() || userInfo.value.nickname
        userInfo.value.signature = editProfileForm.value.signature.trim()
        // 更新本地存储
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
        alert('个人资料修改成功')
        showEditProfileModal.value = false
      }
    }

    // 显示关于应用
    const showAbout = function () {
      showAboutModal.value = true
    }

    // 关闭关于应用弹窗
    const closeAboutModal = function () {
      showAboutModal.value = false
    }

    // 退出登录
    const logout = function () {
      // 清除本地存储的用户信息
      localStorage.removeItem('userInfo')
      // 跳转到登录页面
      router.push('/login')
    }

    // 组件挂载时检查登录状态
    onMounted(() => {
      checkLoginStatus()
    })

    return {
      userInfo,
      defaultAvatar,
      userId,
      qrcodeUrl,
      isEditingSignature,
      editSignature,
      showQrcodeModal,
      showChangePasswordModal,
      showEditProfileModal,
      showAboutModal,
      passwordForm,
      editProfileForm,
      toggleEditSignature,
      saveSignature,
      cancelEditSignature,
      toggleQrcodeModal,
      closeQrcodeModal,
      toggleChangePasswordModal,
      closeChangePasswordModal,
      savePassword,
      toggleEditProfileModal,
      closeEditProfileModal,
      saveProfile,
      showAbout,
      closeAboutModal,
      logout
    }
  }
}
</script>

<style scoped>
@import '../../styles/home.css';

/* 个人中心页面特有样式 */
.mine-container {
  padding: 20px;
  min-height: 70vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.mine-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: moveBackground 20s linear infinite;
  z-index: -1;
}

@keyframes moveBackground {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.mine-container h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 32px;
  font-weight: 600;
  color: #2c3e50;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  position: relative;
  z-index: 1;
}

.user-info {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  margin: 0 auto;
  max-width: 400px;
  position: relative;
  z-index: 1;
}

/* 用户头部信息 */
.user-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.avatar-container {
  margin-right: 20px;
}

.user-avatar {
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #3498db;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.user-basic-info {
  flex: 1;
  text-align: left;
}

.name-signature {
  margin-bottom: 10px;
}

.user-basic-info h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 5px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.signature-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-signature {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  flex: 1;
}

.edit-signature-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.6;
}

.edit-signature-btn:hover {
  background: rgba(52, 152, 219, 0.1);
  opacity: 1;
}

.edit-icon {
  font-size: 14px;
}

.user-id {
  font-size: 14px;
  color: #95a5a6;
  margin-bottom: 5px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.user-email {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ID、邮箱和二维码布局 */
.id-email-qrcode {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.id-email {
  flex: 1;
}

/* 二维码样式 */
.qrcode-small {
  display: inline-block;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  padding: 4px;
  border-radius: 4px;
  background: white;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.qrcode-small:hover {
  background: #f8f9fa;
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.qrcode-mini {
  width: 24px;
  height: 24px;
  border-radius: 2px;
  background: white;
  padding: 2px;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05);
}

/* 签名编辑弹窗 */
.signature-edit-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
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

.modal-content h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
}

.signature-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  resize: vertical;
  min-height: 80px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.signature-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
  background: white;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}

.save-btn, .cancel-btn {
  padding: 8px 16px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.save-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
}

.save-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-1px);
}

.cancel-btn {
  background: #ecf0f1;
  color: #2c3e50;
}

.cancel-btn:hover {
  background: #d5dbdb;
  transform: translateY(-1px);
}

/* 二维码弹窗 */
.qrcode-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.qrcode-large-container {
  text-align: center;
  margin-bottom: 20px;
}

.qrcode-large {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.qrcode-tip {
  margin-top: 12px;
  font-size: 14px;
  color: #7f8c8d;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.close-btn {
  width: 100%;
  padding: 10px;
  background: #ecf0f1;
  color: #2c3e50;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.close-btn:hover {
  background: #d5dbdb;
  transform: translateY(-1px);
}

/* 功能列表样式 */
.feature-list {
  margin: 30px 0;
}

.feature-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #95a5a6;
  margin-bottom: 10px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding-left: 10px;
}

.feature-item {
  display: flex;
  align-items: center;
  padding: 12px 10px;
  background: white;
  border-radius: 8px;
  margin-bottom: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-item:hover {
  background: #f8f9fa;
  transform: translateX(4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 18px;
  margin-right: 12px;
  width: 24px;
  text-align: center;
}

.feature-name {
  flex: 1;
  font-size: 14px;
  color: #2c3e50;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.feature-arrow {
  font-size: 18px;
  color: #bdc3c7;
  font-weight: 300;
}

/* 表单样式 */
.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 6px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #bdc3c7;
  border-radius: 6px;
  font-size: 14px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-sizing: border-box;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

/* 关于应用内容 */
.about-content {
  margin-bottom: 20px;
}

.about-content p {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 8px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
}

/* 退出登录按钮 */
.logout-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
  margin-top: 20px;
}

.logout-btn:hover {
  background: linear-gradient(135deg, #c0392b, #a93226);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(231, 76, 60, 0.4);
}

/* 未登录状态 */
.login-prompt {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 40px 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  text-align: center;
  margin: 0 auto;
  max-width: 400px;
  position: relative;
  z-index: 1;
}

.login-prompt p {
  font-size: 18px;
  color: #7f8c8d;
  margin-bottom: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-btn {
  display: inline-block;
  padding: 12px 24px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.login-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f618d);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .mine-container h2 {
    font-size: 24px;
  }

  .user-info,
  .login-prompt {
    padding: 20px;
    margin: 0 10px;
  }

  .user-info h3 {
    font-size: 20px;
  }

  .logout-btn,
  .login-btn {
    padding: 10px 20px;
    font-size: 14px;
  }

  .feature-item {
    padding: 10px;
  }

  .feature-icon {
    font-size: 16px;
  }

  .feature-name {
    font-size: 13px;
  }
}
</style>

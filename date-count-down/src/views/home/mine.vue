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
              <span class="signature-icon" @click="toggleEditSignatureModal">✏️</span>
              <span class="user-signature">{{ userInfo.signature || '暂无个性签名' }}</span>
            </div>
          </div>
          <div class="id-email-qrcode">
            <div class="id-email">
              <p class="user-id">ID: {{ userId }}</p>
              <div class="user-email-container">
                <span class="user-email">{{ userInfo.email }}</span>
                <div class="qrcode-small" @click="toggleQrcodeModal">
                  <img :src="qrcodeUrl" alt="个人二维码" class="qrcode-mini" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 二维码弹窗 -->
      <div v-if="showQrcodeModal" class="qrcode-modal">
        <div class="modal-content">
          <h4>个人二维码</h4>
          <div class="qrcode-container">
            <img :src="qrcodeUrl" alt="个人二维码" class="qrcode-full" />
          </div>
          <button @click="closeQrcodeModal" class="close-btn">关闭</button>
        </div>
      </div>

      <!-- 修改密码弹窗 -->
      <div v-if="showChangePasswordModal" class="change-password-modal">
        <div class="modal-content">
          <h4>修改密码</h4>
          <!-- 验证方式选择 -->
          <div v-if="!passwordForm.verificationMethod" class="form-group">
            <label>验证方式</label>
            <div class="verification-methods">
              <div v-if="userInfo && userInfo.phone" class="method-item" @click="selectVerificationMethod('phone')">
                <span class="method-icon">📱</span>
                <span class="method-text">手机号验证</span>
                <span class="method-detail">{{ userInfo.phone }}</span>
              </div>
              <div v-if="userInfo && userInfo.email" class="method-item" @click="selectVerificationMethod('email')">
                <span class="method-icon">✉️</span>
                <span class="method-text">邮箱验证</span>
                <span class="method-detail">{{ userInfo.email }}</span>
              </div>
              <div v-if="(!userInfo || (!userInfo.phone && !userInfo.email))" class="no-binding-tip">
                <p>您还未绑定手机号或邮箱</p>
                <p>请先绑定手机号或邮箱，再修改密码</p>
              </div>
              <div class="edit-actions">
                <button @click="closeChangePasswordModal" class="cancel-btn">取消</button>
              </div>
            </div>
          </div>
          <!-- 验证码输入 -->
          <div v-else-if="!passwordForm.verificationPassed" class="form-group">
            <div class="verification-tip">
              <p>即将向 {{ passwordForm.verificationMethod === 'phone' ? userInfo.phone : userInfo.email }} 发出验证信息</p>
            </div>
            <div class="form-group">
              <label for="passwordVerificationCode">验证码</label>
              <div class="phone-input-container">
                <input type="text" id="passwordVerificationCode" v-model="passwordForm.verificationCode" placeholder="请输入验证码" />
                <button type="button" class="code-btn" :disabled="isSendingCode" @click="sendPasswordVerificationCode">
                  {{ codeBtnText }}
                </button>
              </div>
            </div>
            <div class="edit-actions">
              <button @click="verifyCode" class="save-btn">验证</button>
              <button @click="resetVerificationMethod" class="cancel-btn">重新选择</button>
              <button @click="closeChangePasswordModal" class="cancel-btn">取消</button>
            </div>
          </div>
          <!-- 密码输入 -->
          <div v-else class="password-inputs">
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
              <button @click="savePassword" class="save-btn">提交</button>
              <button @click="closeChangePasswordModal" class="cancel-btn">取消</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 修改头像弹窗 -->
      <div v-if="showEditAvatarModal" class="edit-avatar-modal">
        <div class="modal-content">
          <h4>修改头像</h4>
          <div class="form-group">
            <label>头像</label>
            <div class="avatar-upload">
              <img :src="editAvatarForm.avatar || userInfo.avatar || defaultAvatar" alt="头像预览" class="avatar-preview" />
              <input type="file" ref="avatarInput" accept="image/*" @change="handleAvatarUpload" style="display: none;" />
              <button type="button" class="upload-btn" @click="triggerAvatarUpload">上传头像</button>
            </div>
          </div>
          <div class="edit-actions">
            <button @click="saveAvatar" class="save-btn">保存</button>
            <button @click="closeEditAvatarModal" class="cancel-btn">取消</button>
          </div>
        </div>
      </div>

      <!-- 修改昵称弹窗 -->
      <div v-if="showEditNicknameModal" class="edit-nickname-modal">
        <div class="modal-content">
          <h4>修改昵称</h4>
          <div class="form-group">
            <label for="editNickname">昵称</label>
            <input type="text" id="editNickname" v-model="editNicknameForm.nickname" placeholder="请输入昵称" @blur="checkNicknameUniqueness" />
            <p v-if="nicknameError" class="error-message">{{ nicknameError }}</p>
          </div>
          <div class="edit-actions">
            <button @click="saveNickname" class="save-btn">保存</button>
            <button @click="closeEditNicknameModal" class="cancel-btn">取消</button>
          </div>
        </div>
      </div>

      <!-- 修改手机号弹窗 -->
      <div v-if="showEditPhoneModal" class="edit-phone-modal">
        <div class="modal-content">
          <h4>{{ userInfo.phone ? '修改手机号' : '绑定手机号' }}</h4>
          <div class="form-group">
            <label for="editPhone">手机号</label>
            <div class="phone-input-container">
              <input type="tel" id="editPhone" v-model="editPhoneForm.phone" placeholder="请输入手机号" />
              <button type="button" class="code-btn" :disabled="isSendingCode" @click="sendPhoneVerificationCode">
                {{ codeBtnText }}
              </button>
            </div>
          </div>
          <div class="form-group">
            <label for="phoneVerificationCode">验证码</label>
            <input type="text" id="phoneVerificationCode" v-model="editPhoneForm.verificationCode" placeholder="请输入验证码" />
          </div>
          <div class="edit-actions">
            <button @click="savePhone" class="save-btn">{{ userInfo.phone ? '修改' : '绑定' }}</button>
            <button @click="closeEditPhoneModal" class="cancel-btn">取消</button>
          </div>
        </div>
      </div>

      <!-- 修改邮箱弹窗 -->
      <div v-if="showEditEmailModal" class="edit-email-modal">
        <div class="modal-content">
          <h4>{{ userInfo.email ? '修改邮箱' : '绑定邮箱' }}</h4>
          <div class="form-group">
            <label for="editEmail">邮箱</label>
            <input type="email" id="editEmail" v-model="editEmailForm.email" placeholder="请输入邮箱" />
          </div>
          <div class="form-group">
            <label for="emailVerificationCode">验证码</label>
            <div class="phone-input-container">
              <input type="text" id="emailVerificationCode" v-model="editEmailForm.verificationCode" placeholder="请输入验证码" />
              <button type="button" class="code-btn" :disabled="isSendingCode" @click="sendEmailVerificationCode">
                {{ codeBtnText }}
              </button>
            </div>
          </div>
          <div class="edit-actions">
            <button @click="saveEmail" class="save-btn">{{ userInfo.email ? '修改' : '绑定' }}</button>
            <button @click="closeEditEmailModal" class="cancel-btn">取消</button>
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
            <p>开发者：aixiaoqinghe</p>
            <p>© 2026 日期倒计时</p>
          </div>
          <button @click="closeAboutModal" class="close-btn">关闭</button>
        </div>
      </div>

      <!-- 功能列表 -->
      <div class="features">
        <div class="feature-section">
          <h4 class="section-title">账户设置</h4>
          <div class="feature-item" @click="toggleChangePasswordModal">
            <span class="feature-icon">🔐</span>
            <span class="feature-name">修改密码</span>
            <span class="feature-arrow">›</span>
          </div>
          <div class="feature-item" @click="toggleEditAvatarModal">
            <span class="feature-icon">🖼️</span>
            <span class="feature-name">修改头像</span>
            <span class="feature-arrow">›</span>
          </div>
          <div class="feature-item" @click="toggleEditNicknameModal">
            <span class="feature-icon">🎨</span>
            <span class="feature-name">修改昵称</span>
            <span class="feature-arrow">›</span>
          </div>
          <div class="feature-item" @click="toggleEditPhoneModal">
            <span class="feature-icon">📱</span>
            <span class="feature-name">{{ userInfo.phone ? '修改手机号' : '绑定手机号' }}</span>
            <span class="feature-arrow">›</span>
          </div>
          <div class="feature-item" @click="toggleEditEmailModal">
            <span class="feature-icon">✉️</span>
            <span class="feature-name">{{ userInfo.email ? '修改邮箱' : '绑定邮箱' }}</span>
            <span class="feature-arrow">›</span>
          </div>
        </div>
        <!-- 账户安全功能 -->
         <div class="feature-section">
          <h4 class="section-title">账户安全</h4>
          <div class="security-level">
            <div class="security-info">
              <span class="security-icon">🛡️</span>
              <div>
                <p class="security-title">安全等级</p>
                <p class="security-desc">{{ securityLevelText }}</p>
              </div>
            </div>
            <div class="security-progress">
              <div class="progress-bar" :style="{ width: securityLevel + '%'}"></div>
            </div>
            <div class="feature-item" @click="showDeviceManagement">
              <span class="feature-icon">📱</span>
              <span class="feature-name">登录设备管理</span>
              <span class="feature-arrow">›</span>
            </div>
          </div>
         </div>

         <!-- 通知与隐私功能 -->
          <div class="feature-section">
            <h4 class="section-title">通知与隐私</h4>
            <div class="feature-item" @click="showNotificationSettings">
              <span class="feature-icon">🔔</span>
              <span class="feature-name">消息通知设置</span>
              <span class="feature-arrow">›</span>
            </div>
            <div class="feature-item" @click="showPrivacySettings">
              <span class="feature-icon">🔒</span>
              <span class="feature-name">隐私设置</span>
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
import { showToast, showSuccessToast, showFailToast } from 'vant'
export default {
  name: 'homeMyself',
  setup () {
    const router = useRouter()
    const userInfo = ref(null)
    const showQrcodeModal = ref(false)
    const showChangePasswordModal = ref(false)
    const showEditAvatarModal = ref(false)
    const showEditNicknameModal = ref(false)
    const showEditPhoneModal = ref(false)
    const showEditEmailModal = ref(false)
    const showAboutModal = ref(false)
    const defaultAvatar = 'https://a0ai.marscode.cn/api/ide/v1/text_to_image?prompt=default%20user%20avatar%20simple%20flat%20design&image_size=square'

    // 密码修改表单
    const passwordForm = ref({
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
      verificationMethod: '', // 'phone' or 'email'
      verificationCode: '',
      verificationPassed: false
    })

    // 头像修改表单
    const editAvatarForm = ref({
    })

    // 昵称修改表单
    const editNicknameForm = ref({
      nickname: ''
    })

    // 手机号修改表单
    const editPhoneForm = ref({
      phone: '',
      verificationCode: ''
    })

    // 邮箱修改表单
    const editEmailForm = ref({
      email: '',
      verificationCode: ''
    })

    // 验证码相关
    const isSendingCode = ref(false)
    const codeBtnText = ref('获取验证码')
    const avatarInput = ref(null)

    // 昵称错误信息
    const nicknameError = ref('')

    // 模拟已存在的昵称列表
    const existingNicknames = ref(['admin', 'user123', 'test'])

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
        userInfo.value = JSON.parse(storedUser)
      }
    }

    // 切换二维码弹窗
    const toggleQrcodeModal = function () {
      showQrcodeModal.value = !showQrcodeModal.value
    }

    // 关闭二维码弹窗
    const closeQrcodeModal = function () {
      showQrcodeModal.value = false
    }

    // 切换修改密码弹窗
    const toggleChangePasswordModal = function () {
      showChangePasswordModal.value = !showChangePasswordModal.value
      if (showChangePasswordModal.value) {
        // 重置密码表单
        passwordForm.value = {
          oldPassword: '',
          newPassword: '',
          confirmPassword: '',
          verificationMethod: '',
          verificationCode: '',
          verificationPassed: false
        }
      }
    }

    // 关闭修改密码弹窗
    const closeChangePasswordModal = function () {
      showChangePasswordModal.value = false
    }

    // 选择验证方式
    const selectVerificationMethod = function (method) {
      passwordForm.value.verificationMethod = method
      passwordForm.value.verificationCode = ''
      passwordForm.value.verificationPassed = false
    }

    // 重置验证方式
    const resetVerificationMethod = function () {
      passwordForm.value.verificationMethod = ''
      passwordForm.value.verificationCode = ''
      passwordForm.value.verificationPassed = false
    }

    // 验证验证码
    const verifyCode = function () {
      if (!passwordForm.value.verificationCode) {
        showToast('请输入验证码')
        return
      }
      // 模拟验证验证码
      if (passwordForm.value.verificationCode !== '123456') {
        showFailToast('验证码错误')
        return
      }
      passwordForm.value.verificationPassed = true
    }

    // 保存密码
    const savePassword = function () {
      const { oldPassword, newPassword, confirmPassword } = passwordForm.value
      if (!oldPassword) {
        showToast('请输入旧密码')
        return
      }
      if (!newPassword) {
        showToast('请输入新密码')
        return
      }
      if (newPassword.length < 6) {
        showToast('新密码长度不能少于6位')
        return
      }
      if (newPassword !== confirmPassword) {
        showToast('两次输入的密码不一致')
        return
      }
      // 模拟保存密码
      showSuccessToast('密码修改成功')
      showChangePasswordModal.value = false
    }

    // 切换修改头像弹窗
    const toggleEditAvatarModal = function () {
      showEditAvatarModal.value = !showEditAvatarModal.value
      if (showEditAvatarModal.value) {
        editAvatarForm.value = {}
      }
    }

    // 关闭修改头像弹窗
    const closeEditAvatarModal = function () {
      showEditAvatarModal.value = false
    }

    // 保存头像
    const saveAvatar = function () {
      if (editAvatarForm.value.avatar) {
        userInfo.value.avatar = editAvatarForm.value.avatar
        // 更新本地存储
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
        showSuccessToast('头像修改成功')
        showEditAvatarModal.value = false
      } else {
        showToast('请选择头像')
      }
    }

    // 切换修改昵称弹窗
    const toggleEditNicknameModal = function () {
      showEditNicknameModal.value = !showEditNicknameModal.value
      if (showEditNicknameModal.value) {
        editNicknameForm.value.nickname = userInfo.value.nickname || ''
        nicknameError.value = ''
      }
    }

    // 关闭修改昵称弹窗
    const closeEditNicknameModal = function () {
      showEditNicknameModal.value = false
    }

    // 检查昵称唯一性
    const checkNicknameUniqueness = function () {
      const nickname = editNicknameForm.value.nickname.trim()
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

    // 保存昵称
    const saveNickname = function () {
      const nickname = editNicknameForm.value.nickname.trim()
      if (!nickname) {
        showToast('请输入昵称')
        return
      }
      if (nicknameError.value) {
        showToast(nicknameError.value)
        return
      }
      userInfo.value.nickname = nickname
      // 更新本地存储
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
      showSuccessToast('昵称修改成功')
      showEditNicknameModal.value = false
    }

    // 切换修改手机号弹窗
    const toggleEditPhoneModal = function () {
      showEditPhoneModal.value = !showEditPhoneModal.value
      if (showEditPhoneModal.value) {
        editPhoneForm.value = {
          phone: userInfo.value.phone || '',
          verificationCode: ''
        }
      }
    }

    // 关闭修改手机号弹窗
    const closeEditPhoneModal = function () {
      showEditPhoneModal.value = false
    }

    // 保存手机号
    const savePhone = function () {
      const phone = editPhoneForm.value.phone
      const code = editPhoneForm.value.verificationCode
      if (!phone) {
        showToast('请输入手机号')
        return
      }
      if (!/^1[3-9]\d{9}$/.test(phone)) {
        showToast('请输入正确的手机号')
        return
      }
      if (!code) {
        showToast('请输入验证码')
        return
      }
      // 模拟验证验证码
      if (code !== '123456') {
        showFailToast('验证码错误')
        return
      }
      userInfo.value.phone = phone
      // 更新本地存储
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
      showSuccessToast('手机号' + (userInfo.value.phone ? '修改' : '绑定') + '成功')
      showEditPhoneModal.value = false
    }

    // 切换修改邮箱弹窗
    const toggleEditEmailModal = function () {
      showEditEmailModal.value = !showEditEmailModal.value
      if (showEditEmailModal.value) {
        editEmailForm.value = {
          email: userInfo.value.email || '',
          verificationCode: ''
        }
      }
    }

    // 关闭修改邮箱弹窗
    const closeEditEmailModal = function () {
      showEditEmailModal.value = false
    }

    // 保存邮箱
    const saveEmail = function () {
      const email = editEmailForm.value.email
      const code = editEmailForm.value.verificationCode
      if (!email) {
        showToast('请输入邮箱')
        return
      }
      if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
        showToast('请输入正确的邮箱')
        return
      }
      if (!code) {
        showToast('请输入验证码')
        return
      }
      // 模拟验证验证码
      if (code !== '123456') {
        showFailToast('验证码错误')
        return
      }
      userInfo.value.email = email
      // 更新本地存储
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
      showSuccessToast('邮箱' + (userInfo.value.email ? '修改' : '绑定') + '成功')
      showEditEmailModal.value = false
    }

    // 触发头像上传
    const triggerAvatarUpload = function () {
      if (avatarInput.value) {
        avatarInput.value.click()
      }
    }

    // 处理头像上传
    const handleAvatarUpload = function (event) {
      const file = event.target.files[0]
      if (file) {
        // 检查文件类型
        if (!file.type.startsWith('image/')) {
          showToast('请上传图片文件')
          return
        }
        // 检查文件大小
        if (file.size > 2 * 1024 * 1024) {
          showToast('图片大小不能超过2MB')
          return
        }
        // 读取图片
        const reader = new FileReader()
        reader.onload = function (e) {
          editAvatarForm.value.avatar = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }

    // 发送密码验证码
    const sendPasswordVerificationCode = function () {
      if (isSendingCode.value) return
      // 模拟发送验证码
      isSendingCode.value = true
      let countdown = 60
      codeBtnText.value = `${countdown}秒后重新获取`
      const timer = setInterval(() => {
        countdown--
        codeBtnText.value = `${countdown}秒后重新获取`
        if (countdown <= 0) {
          clearInterval(timer)
          isSendingCode.value = false
          codeBtnText.value = '获取验证码'
        }
      }, 1000)
      showSuccessToast('验证码已发送（模拟）')
    }

    // 发送手机号验证码
    const sendPhoneVerificationCode = function () {
      if (isSendingCode.value) return
      const phone = editPhoneForm.value.phone
      if (!phone) {
        showToast('请输入手机号')
        return
      }
      if (!/^1[3-9]\d{9}$/.test(phone)) {
        showToast('请输入正确的手机号')
        return
      }
      // 模拟发送验证码
      isSendingCode.value = true
      let countdown = 60
      codeBtnText.value = `${countdown}秒后重新获取`
      const timer = setInterval(() => {
        countdown--
        codeBtnText.value = `${countdown}秒后重新获取`
        if (countdown <= 0) {
          clearInterval(timer)
          isSendingCode.value = false
          codeBtnText.value = '获取验证码'
        }
      }, 1000)
      showSuccessToast('验证码已发送（模拟）')
    }

    // 发送邮箱验证码
    const sendEmailVerificationCode = function () {
      if (isSendingCode.value) return
      const email = editEmailForm.value.email
      if (!email) {
        showToast('请输入邮箱')
        return
      }
      if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
        showToast('请输入正确的邮箱')
        return
      }
      // 模拟发送验证码
      isSendingCode.value = true
      let countdown = 60
      codeBtnText.value = `${countdown}秒后重新获取`
      const timer = setInterval(() => {
        countdown--
        codeBtnText.value = `${countdown}秒后重新获取`
        if (countdown <= 0) {
          clearInterval(timer)
          isSendingCode.value = false
          codeBtnText.value = '获取验证码'
        }
      }, 1000)
      showSuccessToast('验证码已发送（模拟）')
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

    // 安全等级相关
    const securityLevel = computed(() => {
      if (!userInfo.value) return 0
      let level = 0
      if (userInfo.value.phone) level += 50
      if (userInfo.value.email) level += 50
      return level
    })

    const securityLevelText = computed(() => {
      const level = securityLevel.value
      if (level === 0) return '低'
      if (level === 50) return '中'
      return '高'
    })

    // 设备管理
    const showDeviceManagement = function () {
      showToast('登录设备管理功能开发中')
    }

    // 通知设置
    const showNotificationSettings = function () {
      showToast('消息通知设置功能开发中')
    }

    // 隐私设置
    const showPrivacySettings = function () {
      showToast('隐私设置功能开发中')
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
      showQrcodeModal,
      showChangePasswordModal,
      showEditAvatarModal,
      showEditNicknameModal,
      showEditPhoneModal,
      showEditEmailModal,
      showAboutModal,
      passwordForm,
      editAvatarForm,
      editNicknameForm,
      editPhoneForm,
      editEmailForm,
      isSendingCode,
      codeBtnText,
      avatarInput,
      nicknameError,
      toggleQrcodeModal,
      closeQrcodeModal,
      toggleChangePasswordModal,
      closeChangePasswordModal,
      selectVerificationMethod,
      resetVerificationMethod,
      verifyCode,
      savePassword,
      toggleEditAvatarModal,
      closeEditAvatarModal,
      saveAvatar,
      toggleEditNicknameModal,
      closeEditNicknameModal,
      checkNicknameUniqueness,
      saveNickname,
      toggleEditPhoneModal,
      closeEditPhoneModal,
      savePhone,
      toggleEditEmailModal,
      closeEditEmailModal,
      saveEmail,
      triggerAvatarUpload,
      handleAvatarUpload,
      sendPasswordVerificationCode,
      sendPhoneVerificationCode,
      sendEmailVerificationCode,
      showAbout,
      closeAboutModal,
      logout,
      securityLevel,
      securityLevelText,
      showDeviceManagement,
      showNotificationSettings,
      showPrivacySettings
    }
  }
}
</script>

<style scoped>
@import '../../styles/home.css';
@import '../../styles/mine.css';
</style>

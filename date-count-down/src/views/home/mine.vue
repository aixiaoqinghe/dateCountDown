<template>
  <div class="mine-container">
    <h2>个人中心</h2>
    <!-- 登录状态显示 -->
    <div v-if="userInfo" class="user-info">
      <!-- 用户头像和基本信息 -->
      <div class="user-header">
        <div class="avatar-container">
          <img :src="userInfo.avatar || defaultAvatar" alt="用户头像" class="user-avatar" @error="handleAvatarError" />
        </div>
        <div class="user-basic-info">
          <div class="name-signature">
            <h3>{{ userInfo.nickname || userInfo.username }}</h3>
            <div class="signature-container">
              <span class="signature-icon" @click="toggleSignatureEdit">✏️</span>
              <span v-if="!isEditingSignature" class="user-signature">{{ userInfo.signature || '暂无个性签名' }}</span>
              <input v-else type="text" v-model="editSignature" placeholder="请输入个性签名" maxlength="50" class="signature-input" @blur="saveSignature" @keyup.enter="saveSignature" />
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
              <div class="user-phone-container">
                <span class="user-phone-label">📱</span>
                <span class="user-phone">{{ userInfo.phone || '未绑定' }}</span>
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

      <!-- 登录设备管理弹窗 -->
      <div v-if="showDeviceManagementModal" class="device-management-modal">
        <div class="modal-content">
          <h4>登录设备管理</h4>
          <div class="device-list">
            <!-- 骨架屏 -->
            <template v-if="devices.length === 0">
              <div v-for="i in 3" :key="i" class="device-item skeleton">
                <div class="device-info">
                  <div class="device-icon skeleton-icon"></div>
                  <div class="device-details">
                    <div class="device-name-row">
                      <div class="skeleton-text skeleton-title"></div>
                    </div>
                    <div class="skeleton-text skeleton-small"></div>
                    <div class="skeleton-text skeleton-small"></div>
                    <div class="skeleton-text skeleton-small"></div>
                    <div class="skeleton-text skeleton-small"></div>
                  </div>
                </div>
              </div>
            </template>
            <!-- 实际数据 -->
            <div v-else v-for="(device, index) in devices" :key="device.id" class="device-item">
              <div class="device-info">
                <div class="device-icon">
                  {{ device.deviceType === '手机' ? '📱' : device.deviceType === '平板' ? '📟' : '💻' }}
                </div>
                <div class="device-details">
                  <div class="device-name-row">
                    <h5>{{ device.name }}</h5>
                    <span v-if="device.isCurrent" class="status-current">当前设备</span>
                  </div>
                  <p class="device-system">{{ device.os }} · {{ device.browser }}</p>
                  <p class="device-location">{{ device.location }}</p>
                  <p class="device-time">最后登录：{{ device.lastLogin }}</p>
                  <p class="device-ip">IP地址：{{ device.ip }}</p>
                </div>
              </div>
              <div class="device-status">
                <button v-if="!device.isCurrent" @click="removeDevice(device.id, index)" class="remove-device-btn">移除</button>
              </div>
            </div>
          </div>
          <button @click="closeDeviceManagementModal" class="close-btn">关闭</button>
        </div>
      </div>

      <!-- 消息通知设置弹窗 -->
      <div v-if="showNotificationSettingsModal" class="notification-settings-modal">
        <div class="modal-content">
          <h4>消息通知设置</h4>

          <!-- 通知类型 -->
          <div class="settings-section">
            <h5>通知类型</h5>
            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-icon">⏰</span>
                <div>
                  <p class="setting-name">倒计时提醒</p>
                  <p class="setting-desc">接收倒计时到期提醒</p>
                </div>
              </div>
              <div class="setting-toggle">
                <input type="checkbox" v-model="notificationSettings.countdownReminder" id="countdownReminder">
                <label for="countdownReminder"></label>
              </div>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-icon">📢</span>
                <div>
                  <p class="setting-name">系统消息</p>
                  <p class="setting-desc">接收系统更新、功能上线等消息</p>
                </div>
              </div>
              <div class="setting-toggle">
                <input type="checkbox" v-model="notificationSettings.systemMessages" id="systemMessages">
                <label for="systemMessages"></label>
              </div>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-icon">🎁</span>
                <div>
                  <p class="setting-name">活动通知</p>
                  <p class="setting-desc">接收活动和优惠信息</p>
                </div>
              </div>
              <div class="setting-toggle">
                <input type="checkbox" v-model="notificationSettings.activityNotifications" id="activityNotifications">
                <label for="activityNotifications"></label>
              </div>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-icon">🔒</span>
                <div>
                  <p class="setting-name">重要通知</p>
                  <p class="setting-desc">账户安全相关通知（不可关闭）</p>
                </div>
              </div>
              <div class="setting-toggle">
                <input type="checkbox" v-model="notificationSettings.importantNotifications" id="importantNotifications" disabled>
                <label for="importantNotifications"></label>
              </div>
            </div>
          </div>

          <!-- 通知方式 -->
          <div class="settings-section">
            <h5>通知方式</h5>
            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-icon">🖥️</span>
                <div>
                  <p class="setting-name">弹窗通知</p>
                  <p class="setting-desc">应用内弹窗显示通知</p>
                </div>
              </div>
              <div class="setting-toggle">
                <input type="checkbox" v-model="notificationSettings.popupNotification" id="popupNotification">
                <label for="popupNotification"></label>
              </div>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-icon">🔊</span>
                <div>
                  <p class="setting-name">声音提醒</p>
                  <p class="setting-desc">通知时播放提示音</p>
                </div>
              </div>
              <div class="setting-toggle">
                <input type="checkbox" v-model="notificationSettings.soundNotification" id="soundNotification">
                <label for="soundNotification"></label>
              </div>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-icon">📳</span>
                <div>
                  <p class="setting-name">震动提醒</p>
                  <p class="setting-desc">通知时触发震动（仅移动设备）</p>
                </div>
              </div>
              <div class="setting-toggle">
                <input type="checkbox" v-model="notificationSettings.vibrationNotification" id="vibrationNotification">
                <label for="vibrationNotification"></label>
              </div>
            </div>
          </div>

          <!-- 通知频率 -->
          <div class="settings-section">
            <h5>通知频率</h5>
            <div class="frequency-options">
              <div class="frequency-item" :class="{ active: notificationSettings.notificationFrequency === 'realtime' }" @click="notificationSettings.notificationFrequency = 'realtime'">
                <span class="frequency-icon">⚡</span>
                <span class="frequency-name">实时通知</span>
                <span class="frequency-desc">立即发送所有通知</span>
              </div>

              <div class="frequency-item" :class="{ active: notificationSettings.notificationFrequency === 'daily' }" @click="notificationSettings.notificationFrequency = 'daily'">
                <span class="frequency-icon">📅</span>
                <span class="frequency-name">每日摘要</span>
                <span class="frequency-desc">汇总为每日摘要发送</span>
              </div>
            </div>
          </div>

          <div class="edit-actions">
            <button @click="saveNotificationSettings" class="save-btn">保存设置</button>
            <button @click="closeNotificationSettingsModal" class="cancel-btn">取消</button>
          </div>
        </div>
      </div>

      <!-- 隐私设置弹窗 -->
      <div v-if="showPrivacySettingsModal" class="privacy-settings-modal">
        <div class="modal-content">
          <h4>隐私设置</h4>

          <!-- 个人信息管理 -->
          <div class="settings-section">
            <h5>个人信息管理</h5>
            <div class="setting-item">
              <div class="setting-info">
                <span class="setting-icon">👤</span>
                <div>
                  <p class="setting-name">个人信息可见性</p>
                  <p class="setting-desc">设置个人信息的可见范围</p>
                </div>
              </div>
              <div class="setting-select">
                <select v-model="privacySettings.personalInfoVisibility" class="select-input">
                  <option value="private">仅自己可见</option>
                  <option value="friends">对朋友可见</option>
                  <option value="public">公开可见</option>
                </select>
              </div>
            </div>

            <div class="action-buttons">
              <button @click="exportUserData" class="action-btn secondary">导出个人数据</button>
              <button @click="deleteUserData" class="action-btn danger">删除所有数据</button>
            </div>
          </div>

          <!-- 隐私政策 -->
          <div class="settings-section">
            <h5>隐私政策</h5>
            <div class="policy-info">
              <p class="policy-text">我们致力于保护您的隐私和个人信息。</p>
              <a href="#" class="policy-link">查看完整隐私政策</a>
              <p class="policy-updated">最后更新：2026年5月8日</p>
            </div>
          </div>

          <div class="edit-actions">
            <button @click="savePrivacySettings" class="save-btn">保存设置</button>
            <button @click="closePrivacySettingsModal" class="cancel-btn">取消</button>
          </div>
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

      <button @click="openLogoutConfirmModal" class="logout-btn">退出登录</button>

      <!-- 退出登录确认弹窗 -->
      <div class="logout-confirm-modal" v-if="showLogoutConfirmModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>退出登录</h3>
            <button class="modal-close" @click="closeLogoutConfirmModal">×</button>
          </div>
          <div class="modal-body">
            <div class="confirm-icon">⚠️</div>
            <p class="confirm-message">确定要退出登录吗？</p>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="closeLogoutConfirmModal">取消</button>
            <button class="confirm-btn" @click="confirmLogout">确定</button>
          </div>
        </div>
      </div>
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

    // 个性签名相关
    const isEditingSignature = ref(false)
    const editSignature = ref('')

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
    const qrcodeUrl = computed(() => {
      if (!userInfo.value) return ''
      const userData = `用户: ${userInfo.value.nickname || userInfo.value.username}\nID: ${userId.value}\n邮箱: ${userInfo.value.email}`
      const encodedData = encodeURIComponent(userData)
      // 使用更稳定的二维码API
      return `https://api.pwmqr.com/qrcode/create?url=${encodedData}&size=150x150`
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

    // 保存密码
    const savePassword = async function () {
      const { oldPassword, newPassword, confirmPassword } = passwordForm.value
      if (!oldPassword) {
        showToast('请输入旧密码')
        return
      }
      if (!newPassword) {
        showToast('请输入新密码')
        return
      }
      if (newPassword !== confirmPassword) {
        showToast('两次输入的密码不一致')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          const response = await fetch('/api/auth/change_password', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
              old_password: oldPassword,
              new_password: newPassword
            })
          })

          const result = await response.json()
          if (response.ok) {
            showSuccessToast('密码修改成功')
            showChangePasswordModal.value = false
          } else {
            showToast(result.message || '修改失败')
          }
        } else {
          showToast('请先登录')
        }
      } catch (error) {
        showToast('网络错误')
      }
    }

    // 切换修改头像弹窗
    const toggleEditAvatarModal = function () {
      showEditAvatarModal.value = !showEditAvatarModal.value
      // 只有关闭弹窗时才清空表单，避免打开时清空用户已选择的图片
      if (!showEditAvatarModal.value) {
        editAvatarForm.value = {}
      }
    }

    // 关闭修改头像弹窗
    const closeEditAvatarModal = function () {
      showEditAvatarModal.value = false
    }

    // 头像加载失败处理
    const handleAvatarError = function () {
      console.log('[handleAvatarError] 头像加载失败，尝试使用本地保存的图片')
      const localAvatar = localStorage.getItem('localAvatar')
      if (localAvatar && userInfo.value) {
        userInfo.value.avatar = localAvatar
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
        console.log('[handleAvatarError] 已切换到本地保存的头像')
      }
    }

    // 保存头像
    const saveAvatar = async function () {
      console.log('[saveAvatar] 开始保存头像')
      console.log('[saveAvatar] editAvatarForm.value:', editAvatarForm.value)
      console.log('[saveAvatar] editAvatarForm.value.avatar:', editAvatarForm.value.avatar)

      if (editAvatarForm.value.avatar) {
        try {
          // 确保 userInfo 有值
          if (!userInfo.value) {
            userInfo.value = {}
          }

          const token = localStorage.getItem('access_token')
          console.log('[saveAvatar] token:', token ? '存在' : '不存在')
          if (token) {
            // 将 Base64 图片转换为 Blob 对象
            const blob = await fetch(editAvatarForm.value.avatar).then(res => res.blob())

            // 创建 FormData 对象（用于文件上传）
            const formData = new FormData()
            formData.append('avatar', blob, 'avatar.png')

            // 调用后端专门的头像上传接口
            const response = await fetch('/api/auth/avatar', {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${token}`
                // 注意：不要设置 Content-Type，浏览器会自动设置正确的 multipart/form-data
              },
              body: formData
            })

            console.log('[saveAvatar] response.ok:', response.ok)
            console.log('[saveAvatar] response.status:', response.status)

            if (response.ok) {
              // 获取后端返回的头像 URL
              const result = await response.json()
              console.log('[saveAvatar] result:', result)
              console.log('[saveAvatar] result.avatar:', result.avatar)
              // 验证后端返回的头像 URL 是否有效
              if (result.avatar && result.avatar !== '') {
                // 后端返回的是相对路径，需要转换为完整URL
                let avatarUrl = result.avatar
                console.log('[saveAvatar] 原始头像路径:', avatarUrl)
                if (!avatarUrl.startsWith('http://') && !avatarUrl.startsWith('https://') && !avatarUrl.startsWith('data:')) {
                  console.log('[saveAvatar] 检测到相对路径，开始转换')
                  // 添加服务器地址前缀
                  avatarUrl = 'http://8.134.150.161' + avatarUrl
                  console.log('[saveAvatar] 转换后的完整URL:', avatarUrl)
                }
                // 添加时间戳参数防止浏览器缓存旧图片
                userInfo.value.avatar = avatarUrl + '?t=' + Date.now()
                console.log('[saveAvatar] 使用后端返回的头像:', userInfo.value.avatar)
              } else {
                // 如果后端没有返回有效头像，使用本地的 Base64 图片
                userInfo.value.avatar = editAvatarForm.value.avatar
                console.log('[saveAvatar] 使用本地 Base64 图片')
              }
              // 为了确保头像能正常显示，同时保存原始的 Base64 图片到本地存储
              // 如果后端图片加载失败，下次登录时可以使用本地保存的 Base64 图片
              localStorage.setItem('localAvatar', editAvatarForm.value.avatar)
              console.log('[saveAvatar] userInfo.value.avatar:', userInfo.value.avatar)
              localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
              // 同时保存到用户偏好设置，确保退出登录后可以恢复
              // 注意：保存原始的Base64图片，而不是后端返回的URL
              const userPreferences = {
                avatar: editAvatarForm.value.avatar,
                signature: userInfo.value.signature
              }
              localStorage.setItem('userPreferences', JSON.stringify(userPreferences))
              showSuccessToast('头像修改成功')
              showEditAvatarModal.value = false
            } else {
              // 如果后端接口失败，降级到本地保存
              userInfo.value.avatar = editAvatarForm.value.avatar
              localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
              // 同时保存到用户偏好设置，确保退出登录后可以恢复
              // 注意：保存原始的Base64图片，而不是后端返回的URL
              const userPreferences = {
                avatar: editAvatarForm.value.avatar,
                signature: userInfo.value.signature
              }
              localStorage.setItem('userPreferences', JSON.stringify(userPreferences))
              showSuccessToast('头像修改成功（本地）')
              showEditAvatarModal.value = false
            }
          } else {
            // 未登录，只保存到本地
            userInfo.value.avatar = editAvatarForm.value.avatar
            localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
            showSuccessToast('头像修改成功（本地）')
            showEditAvatarModal.value = false
          }
        } catch (error) {
          // 网络错误时降级到本地保存
          console.error('头像上传失败:', error)
          // 确保 userInfo 有值
          if (!userInfo.value) {
            userInfo.value = {}
          }
          userInfo.value.avatar = editAvatarForm.value.avatar
          localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
          showSuccessToast('头像修改成功（本地）')
          showEditAvatarModal.value = false
        }
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
    const saveNickname = async function () {
      if (!editNicknameForm.value.nickname.trim()) {
        showToast('请输入昵称')
        return
      }
      if (editNicknameForm.value.nickname.length > 20) {
        showToast('昵称长度不能超过20位')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          const response = await fetch('/api/auth/user', {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({
              nickname: editNicknameForm.value.nickname
            })
          })

          const result = await response.json()
          if (response.ok) {
            const storedUser = localStorage.getItem('userInfo')
            if (storedUser) {
              const user = JSON.parse(storedUser)
              user.nickname = editNicknameForm.value.nickname
              localStorage.setItem('userInfo', JSON.stringify(user))
              userInfo.value = user
            }
            showSuccessToast('昵称修改成功')
            showEditNicknameModal.value = false
          } else {
            showToast(result.message || '修改失败')
          }
        } else {
          showToast('请先登录')
        }
      } catch (error) {
        showToast('网络错误')
      }
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
    const savePhone = async function () {
      const phone = editPhoneForm.value.phone
      const code = editPhoneForm.value.verificationCode
      if (!phone) {
        showToast('请输入手机号')
        return
      }
      if (!code) {
        showToast('请输入验证码')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        const url = userInfo.value.phone
          ? '/api/auth/change_phone'
          : '/api/auth/bind_phone'

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            phone: phone,
            verification_code: code
          })
        })

        const result = await response.json()

        if (response.ok) {
          userInfo.value.phone = phone.replace(/[^0-9]/g, '')
          localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
          showSuccessToast('手机号' + (userInfo.value.phone ? '修改' : '绑定') + '成功')
          showEditPhoneModal.value = false
        } else {
          showToast(result.message || '操作失败')
        }
      } catch (error) {
        showToast('网络错误')
      }
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
    const saveEmail = async function () {
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

      try {
        const token = localStorage.getItem('access_token')
        const url = userInfo.value.email
          ? '/api/auth/change_email'
          : '/api/auth/bind_email'

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            email: email,
            verification_code: code
          })
        })

        const result = await response.json()

        if (response.ok) {
          userInfo.value.email = email
          localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
          showSuccessToast('邮箱' + (userInfo.value.email ? '修改' : '绑定') + '成功')
          showEditEmailModal.value = false
        } else {
          showToast(result.message || '操作失败')
        }
      } catch (error) {
        showToast('网络错误')
      }
    }

    // 触发头像上传
    const triggerAvatarUpload = function () {
      if (avatarInput.value) {
        avatarInput.value.click()
      }
    }

    // 处理头像上传
    const handleAvatarUpload = function (event) {
      console.log('[handleAvatarUpload] 触发头像上传')
      const file = event.target.files[0]
      console.log('[handleAvatarUpload] file:', file)
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
          console.log('[handleAvatarUpload] 图片读取完成')
          console.log('[handleAvatarUpload] e.target.result:', e.target.result ? '有值' : '空')
          editAvatarForm.value.avatar = e.target.result
          console.log('[handleAvatarUpload] editAvatarForm.value.avatar:', editAvatarForm.value.avatar ? '有值' : '空')
        }
        reader.readAsDataURL(file)
      }
    }

    // 发送密码验证码
    const sendPasswordVerificationCode = async function () {
      if (isSendingCode.value) return

      const target = passwordForm.value.verificationMethod === 'phone'
        ? userInfo.value.phone
        : userInfo.value.email

      if (!target) {
        showToast('验证目标不存在')
        return
      }

      try {
        const url = passwordForm.value.verificationMethod === 'phone'
          ? '/api/verify/send_sms_code'
          : '/api/verify/send_email_code'

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            [passwordForm.value.verificationMethod]: target
          })
        })

        const result = await response.json()

        if (response.ok) {
          showSuccessToast('验证码已发送')
          // 开始倒计时
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
        } else {
          showToast(result.message || '发送失败')
        }
      } catch (error) {
        showToast('网络错误')
      }
    }

    // 验证验证码（修改密码场景）
    const verifyCode = async function () {
      if (!passwordForm.value.verificationCode) {
        showToast('请输入验证码')
        return
      }

      try {
        const url = passwordForm.value.verificationMethod === 'phone'
          ? '/api/verify/verify_sms_code'
          : '/api/verify/verify_email_code'

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            [passwordForm.value.verificationMethod]: passwordForm.value.verificationMethod === 'phone' ? userInfo.value.phone : userInfo.value.email,
            code: passwordForm.value.verificationCode
          })
        })

        const result = await response.json()

        if (response.ok) {
          passwordForm.value.verificationPassed = true
          showSuccessToast('验证成功')
        } else {
          showFailToast(result.message || '验证失败')
        }
      } catch (error) {
        showFailToast('网络错误')
      }
    }

    // 发送手机号验证码
    const sendPhoneVerificationCode = async function () {
      if (isSendingCode.value) return
      const phone = editPhoneForm.value.phone
      if (!phone) {
        showToast('请输入手机号')
        return
      }

      if (!/^1[3-9]\d{9}$/.test(phone.replace(/[^0-9]/g, ''))) {
        showToast('请输入正确的手机号')
        return
      }

      try {
        const token = localStorage.getItem('access_token')
        // 根据是否已绑定手机号选择不同的API
        const url = userInfo.value.phone ? '/api/auth/send_change_phone_code' : '/api/auth/send_bind_phone_code'

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            phone: phone
          })
        })
        const result = await response.json()
        if (response.ok) {
          showSuccessToast('验证码已发送')
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
        } else {
          showToast(result.message || '发送失败')
        }
      } catch (error) {
        showToast('网络错误')
      }
    }

    // 发送邮箱验证码
    const sendEmailVerificationCode = async function () {
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

      try {
        const token = localStorage.getItem('access_token')
        const url = userInfo.value.email
          ? '/api/auth/send_change_email_code'
          : '/api/auth/send_bind_email_code'

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            email: email
          })
        })

        const result = await response.json()

        if (response.ok) {
          showSuccessToast('验证码已发送')
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
        } else {
          showToast(result.message || '发送失败')
        }
      } catch (error) {
        showToast('网络错误')
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

    // 退出登录确认弹窗
    const showLogoutConfirmModal = ref(false)

    // 打开退出登录确认弹窗
    const openLogoutConfirmModal = function () {
      showLogoutConfirmModal.value = true
    }

    // 关闭退出登录确认弹窗
    const closeLogoutConfirmModal = function () {
      showLogoutConfirmModal.value = false
    }

    // 确认退出登录
    const confirmLogout = function () {
      // 在清除用户信息前，保存头像和个性签名到偏好设置
      if (userInfo.value) {
        const userPreferences = {
          avatar: userInfo.value.avatar,
          signature: userInfo.value.signature
        }
        localStorage.setItem('userPreferences', JSON.stringify(userPreferences))
      }
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
    const showDeviceManagementModal = ref(false)
    // 模拟数据
    // const devices = ref([
    //   {
    //     id: 1,
    //     name: '当前设备',
    //     deviceType: '电脑',
    //     os: 'Windows 11',
    //     browser: 'Chrome',
    //     lastLogin: '2026-04-25 10:30:00',
    //     ip: '192.168.1.100',
    //     location: '本地网络',
    //     isCurrent: true
    //   },
    //   {
    //     id: 2,
    //     name: 'iPhone 14',
    //     deviceType: '手机',
    //     os: 'iOS 17.0',
    //     browser: 'Safari',
    //     lastLogin: '2026-04-24 15:45:00',
    //     ip: '10.0.0.5',
    //     location: '北京市',
    //     isCurrent: false
    //   },
    //   {
    //     id: 3,
    //     name: 'MacBook Pro',
    //     deviceType: '电脑',
    //     os: 'macOS Sonoma',
    //     browser: 'Safari',
    //     lastLogin: '2026-04-23 09:20:00',
    //     ip: '192.168.1.101',
    //     location: '上海市',
    //     isCurrent: false
    //   }
    // ])

    // 调用API
    // 设备信息相关
    const devices = ref([])

    // 生成设备唯一标识（只生成一次，保存在localStorage）
    const generateDeviceId = () => {
      const id = 'device-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9)
      localStorage.setItem('device_id', id)
      return id
    }

    const currentDeviceId = ref(localStorage.getItem('device_id') || generateDeviceId())

    // 自动获取浏览器信息
    const getBrowserInfo = () => {
      const userAgent = navigator.userAgent

      // 检查浏览器
      let browser = '未知浏览器'
      if (userAgent.includes('Chrome') && !userAgent.includes('Edg')) {
        browser = 'Chrome'
      } else if (userAgent.includes('Firefox')) {
        browser = 'Firefox'
      } else if (userAgent.includes('Safari') && !userAgent.includes('Chrome')) {
        browser = 'Safari'
      } else if (userAgent.includes('Edge')) {
        browser = 'Edge'
      } else if (userAgent.includes('Opera') || userAgent.includes('OPR')) {
        browser = 'Opera'
      }

      // 检查操作系统
      let os = '未知系统'
      if (userAgent.includes('Windows')) {
        os = 'Windows'
      } else if (userAgent.includes('Mac OS')) {
        os = 'macOS'
      } else if (userAgent.includes('Linux') && !userAgent.includes('Android')) {
        os = 'Linux'
      } else if (userAgent.includes('Android')) {
        os = 'Android'
      } else if (userAgent.includes('iPhone') || userAgent.includes('iPad')) {
        os = 'iOS'
      }

      // 检测设备类型
      let deviceType = '电脑'
      if (/Mobile|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent)) {
        deviceType = '手机'
      } else if (/Tablet|iPad/i.test(userAgent)) {
        deviceType = '平板'
      }

      return { browser, os, deviceType }
    }

    // 获取设备名称
    const getDeviceName = () => {
      const { browser, os } = getBrowserInfo()
      return `${browser} - ${os}`
    }

    // 获取IP地理位置信息（带缓存和超时）
    const getLocationByIP = async () => {
      // 优先从缓存获取
      const cachedLocation = localStorage.getItem('userLocation')
      if (cachedLocation) {
        return cachedLocation
      }

      try {
        // 设置10秒超时
        const controller = new AbortController()
        const timeout = setTimeout(() => controller.abort(), 10000)

        const response = await fetch('https://ipapi.co/json/', {
          signal: controller.signal
        })
        clearTimeout(timeout)

        if (response.ok) {
          const data = await response.json()
          const city = data.city || ''
          const region = data.region || ''
          const country = data.country_name || ''
          let location = '未知位置'
          if (city && region && country) {
            location = `${country} ${region} ${city}`
          } else if (region && country) {
            location = `${country} ${region}`
          } else if (country) {
            location = country
          }
          localStorage.setItem('userLocation', location)
          return location
        }
      } catch (error) {
        console.error('获取地理位置失败：', error)
      }
      return '未知位置'
    }

    // 保存当前设备信息（登录时调用）
    const saveCurrentDevice = async () => {
      const token = localStorage.getItem('access_token')
      if (!token) return

      const { browser, os, deviceType } = getBrowserInfo()
      const location = await getLocationByIP()

      try {
        await fetch('/api/devices/current', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            device_id: currentDeviceId.value,
            name: getDeviceName(),
            deviceType: deviceType,
            os: os,
            browser: browser,
            location: location
          })
        })
      } catch (error) {
        console.error('保存设备信息失败：', error)
      }
    }

    // 获取设备列表
    const fetchDevices = async () => {
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          const response = await fetch('/api/devices', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          if (response.ok) {
            devices.value = await response.json()
          }
        } catch (error) {
          console.error('获取列表失败：', error)
        }
      }
    }

    const showDeviceManagement = async function () {
      showDeviceManagementModal.value = true
      await fetchDevices()
    }

    const closeDeviceManagementModal = function () {
      showDeviceManagementModal.value = false
    }

    // 只是修改本地数据
    // const removeDevice = function (index) {
    //   if (devices.value[index].isCurrent) {
    //     showToast('不能移除当前设备')
    //     return
    //   }
    //   devices.value.splice(index, 1)
    //   // 更新本地存储
    //   localStorage.setItem('devices', JSON.stringify(devices.value))
    //   showSuccessToast('设备已成功移除')
    // }

    // 调用API
    // 删除设备
    const removeDevice = async (deviceId, deviceIndex) => {
      const token = localStorage.getItem('access_token')
      const currentDeviceId = localStorage.getItem('device_id')

      // 检查是否当前设备
      if (devices.value[deviceIndex].isCurrent) {
        showToast('不能移除当前设备')
        return
      }

      try {
        const response = await fetch(`/api/devices/${deviceId}`, {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            current_device_id: currentDeviceId
          })
        })

        if (response.ok) {
          // 从本地列表中移除
          devices.value.splice(deviceIndex, 1)
          showSuccessToast('设备已成功移除')
        } else {
          const data = await response.json()
          showToast(data.message)
        }
      } catch (error) {
        console.error('删除设备失败:', error)
        showToast('删除设备失败')
      }
    }

    // 在登录成功后调用
    const handleLoginSuccess = async () => {
      // 保存设备信息
      await saveCurrentDevice()
      // 获取设备列表
      await fetchDevices()
    }

    // 消息通知设置
    const showNotificationSettingsModal = ref(false)
    const notificationSettings = ref({
      // 通知类型
      countdownReminder: true,
      systemMessages: true,
      activityNotifications: true,
      importantNotifications: true, // 默认开启且不可关闭

      // 通知方式
      popupNotification: true,
      soundNotification: true,
      vibrationNotification: true,

      // 通知频率
      notificationFrequency: 'realtime' // 'realtime', 'daily', 'custom'
    })

    const showNotificationSettings = function () {
      // 从本地存储加载设置
      const savedSettings = localStorage.getItem('notificationSettings')
      if (savedSettings) {
        notificationSettings.value = JSON.parse(savedSettings)
      }
      showNotificationSettingsModal.value = true
    }

    const closeNotificationSettingsModal = function () {
      showNotificationSettingsModal.value = false
    }

    const saveNotificationSettings = function () {
      // 保存设置到本地存储
      localStorage.setItem('notificationSettings', JSON.stringify(notificationSettings.value))
      showSuccessToast('通知设置已保存')
      showNotificationSettingsModal.value = false
    }

    // 隐私设置
    const showPrivacySettingsModal = ref(false)
    const privacySettings = ref({
      // 个人信息管理
      personalInfoVisibility: 'private' // 'private', 'friends', 'public'
    })

    const showPrivacySettings = async function () {
      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          const response = await fetch('/api/privacy/settings', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })

          if (response.ok) {
            const result = await response.json()
            privacySettings.value = result
            // 同时保存到本地
            localStorage.setItem('privacySettings', JSON.stringify(privacySettings.value))
          } else {
            // 如果后端获取失败，从本地存储加载
            const savedSettings = localStorage.getItem('privacySettings')
            if (savedSettings) {
              privacySettings.value = JSON.parse(savedSettings)
            }
          }
        } else {
          // 未登录，从本地存储加载
          const savedSettings = localStorage.getItem('privacySettings')
          if (savedSettings) {
            privacySettings.value = JSON.parse(savedSettings)
          }
        }
        showPrivacySettingsModal.value = true
      } catch (error) {
        console.error('获取隐私设置失败:', error)
        // 网络错误时从本地存储加载
        const savedSettings = localStorage.getItem('privacySettings')
        if (savedSettings) {
          privacySettings.value = JSON.parse(savedSettings)
        }
        showPrivacySettingsModal.value = true
      }
    }

    const closePrivacySettingsModal = function () {
      showPrivacySettingsModal.value = false
    }

    const savePrivacySettings = async function () {
      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          const response = await fetch('/api/privacy/settings', {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(privacySettings.value)
          })

          if (response.ok) {
            // 保存到本地存储
            localStorage.setItem('privacySettings', JSON.stringify(privacySettings.value))
            showSuccessToast('隐私设置已保存')
            showPrivacySettingsModal.value = false
          } else {
            const result = await response.json()
            showToast(result.message || '保存失败')
          }
        } else {
          // 未登录，只保存到本地
          localStorage.setItem('privacySettings', JSON.stringify(privacySettings.value))
          showSuccessToast('隐私设置已保存（本地）')
          showPrivacySettingsModal.value = false
        }
      } catch (error) {
        console.error('保存隐私设置失败:', error)
        // 网络错误时保存到本地
        localStorage.setItem('privacySettings', JSON.stringify(privacySettings.value))
        showSuccessToast('隐私设置已保存（本地）')
        showPrivacySettingsModal.value = false
      }
    }

    const exportUserData = function () {
      showToast('数据导出功能开发中')
    }

    const deleteUserData = function () {
      if (confirm('确定要删除所有个人数据吗？此操作不可恢复。')) {
        // 清除本地存储
        localStorage.removeItem('userInfo')
        localStorage.removeItem('devices')
        localStorage.removeItem('notificationSettings')
        localStorage.removeItem('privacySettings')
        showSuccessToast('个人数据已删除')
        // 跳转到登录页面
        router.push('/login')
      }
    }

    // 个性签名相关方法
    const toggleSignatureEdit = function () {
      isEditingSignature.value = !isEditingSignature.value
      if (isEditingSignature.value) {
        editSignature.value = userInfo.value.signature || ''
      }
    }

    const saveSignature = function () {
      userInfo.value.signature = editSignature.value.trim()
      // 更新本地存储
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
      showSuccessToast('个性签名修改成功')
      isEditingSignature.value = false
    }

    // 组件挂载时检查登录状态
    onMounted(() => {
      // 检查登录状态
      checkLoginStatus()

      // 如果已登录，保存设备信息并获取设备列表
      if (localStorage.getItem('access_token')) {
        handleLoginSuccess()
      }
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
      handleAvatarError,
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
      showLogoutConfirmModal,
      openLogoutConfirmModal,
      closeLogoutConfirmModal,
      confirmLogout,
      securityLevel,
      securityLevelText,
      showDeviceManagement,
      showDeviceManagementModal,
      closeDeviceManagementModal,
      devices,
      removeDevice,
      showNotificationSettings,
      showNotificationSettingsModal,
      closeNotificationSettingsModal,
      notificationSettings,
      saveNotificationSettings,
      showPrivacySettings,
      showPrivacySettingsModal,
      closePrivacySettingsModal,
      privacySettings,
      savePrivacySettings,
      exportUserData,
      deleteUserData,
      isEditingSignature,
      editSignature,
      toggleSignatureEdit,
      saveSignature
    }
  }
}
</script>

<style scoped>
@import '../../styles/home.css';
@import '../../styles/mine.css';
</style>

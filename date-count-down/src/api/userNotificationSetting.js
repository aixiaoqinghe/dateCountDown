// src/api/userNotificationSetting.js - 用户通知设置相关 API

import { get, put } from './request'

// 获取用户通知设置
export const getNotificationSettings = () => {
  return get('/api/notification/settings')
}

// 更新用户通知设置
export const updateNotificationSettings = (data) => {
  return put('/api/notification/settings', data)
}

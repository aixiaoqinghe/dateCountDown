// src/api/privacy.js - 隐私设置相关 API

import { get, put } from './request'

// 获取隐私设置
export const getPrivacySettings = () => {
  return get('/api/privacy/settings')
}

// 更新隐私设置
export const updatePrivacySettings = (data) => {
  return put('/api/privacy/settings', data)
}

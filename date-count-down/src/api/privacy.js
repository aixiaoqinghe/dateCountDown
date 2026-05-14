// src/privacy.js - 隐私设置相关 API

import { get, put } from './request'

// 获取隐私设置
export const getPrivacySettings = () => {
  return get('/privacy/settings')
}

// 更新隐私设置
export const updatePrivacySettings = (data) => {
  return put('/privacy/settings', data)
}

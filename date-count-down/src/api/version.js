// src/api/version.js - 版本管理相关 API

import { get, post, put, del } from './request'

// 获取版本列表
export const getVersionList = () => {
  return get('/api/version')
}

// 获取单个版本
export const getVersion = (id) => {
  return get(`/api/version/${id}`)
}

// 检查更新
export const checkUpdate = (currentVersion) => {
  return get('/api/version/check_update', { current_version: currentVersion })
}

// 创建版本（管理员）
export const createVersion = (data) => {
  return post('/api/version', data)
}

// 更新版本（管理员）
export const updateVersion = (id, data) => {
  return put(`/api/version/${id}`, data)
}

// 删除版本（管理员）
export const deleteVersion = (id) => {
  return del(`/api/version/${id}`)
}
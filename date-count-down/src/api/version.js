// src/api/version.js - 版本管理相关 API

import { get, post, put, del } from './request'

// 获取版本列表
export const getVersionList = () => {
  return get('/version')
}

// 获取单个版本
export const getVersion = (id) => {
  return get(`/version/${id}`)
}

// 检查更新
export const checkUpdate = (currentVersion) => {
  return get('/version/check_update', { current_version: currentVersion })
}

// 创建版本（管理员）
export const createVersion = (data) => {
  return post('/version', data)
}

// 更新版本（管理员）
export const updateVersion = (id, data) => {
  return put(`/version/${id}`, data)
}

// 删除版本（管理员）
export const deleteVersion = (id) => {
  return del(`/version/${id}`)
}
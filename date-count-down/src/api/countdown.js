// src/api/countdown.js - 倒计时相关 API

import { get, post, put, del } from './request'

// 获取倒计时列表
export const getCountdownList = () => {
  return get('/api/countdown')
}

// 获取单个倒计时
export const getCountdown = (id) => {
  return get(`/api/countdown/${id}`)
}

// 创建倒计时
export const createCountdown = (data) => {
  return post('/api/countdown', data)
}

// 更新倒计时
export const updateCountdown = (id, data) => {
  return put(`/api/countdown/${id}`, data)
}

// 删除倒计时
export const deleteCountdown = (id) => {
  return del(`/api/countdown/${id}`)
}

// 批量删除倒计时
export const batchDeleteCountdown = (ids) => {
  return post('/api/countdown/batch_delete', { ids })
}
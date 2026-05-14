// src/countdown.js - 倒计时相关 API

import { get, post, put, del } from './request'

// 获取倒计时列表
export const getCountdownList = () => {
  return get('/countdown')
}

// 获取单个倒计时
export const getCountdown = (id) => {
  return get(`/countdown/${id}`)
}

// 创建倒计时
export const createCountdown = (data) => {
  return post('/countdown', data)
}

// 更新倒计时
export const updateCountdown = (id, data) => {
  return put(`/countdown/${id}`, data)
}

// 删除倒计时
export const deleteCountdown = (id) => {
  return del(`/countdown/${id}`)
}

// 批量删除倒计时
export const batchDeleteCountdown = (ids) => {
  return post('/countdown/batch_delete', { ids })
}

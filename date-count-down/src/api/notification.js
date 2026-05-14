// src/api/notification.js - 通知相关 API

import { get, put, del } from './request'

// 获取通知列表
export const getNotificationList = () => {
  return get('/notification')
}

// 获取单个通知
export const getNotification = (id) => {
  return get(`/notification/${id}`)
}

// 标记通知为已读
export const markNotificationAsRead = (id) => {
  return put(`/notification/${id}/read`)
}

// 删除通知
export const deleteNotification = (id) => {
  return del(`/notification/${id}`)
}

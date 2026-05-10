// src/api/notification.js - 通知相关 API

import { get, put } from './request'

// 获取通知列表
export const getNotificationList = () => {
  return get('/api/notification')
}

// 获取单个通知
export const getNotification = (id) => {
  return get(`/api/notification/${id}`)
}

// 标记通知为已读
export const markNotificationAsRead = (id) => {
  return put(`/api/notification/${id}/read`)
}

// 删除通知
export const deleteNotification = (id) => {
  return fetch(`/api/notification/${id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`
    }
  })
}
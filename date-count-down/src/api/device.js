// src/api/device.js - 设备管理相关 API

import { get, post, del } from './request'

// 获取设备列表
export const getDeviceList = () => {
  return get('/api/devices')
}

// 保存当前设备信息
export const saveCurrentDevice = (data) => {
  return post('/api/devices/current', data)
}

// 删除设备
export const deleteDevice = (id, data) => {
  return fetch(`/api/devices/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify(data)
  })
}
// src/api/device.js - 设备管理相关 API

import { get, post, del } from './request'

// 获取设备列表
export const getDeviceList = () => {
  return get('/devices')
}

// 保存当前设备信息
export const saveCurrentDevice = (data) => {
  return post('/devices/current', data)
}

// 删除设备
export const deleteDevice = (id) => {
  return del(`/devices/${id}`)
}

// src/api/auth.js - 认证相关 API

import { post, put, get } from './request'

// 用户注册
export const register = (data) => {
  return post('/api/auth/register', data)
}

// 用户登录
export const login = (data) => {
  return post('/api/auth/login', data)
}

// 获取用户信息
export const getUserInfo = () => {
  return get('/api/auth/user')
}

// 修改密码
export const changePassword = (data) => {
  return post('/api/auth/change_password', data)
}

// 修改头像
export const updateAvatar = (formData) => {
  const token = localStorage.getItem('access_token')
  return fetch('/api/auth/avatar', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: formData
  })
}

// 修改昵称
export const updateNickname = (data) => {
  return put('/api/auth/user', data)
}

// 绑定/修改手机号
export const bindPhone = (data) => {
  return post('/api/auth/bind_phone', data)
}

export const changePhone = (data) => {
  return post('/api/auth/change_phone', data)
}

// 绑定/修改邮箱
export const bindEmail = (data) => {
  return post('/api/auth/bind_email', data)
}

export const changeEmail = (data) => {
  return post('/api/auth/change_email', data)
}

// 发送验证码
export const sendSmsCode = (data) => {
  return post('/api/verify/send_sms_code', data)
}

export const sendEmailCode = (data) => {
  return post('/api/verify/send_email_code', data)
}

// 验证验证码
export const verifySmsCode = (data) => {
  return post('/api/verify/verify_sms_code', data)
}

export const verifyEmailCode = (data) => {
  return post('/api/verify/verify_email_code', data)
}
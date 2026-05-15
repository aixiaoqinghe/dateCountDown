// src/auth.js - 认证相关 API

import { post, put, get } from './request'

// 用户注册
export const register = (data) => {
  return post('/auth/register', data)
}

// 用户登录
export const login = (data) => {
  return post('/auth/login', data)
}

// 获取用户信息
export const getUserInfo = () => {
  return get('/auth/user')
}

// 修改密码
export const changePassword = (data) => {
  return post('/auth/change_password', data)
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
  return put('/auth/user', data)
}

// 更新个性签名
export const updateSignature = (data) => {
  return put('/auth/user', data)
}

// 绑定/修改手机号
export const bindPhone = (data) => {
  return post('/auth/bind_phone', data)
}

export const changePhone = (data) => {
  return post('/auth/change_phone', data)
}

// 绑定/修改邮箱
export const bindEmail = (data) => {
  return post('/auth/bind_email', data)
}

export const changeEmail = (data) => {
  return post('/auth/change_email', data)
}

// 发送验证码
export const sendSmsCode = (data) => {
  return post('/verify/send_sms_code', data)
}

export const sendEmailCode = (data) => {
  return post('/verify/send_email_code', data)
}

// 验证验证码
export const verifySmsCode = (data) => {
  return post('/verify/verify_sms_code', data)
}

export const verifyEmailCode = (data) => {
  return post('/verify/verify_email_code', data)
}

// src/api/request.js - 统一请求封装

// 请求拦截器：在发送请求前做一些处理
const requestInterceptor = (config) => {
  // 添加 token 到请求头
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  
  // 设置默认 Content-Type
  if (!config.headers?.['Content-Type']) {
    config.headers = config.headers || {}
    config.headers['Content-Type'] = 'application/json'
  }
  
  console.log('请求配置:', config)
  return config
}

// 响应拦截器：统一处理响应
const responseInterceptor = async (response) => {
  const result = await response.json()
  
  // 统一错误处理
  if (!response.ok) {
    // 根据不同状态码处理
    switch (response.status) {
      case 401:
        // 未授权，清除本地存储并跳转到登录页
        localStorage.removeItem('access_token')
        localStorage.removeItem('userInfo')
        // 跳转到登录页
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
        throw new Error(result.message || '登录已过期，请重新登录')
        
      case 403:
        throw new Error(result.message || '无权访问')
        
      case 404:
        throw new Error(result.message || '资源不存在')
        
      case 500:
        throw new Error(result.message || '服务器内部错误')
        
      default:
        throw new Error(result.message || '请求失败')
    }
  }
  
  return result
}

// 错误处理函数
const errorHandler = (error) => {
  console.error('请求错误:', error)
  // 可以在这里统一显示错误提示
  if (error.message) {
    // 如果有 vant 的 toast，可以在这里调用
    if (window.showToast) {
      window.showToast(error.message)
    }
  }
  throw error
}

// 封装 fetch 请求
export const request = async (url, options = {}) => {
  try {
    // 应用请求拦截器
    const config = requestInterceptor({ url, ...options })
    
    // 发送请求
    const response = await fetch(config.url, config)
    
    // 应用响应拦截器
    return await responseInterceptor(response)
    
  } catch (error) {
    // 统一错误处理
    errorHandler(error)
    throw error
  }
}

// GET 请求
export const get = (url, params = {}) => {
  // 构建查询参数
  const queryString = new URLSearchParams(params).toString()
  const fullUrl = queryString ? `${url}?${queryString}` : url
  
  return request(fullUrl, { method: 'GET' })
}

// POST 请求
export const post = (url, data = {}) => {
  return request(url, {
    method: 'POST',
    body: JSON.stringify(data)
  })
}

// PUT 请求
export const put = (url, data = {}) => {
  return request(url, {
    method: 'PUT',
    body: JSON.stringify(data)
  })
}

// DELETE 请求
export const del = (url, params = {}) => {
  const queryString = new URLSearchParams(params).toString()
  const fullUrl = queryString ? `${url}?${queryString}` : url
  
  return request(fullUrl, { method: 'DELETE' })
}

export default {
  request,
  get,
  post,
  put,
  delete: del
}
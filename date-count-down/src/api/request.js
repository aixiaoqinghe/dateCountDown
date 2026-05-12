// src/api/request.js - 统一请求封装
import { requestCache } from '@/utils/requestCache.js'

// 后端 API 基础地址
const baseURL = 'https://aixiaoqinghe.pythonanywhere.com/api'

// 请求拦截器：在发送请求前做一些处理
const requestInterceptor = (config) => {
  // 添加 token 到请求头
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}` // 自动加 Token
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
          window.location.href = '/login' // 自动跳登录
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

// 封装 fetch 请求（带缓存支持）
export const request = async (url, options = {}) => {
  try {
    // 拼接完整的 API 地址
    const fullUrl = url.startsWith('http') ? url : `${baseURL}${url}`

    // 应用请求拦截器
    const config = requestInterceptor({ url: fullUrl, ...options })

    // ✅ GET请求启用缓存
    const method = (options.method || 'GET').toUpperCase()
    if (method === 'GET') {
      const cacheKey = `${config.url}_${JSON.stringify(options.body || {})}`

      // 检查缓存
      const cachedData = requestCache.get(cacheKey)
      if (cachedData) {
        console.log(`[API缓存命中] ${config.url}`)
        return cachedData
      }

      // 检查是否有正在进行的请求（请求合并）
      if (requestCache.hasPending(cacheKey)) {
        console.log(`[API请求合并] ${config.url}`)
        return requestCache.getPending(cacheKey)
      }

      // 创建请求Promise并添加到pending队列
      const requestPromise = (async () => {
        try {
          // 发送请求
          const response = await fetch(config.url, config)

          // 应用响应拦截器
          const result = await responseInterceptor(response)

          // ✅ GET请求成功后缓存结果（5分钟）
          requestCache.set(cacheKey, result, 5 * 60 * 1000)

          return result
        } catch (error) {
          throw error
        } finally {
          // 请求完成后移除pending状态
          requestCache.removePending(cacheKey)
        }
      })()

      // 添加到pending队列
      requestCache.addPending(cacheKey, requestPromise)
      return requestPromise
    }

    // 非GET请求直接发送
    const response = await fetch(config.url, config)
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

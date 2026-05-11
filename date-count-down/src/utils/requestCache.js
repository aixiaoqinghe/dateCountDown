// 请求缓存工具
// 用于防止重复请求和缓存API响应

class RequestCache {
  constructor() {
    this.cache = new Map()
    this.pending = new Map()
    this.defaultTTL = 5 * 60 * 1000 // 默认5分钟缓存
  }

  // 获取缓存数据
  get(key) {
    const item = this.cache.get(key)
    if (item && Date.now() < item.expireTime) {
      return item.data
    }
    // 缓存过期，移除
    if (item) {
      this.cache.delete(key)
    }
    return null
  }

  // 设置缓存数据
  set(key, data, ttl = this.defaultTTL) {
    this.cache.set(key, {
      data,
      expireTime: Date.now() + ttl
    })
  }

  // 检查是否有正在进行的请求
  hasPending(key) {
    return this.pending.has(key)
  }

  // 添加待处理请求
  addPending(key, promise) {
    this.pending.set(key, promise)
  }

  // 移除待处理请求
  removePending(key) {
    this.pending.delete(key)
  }

  // 获取待处理请求
  getPending(key) {
    return this.pending.get(key)
  }

  // 清除所有缓存
  clear() {
    this.cache.clear()
    this.pending.clear()
  }

  // 清除过期缓存
  cleanup() {
    const now = Date.now()
    for (const [key, item] of this.cache.entries()) {
      if (now >= item.expireTime) {
        this.cache.delete(key)
      }
    }
  }
}

// 创建全局请求缓存实例
export const requestCache = new RequestCache()

// 带缓存的fetch包装器
export async function cachedFetch(url, options = {}, ttl = 5 * 60 * 1000) {
  // 生成缓存key
  const key = `${url}_${JSON.stringify(options.body || {})}`
  
  // 先检查缓存
  const cachedData = requestCache.get(key)
  if (cachedData) {
    console.log(`[缓存命中] ${url}`)
    return cachedData
  }
  
  // 检查是否有正在进行的请求
  if (requestCache.hasPending(key)) {
    console.log(`[请求合并] ${url}`)
    return requestCache.getPending(key)
  }
  
  // 创建新请求
  const promise = fetch(url, options)
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      // 只缓存成功的响应
      requestCache.set(key, data, ttl)
      return data
    })
    .catch((error) => {
      console.error(`[请求失败] ${url}:`, error)
      throw error
    })
    .finally(() => {
      requestCache.removePending(key)
    })
  
  // 添加到待处理请求
  requestCache.addPending(key, promise)
  
  return promise
}

// 防抖请求（用于搜索等场景）
export function debouncedFetch(fn, delay = 300) {
  let timer = null
  return function (...args) {
    if (timer) {
      clearTimeout(timer)
    }
    return new Promise((resolve, reject) => {
      timer = setTimeout(() => {
        fn(...args).then(resolve).catch(reject)
      }, delay)
    })
  }
}

// 请求节流（用于频繁触发的请求）
export function throttledFetch(fn, limit = 1000) {
  let lastTime = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastTime >= limit) {
      lastTime = now
      return fn(...args)
    }
    return Promise.resolve(null)
  }
}
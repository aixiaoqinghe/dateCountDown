// 节流函数
export function throttle (fn, delay = 300) {
  let lastTime = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      lastTime = now
      return fn.apply(this, args)
    }
  }
}

// 防抖函数
export function debounce (fn, delay = 300) {
  let timer = null
  return function (...args) {
    if (timer) {
      clearTimeout(timer)
    }
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

// 请求缓存函数（防止重复请求）
export function requestCache (fn) {
  const cache = new Map()
  return async function (...args) {
    const key = JSON.stringify(args)
    if (cache.has(key)) {
      return cache.get(key)
    }
    const result = await fn.apply(this, args)
    cache.set(key, result)
    return result
  }
}

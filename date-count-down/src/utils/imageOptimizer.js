/**
 * 图片优化工具
 * 功能：压缩图片、转换为WebP格式、生成响应式图片
 */

/**
 * 压缩图片
 * @param {File} file - 原始图片文件
 * @param {number} quality - 压缩质量 (0-1)
 * @returns {Promise<Blob>} - 压缩后的图片Blob
 */
export const compressImage = (file, quality = 0.8) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()

    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        // 创建canvas
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')

        // 设置最大尺寸
        const maxWidth = 1200
        const maxHeight = 1200

        let width = img.width
        let height = img.height

        // 按比例缩小
        if (width > maxWidth) {
          height = (height * maxWidth) / width
          width = maxWidth
        }
        if (height > maxHeight) {
          width = (width * maxHeight) / height
          height = maxHeight
        }

        canvas.width = width
        canvas.height = height

        // 绘制图片
        ctx.drawImage(img, 0, 0, width, height)

        // 转换为Blob
        canvas.toBlob((blob) => {
          if (blob) {
            resolve(blob)
          } else {
            reject(new Error('图片压缩失败'))
          }
        }, 'image/jpeg', quality)
      }
      img.onerror = reject
      img.src = e.target.result
    }

    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

/**
 * 转换为WebP格式
 * @param {File} file - 原始图片文件
 * @param {number} quality - 压缩质量 (0-1)
 * @returns {Promise<Blob>} - WebP格式的图片Blob
 */
export const convertToWebP = (file, quality = 0.8) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()

    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')

        // 保持原始尺寸
        canvas.width = img.width
        canvas.height = img.height

        ctx.drawImage(img, 0, 0)

        // 转换为WebP
        canvas.toBlob((blob) => {
          if (blob) {
            resolve(blob)
          } else {
            // 如果浏览器不支持WebP，返回原始压缩图片
            compressImage(file, quality).then(resolve).catch(reject)
          }
        }, 'image/webp', quality)
      }
      img.onerror = reject
      img.src = e.target.result
    }

    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

/**
 * 生成响应式图片URL
 * @param {string} baseUrl - 基础图片URL
 * @param {number[]} widths - 不同宽度的图片尺寸
 * @returns {object} - 包含src和srcset的对象
 */
export const generateResponsiveImage = (baseUrl, widths = [400, 800, 1200]) => {
  const ext = baseUrl.split('.').pop()
  const basePath = baseUrl.replace(/\.[^/.]+$/, '')

  const srcset = widths.map(width => {
    return `${basePath}_${width}w.${ext} ${width}w`
  }).join(', ')

  return {
    src: `${basePath}_800w.${ext}`,
    srcset: srcset,
    sizes: '(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px'
  }
}

/**
 * 检查浏览器是否支持WebP
 * @returns {Promise<boolean>} - 是否支持WebP
 */
export const supportsWebP = () => {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => resolve(true)
    img.onerror = () => resolve(false)
    img.src = 'data:image/webp;base64,UklGRiIAAABXRUJQVlA4IBYAAAAwAQCdASoBAAEAAkA0JaQAA3AA/vuUAAA='
  })
}

/**
 * 优化图片上传
 * @param {File} file - 原始图片文件
 * @returns {Promise<File>} - 优化后的图片文件
 */
export const optimizeImageForUpload = async (file) => {
  // 检查是否支持WebP
  const canUseWebP = await supportsWebP()

  // 压缩并转换图片
  const optimizedBlob = canUseWebP
    ? await convertToWebP(file, 0.8)
    : await compressImage(file, 0.8)

  // 创建新的File对象
  const ext = canUseWebP ? 'webp' : 'jpg'
  const fileName = file.name.replace(/\.[^/.]+$/, '') + `.${ext}`

  return new File([optimizedBlob], fileName, {
    type: `image/${ext}`,
    lastModified: Date.now()
  })
}

export default {
  compressImage,
  convertToWebP,
  generateResponsiveImage,
  supportsWebP,
  optimizeImageForUpload
}

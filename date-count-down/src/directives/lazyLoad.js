// 图片懒加载指令
const lazyLoad = {
  mounted (el, binding) {
    // 创建观察器
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // 元素进入视口，加载图片
            el.src = binding.value
            // 停止观察
            observer.unobserve(el)
          }
        })
      },
      {
        rootMargin: '100px', // 提前100px加载
        threshold: 0.1
      }
    )

    // 开始观察元素
    observer.observe(el)

    // 保存观察器引用，便于销毁时清理
    el._lazyObserver = observer
  },
  unmounted (el) {
    // 组件销毁时清理观察器
    if (el._lazyObserver) {
      el._lazyObserver.disconnect()
    }
  }
}

export default lazyLoad

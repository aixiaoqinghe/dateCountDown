const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    }
  },
  // 添加代理配置
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 后端服务地址
        changeOrigin: true, // 支持跨域
        pathRewrite: {
          '^/api': '/api' // 路径重写
        }
      }
    }
  }
})

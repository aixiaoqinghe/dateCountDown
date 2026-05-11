const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  // ✅ 启用文件名哈希（用于缓存策略）
  filenameHashing: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    // ✅ 配置输出文件名带哈希
    output: {
      filename: 'js/[name].[contenthash:8].js',
      chunkFilename: 'js/[name].[contenthash:8].js'
    }
  },
  chainWebpack: (config) => {
    // ✅ 分割第三方依赖为单独的 chunk
    config.optimization.splitChunks({
      chunks: 'all',
      cacheGroups: {
        vendors: {
          test: /[\\/]node_modules[\\/]/,
          name: 'chunk-vendors',
          priority: -10
        },
        common: {
          name: 'chunk-common',
          minChunks: 2,
          priority: -20,
          reuseExistingChunk: true
        }
      }
    })

    // ✅ 压缩图片（仅生产环境）
    if (process.env.NODE_ENV === 'production') {
      config.module.rule('images')
        .use('image-webpack-loader')
        .loader('image-webpack-loader')
        .options({
          mozjpeg: { quality: 80 },
          optipng: { enabled: true },
          pngquant: { quality: [0.65, 0.90] },
          gifsicle: { interlaced: false }
        })
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
      },
      '/uploads': {
        target: 'http://localhost:5000', // 后端服务地址
        changeOrigin: true, // 支持跨域
        pathRewrite: {
          '^/uploads': '/uploads' // 路径重写
        }
      }
    },
    // ✅ 配置静态资源缓存头
    static: {
      cacheControl: 'public, max-age=31536000, immutable'
    }
  }
})
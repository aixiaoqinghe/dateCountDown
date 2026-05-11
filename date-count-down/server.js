const express = require('express')
const path = require('path')
const compression = require('compression')

const app = express()
const PORT = process.env.PORT || 8080

// ✅ 启用 gzip 压缩
app.use(compression())

// ✅ 配置静态资源缓存
app.use('/js', express.static(path.join(__dirname, 'dist/js'), {
  maxAge: '1y',
  immutable: true
}))

app.use('/css', express.static(path.join(__dirname, 'dist/css'), {
  maxAge: '1y',
  immutable: true
}))

app.use('/img', express.static(path.join(__dirname, 'dist/img'), {
  maxAge: '1y',
  immutable: true
}))

// ✅ 其他静态资源设置较短缓存
app.use(express.static(path.join(__dirname, 'dist'), {
  maxAge: '1d'
}))

// ✅ SPA 路由处理 - 使用中间件方式
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'))
})

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`)
})

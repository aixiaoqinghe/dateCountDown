# dateCountDown

一个功能强大的倒计时应用，支持用户认证、倒计时管理和个性化设置

**主要特点**：
- 🔐 安全的用户认证系统（JWT + 验证码）
- ⏱️ 灵活的倒计时管理（创建、编辑、删除）
- 🎨 个性化设置（头像、签名、主题）
- 🔄 多设备数据同步
- 📱 响应式设计，支持各种设备

🌐 **在线体验**: http://8.134.150.161



## 🎯 功能特性

### 📱 响应式布局模块
- **多设备适配** - 完美适配手机、平板、电脑等不同屏幕尺寸
- **弹性布局** - 页面元素自动调整以适应不同屏幕
- **触摸友好** - 移动端优化的交互体验
- **响应式图片** - 图片自动缩放以适应不同设备

### 👤 用户认证模块
- **用户注册** - 支持邮箱注册，需完成图形验证码验证
- **图形验证码** - 注册时需输入随机生成的图形验证码，防止恶意注册
- **用户登录** - 支持用户名密码登录，支持记住登录状态
- **密码修改** - 支持通过邮箱验证或手机号验证修改密码
- **邮箱修改** - 支持更换绑定邮箱，需验证绑定邮箱
- **JWT 认证** - 安全的身份验证机制，token 有效期自动管理

### ⏱️ 倒计时管理模块
- **创建倒计时** - 自定义标题、目标日期、描述信息、背景图片
- **编辑倒计时** - 支持修改已有倒计时信息
- **删除倒计时** - 支持删除不需要的倒计时
- **实时显示** - 天、时、分、秒实时倒计时显示
- **列表展示** - 美观的倒计时卡片列表，支持按时间排序

### 📱 设备管理模块
- **登录设备管理** - 查看当前登录的近期设备列表
- **设备信息展示** - 显示设备类型、登录时间、登录地点、IP地址
- **安全提醒** - 新设备登录时发送通知提醒

### 🎨 个性化设置模块
- **头像上传** - 支持自定义个人头像，支持多种图片格式
- **个性签名** - 支持编辑个性签名，字数限制提示
- **主题设置** - 支持切换深色/浅色主题
- **字体设置** - 支持调整字体大小和字体样式

### 🔔 通知系统
- **通知设置** - 支持开启/关闭各类通知
- **提醒频率** - 支持设置通知频率（实时/每日/每周）
- **声音提醒** - 支持开启/关闭通知声音
- **弹窗提醒** - 倒计时到期时弹出提醒窗口


## 🎬 功能演示

### 用户登录
<img width="2543" height="1406" alt="login_demo" src="https://github.com/user-attachments/assets/4b3c1d6f-34fd-468d-a2eb-717bcc5c4f26" />

### 添加倒计时
<img width="2543" height="1406" alt="add_countdown_demo" src="https://github.com/user-attachments/assets/6aff6191-f5b1-4765-985a-067d09526f3d" />


### 实时倒计时


### 个性签名设置
<img width="2543" height="1406" alt="signature_demo" src="https://github.com/user-attachments/assets/cf5f2f45-76e8-401a-bf08-f152da199fb8" />

### 主题切换


### 修改密码
<img width="2543" height="1406" alt="modify_pwd_demo" src="https://github.com/user-attachments/assets/63ec2540-3a91-46cc-8a96-161966da6429" />



## 📋 版本规划

### ✅ v1.0.0 - 已发布
- 用户注册与登录功能（图形验证码验证）
- 倒计时基础管理功能（创建、编辑、删除）
- 个性化设置（头像、个性签名）
- 主题切换功能（深色/浅色模式）
- 字体设置功能（字体大小、样式调整）
- 登录设备管理（查看设备列表）
- 密码修改与邮箱修改功能
- 多设备数据同步
- 响应式设计（适配手机、平板、电脑）

### 🔄 v1.1.0 - 开发中
- 通知设置界面实现
- 倒计时到期提醒功能
- 通知偏好配置（声音、弹窗开关）
- 手机号验证功能

### 📅 v2.0.0 - 计划中
- 消息通知功能
- 远程退出登录设备
- 导出个人数据（Excel/CSV）
- 版本更新功能（真实更新，非模拟）
- 倒计时任务分模块管理
- 商城页面

### 💡 v3.0.0 - 规划中
- 好友系统（我的好友模式）
- 二维码添加好友功能
- 隐私设置（倒计时任务可见性控制）
- 数据分析与统计



## 🛠️ 技术栈

### 前端
| 技术 | 版本 | 说明 |
|------|:----:|------|
| Vue | 3.x | 渐进式 JavaScript 框架 |
| Vite | 6.x | 快速前端构建 |
| Tailwind CSS | 3.x | 实用优先的 CSS 框架（样式处理） |
|Vant|4.x|移动端UI组件库|
|Lucide Icons|最新|精美图标库（图标展示）|
|ESLint|最新|代码规范检查工具|

### 后端
| 技术 | 版本 | 说明 |
|------|:----:|------|
| Flask | 2.x | Python Web 框架 |
|Flask-JWT-Extended|4.x|JWT认证扩展|
| SQLAlchemy | 2.x | ORM 数据库工具 |
| MySQL | 8.0+ | 关系型数据库 |

### 部署
| 技术 | 版本 | 说明 |
|------|:----:|------|
| Nginx | 1.18+ | Web 服务器（反向代理） |
|Gunicorn|最新|WSGI应用服务器（运行Flask）|
| 阿里云 ECS | - | 云服务器 |

访问地址：http://8.134.150.161



## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+


### 后端启动

**方式一：快速启动（适合已有环境）**
1.激活虚拟环境
```
source /root/dateCountDown/venv/bin/activate
```

2.进入后端项目
```
cd ~/dateCountDown/dateCountDown/date-count-down/backend
```

3.启动服务
```
python run.py
```

服务将在 http://127.0.0.1:5000 运行


**方式二：完整部署（适合首次部署或他人使用）**
1.创建虚拟环境（仅仅是第一次使用要创建，首次创建之后，后续都不需要创建，直接进行第2步激活虚拟环境）
```
python -m venv venv
```

2.激活虚拟环境
```
source venv/bin/activate
```

3.安装基础依赖
```
pip install -r requirements.txt
```

4.安装额外依赖（根据项目需求）
```
pip install flask flask-jwt-extended flask-sqlalchemy pymysql python-dotenv flask-cors
```
如果还有缺少的依赖，使用`pip install 缺少的依赖`即可

5.配置数据库（编辑config.py）
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@localhost/数据库名'
```

6.启动服务
```
python run.py
```


### 前端启动

1.进入项目根目录
```
cd ~/dateCountDown/dateCountDown/date-count-down
```

2.安装基础依赖
```
npm install
```

3.安装额外依赖
```
npm install vant lucide-vue-next axios vue-router
```

4.代码规范检查
```
npm run lint
```

5.开发模式（热更新）
```
npm run serve
```
服务器将在 http://localhost:8080 运行（如果8080端口被占用，可能是8081或者8082等）
在浏览器中访问该网址即可查看应用

6.生产构建
```
npm run build
```
构建产物输出到dist目录


### 📋 常用命令

| 操作 | 命令 |
|------|------|
| 激活虚拟环境 | `source venv/bin/activate` |
| 关闭虚拟环境 | `deactivate` |
| 安装后端依赖 | `pip install -r requirements.txt` |
| 启动后端 | `python run.py` |
| 安装前端依赖 | `npm install` |
| 代码规范检查 | `npm run lint` |
| 启动前端 | `npm run serve` |
| 生产构建 | `npm run build` |



## 🔌 API 接口文档

### 📦 统一请求封装

项目使用 `src/api/request.js` 进行统一的 HTTP 请求封装，具有以下特性：

| 特性 | 说明 |
|------|------|
| **请求拦截器** | 自动添加 JWT Token 到请求头 |
| **响应拦截器** | 统一错误处理，401 自动跳转到登录页 |
| **GET 请求缓存** | 启用 5 分钟缓存机制，支持请求合并 |
| **统一错误处理** | 支持 Toast 提示（需引入 vant） |

**请求方法封装**：

| 方法 | 函数 | 说明 |
|------|------|------|
| GET | `get(url, params)` | 发送 GET 请求，自动拼接查询参数 |
| POST | `post(url, data)` | 发送 POST 请求，数据 JSON 序列化 |
| PUT | `put(url, data)` | 发送 PUT 请求，数据 JSON 序列化 |
| DELETE | `del(url, params)` | 发送 DELETE 请求 |

---

### 👤用户认证模块接口

| API 路径 | 方法 | 函数名 | 说明 |
|----------|------|--------|------|
| `/auth/register` | POST | `register(data)` | 用户注册 |
| `/auth/login` | POST | `login(data)` | 用户登录 |
| `/auth/user` | GET | `getUserInfo()` | 获取用户信息 |
| `/auth/user` | PUT | `updateNickname(data)` | 更新用户资料（昵称等） |
| `/auth/user` | PUT | `updateSignature(data)` | 更新个性签名 |
| `/auth/change_password` | POST | `changePassword(data)` | 修改密码 |
| `/auth/avatar` | POST | `updateAvatar(formData)` | 上传头像（multipart/form-data） |
| `/auth/bind_phone` | POST | `bindPhone(data)` | 绑定手机号 |
| `/auth/change_phone` | POST | `changePhone(data)` | 修改手机号 |
| `/auth/bind_email` | POST | `bindEmail(data)` | 绑定邮箱 |
| `/auth/change_email` | POST | `changeEmail(data)` | 修改邮箱 |


### ⏱️倒计时管理接口

| API 路径 | 方法 | 函数名 | 说明 |
|----------|------|--------|------|
| `/countdown` | GET | `getCountdownList()` | 获取倒计时列表 |
| `/countdown/:id` | GET | `getCountdown(id)` | 获取单个倒计时 |
| `/countdown` | POST | `createCountdown(data)` | 创建倒计时 |
| `/countdown/:id` | PUT | `updateCountdown(id, data)` | 更新倒计时 |
| `/countdown/:id` | DELETE | `deleteCountdown(id)` | 删除倒计时 |
| `/countdown/batch_delete` | POST | `batchDeleteCountdown(ids)` | 批量删除倒计时 |


### 📣消息通知接口

| API 路径 | 方法 | 函数名 | 说明 |
|----------|------|--------|------|
| `/notification` | GET | `getNotificationList()` | 获取通知列表 |
| `/notification/:id` | GET | `getNotification(id)` | 获取单个通知 |
| `/notification/:id/read` | PUT | `markNotificationAsRead(id)` | 标记通知为已读 |
| `/notification/:id` | DELETE | `deleteNotification(id)` | 删除通知 |

---

### 🔔用户通知设置接口

| API 路径 | 方法 | 函数名 | 说明 |
|----------|------|--------|------|
| `/notification/settings` | GET | `getNotificationSettings()` | 获取用户通知设置 |
| `/notification/settings` | PUT | `updateNotificationSettings(data)` | 更新用户通知设置 |

---

### 📱设备管理接口

| API 路径 | 方法 | 函数名 | 说明 |
|----------|------|--------|------|
| `/devices` | GET | `getDeviceList()` | 获取设备列表 |
| `/devices/current` | POST | `saveCurrentDevice(data)` | 保存当前设备信息 |
| `/devices/:id` | DELETE | `deleteDevice(id)` | 删除设备 |

---

### 🛡️隐私设置接口

| API 路径 | 方法 | 函数名 | 说明 |
|----------|------|--------|------|
| `/privacy/settings` | GET | `getPrivacySettings()` | 获取隐私设置 |
| `/privacy/settings` | PUT | `updatePrivacySettings(data)` | 更新隐私设置 |

---

### 🔄版本管理接口

| API 路径 | 方法 | 函数名 | 说明 |
|----------|------|--------|------|
| `/version` | GET | `getVersionList()` | 获取版本列表 |
| `/version/:id` | GET | `getVersion(id)` | 获取单个版本 |
| `/version/check_update` | GET | `checkUpdate(currentVersion)` | 检查更新 |
| `/version` | POST | `createVersion(data)` | 创建版本（管理员） |
| `/version/:id` | PUT | `updateVersion(id, data)` | 更新版本（管理员） |
| `/version/:id` | DELETE | `deleteVersion(id)` | 删除版本（管理员） |


### 🔴错误处理

| HTTP 状态码 | 处理方式 |
|-------------|----------|
| 401 | 清除 Token，自动跳转到登录页 |
| 403 | 抛出错误："无权访问" |
| 404 | 抛出错误："资源不存在" |
| 500 | 抛出错误："服务器内部错误" |

---

### 认证机制

- **JWT Token**：登录成功后返回 `access_token`，存储在 `localStorage`
- **自动携带**：请求拦截器自动添加 `Authorization: Bearer {token}` 头
- **过期处理**：401 响应自动清除 Token 并跳转登录页



## 📁 项目结构

```
date-count-down/
├── backend/                    # 后端代码
│   ├── app/                   # Flask 应用核心
│   │   ├── __init__.py        # 应用初始化
│   │   ├── routes/            # API 路由定义
│   │   │   ├── auth.py        # 认证相关接口
│   │   │   ├── countdown.py   # 倒计时相关接口
│   │   │   ├── device.py      # 设备管理接口
│   │   │   ├── notification.py # 通知设置接口
│   │   │   ├── privacy.py     # 隐私设置接口
│   │   │   └── version.py     # 版本管理接口
│   │   ├── models/            # 数据库模型
│   │   │   ├── user.py        # 用户模型
│   │   │   └── countdown.py   # 倒计时模型
│   │   ├── utils/             # 工具函数
│   │   └── config.py          # 配置文件
│   ├── requirements.txt       # Python 依赖列表
│   └── run.py                 # 应用启动脚本
├── src/                       # 前端代码
│   ├── components/            # Vue 组件
│   │   ├── CountdownCard.vue  # 倒计时卡片组件
│   │   ├── AvatarUpload.vue   # 头像上传组件
│   │   └── NotificationPanel.vue # 通知面板组件
│   ├── views/                 # 页面视图
│   │   ├── home/              # 首页相关视图
│   │   │   └── mine.vue       # 个人中心页面
│   │   └── auth/              # 认证相关视图
│   ├── api/                   # API 封装
│   │   ├── request.js         # 统一请求封装
│   │   ├── auth.js            # 认证 API
│   │   └── countdown.js       # 倒计时 API
│   ├── utils/                 # 工具函数
│   ├── App.vue                # 根组件
│   └── main.js                # 入口文件
├── dist/                      # 构建产物
├── index.html                 # HTML 模板
├── package.json               # Node.js 依赖配置
├── vite.config.js             # Vite 配置
├── tailwind.config.js         # Tailwind CSS 配置
├── README.md                  # 英文说明文档
└── README_zh.md               # 中文说明文档
```



## 📦 部署说明

### Nginx 配置示例
```nginx
server {
    listen 80;
    server_name 8.134.150.161;

    # 前端静态文件
    location / {
        root /var/www/html/datecountdown;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 上传文件
    location /uploads/ {
        alias /var/www/uploads/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 错误页面
    error_page 404 /index.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```



### 后端部署

使用 Gunicorn 启动后端（确保进入了虚拟环境）

```bash
gunicorn -w 4 -b 127.0.0.1:5000 run:app
```

如果没有进入虚拟环境，需要先激活
```
cd ~/dateCountDown/dateCountDown/date-count-down/backend
source /root/dateCountDown/venv/bin/activate
gunicorn -w 4 -b 127.0.0.1:5000 run:app
```

### 前端部署
```
# 构建并部署前端
npm run build
cp -r dist/* /var/www/html/datecountdown
```

### 数据库配置

确保 `backend/config.py` 中配置正确的数据库连接：
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@localhost/数据库名'
```



## 🛠️ 故障排除

### 常见问题

**Q: 前端无法连接后端？**
- 检查后端服务是否启动：`ps aux | grep python`
- 检查端口是否开放：`netstat -tlnp | grep 5000`
- 检查防火墙设置

**Q: 数据库连接失败？**
- 确保 MySQL 服务运行：`systemctl status mysql`
- 检查 `backend/.env` 文件中的数据库配置
- 确保数据库用户权限正确

**Q: 静态资源无法加载？**
- 检查 Nginx 配置中的 `root` 路径
- 确保 `dist` 目录正确部署

**Q: 验证码不显示？**
- 检查后端日志：`cat backend/app.log`
- 确保 Pillow 库已安装：`pip install pillow`



## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交代码规范

- 代码风格：前端遵循 ESLint 规范，后端遵循 PEP8 规范
- 提交信息：使用英文描述，格式为 `[类型] 描述`
  - `[feat]` - 新功能
  - `[fix]` - 修复 Bug
  - `[docs]` - 文档更新
  - `[refactor]` - 代码重构

### 开发流程

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/xxx`
3. 提交代码：`git commit -m "[feat] 添加 xxx 功能"`
4. 推送到分支：`git push origin feature/xxx`
5. 创建 Pull Request



## 📄 许可证

MIT License

MIT License

Copyright (c) 2026 dateCountDown

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



## 📧 联系方式

- 邮箱: axiaoqinghe@163.com
- 项目地址: [GitHub Repository](https://github.com/aixiaoqinghe/dateCountDown)
- 在线体验: http://8.134.150.161

如果对项目有什么建议，或者错误，欢迎提出，感谢您的支持😊。



  

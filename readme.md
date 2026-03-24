# 二次元风格博客技术文档
打算自己写个博客博客项目练练手，并把原来博客的东西都搬过去，先把仓库和前端写了

### 项目基本信息

- **项目名称**：ACG Blog（二次元风格博客）
- **项目简介**：基于 **FastAPI** 与 **Vue 3** 的前后端分离博客系统，主打二次元视觉体验与高性能响应。支持 Markdown 文章发布、动态看板娘、访问量统计、热搜排行、深色模式切换等特色功能。
- **技术栈概览**：
  - 后端：Python + FastAPI + SupaBase + Tortoise‑ORM + Redis + JWT
  - 前端：Vue 3 (Vite) + Pinia + Naive UI + Tailwind CSS + GSAP
- **系统架构**：**B/S 架构**（Browser/Server，浏览器/服务器架构）
  - 前端：单页应用（SPA）运行于浏览器
  - 后端：RESTful API 服务器
  - 通信协议：HTTP/HTTPS + JSON
- **后端架构模式**：**类 MVC 模式**
  - **Model（模型层）**：`models/` 目录，Tortoise-ORM 数据模型定义
  - **View（视图层）**：`api/endpoints/` 目录，FastAPI 路由返回 JSON 响应
  - **Controller（控制器层）**：`api/endpoints/` 中的路由处理函数，协调业务逻辑
  - **Service（服务层）**：`services/` 目录，封装核心业务（如看板娘互动、统计逻辑）
  - **Schema（数据传输层）**：`schemas/` 目录，Pydantic 模型校验请求与响应
  - **CRUD（数据操作层）**：`crud/` 目录，封装数据库增删改查逻辑，辅助 Model 层
  - **Core（核心配置）**：`core/` 目录，管理环境变量、日志、JWT 安全等基础设施
- **开发状态**：规划中

> 详细技术选型及项目结构请参见下文。

### 后端技术栈

| **模块**       | **技术选型**          | **说明**                                                     |
| -------------- | --------------------- | ------------------------------------------------------------ |
| **核心框架**   | **FastAPI**           | 高性能、原生异步（Async），满足二次元素材（图片/视频）的高并发加载需求。 |
| **数据库**     | **SupaBace**          | **内置 Auth**，支持第三方登录 (Github/Google)                |
| **ORM (异步)** | **Tortoise-ORM**      | 语法类似 Django，且原生支持异步操作。                        |
| **缓存/任务**  | **Redis**             | 用于文章点击量统计、热搜排行以及 Session 存储。              |
| **认证**       | **JWT (python-jose)** | 无状态认证，方便前后端分离部署。                             |
| **数据校验**   | **Pydantic v2**       | 确保前端传来的数据不会让后端“炸掉”。                         |
| **日志**       | **Loguru**            | 极简且强大的异步日志处理，便于排错                           |

###  前端技术栈 (The Visuals)

| **模块**      | **技术选型**     | **说明**                                                     |
| ------------- | ---------------- | ------------------------------------------------------------ |
| **框架**      | **Vue 3 (Vite)** | 组合式 API (Script Setup) 开发体验极佳，构建速度快。         |
| **状态管理**  | **Pinia**        | 轻量、简洁，存储用户偏好（如：深色/浅色模式、看板娘状态）。  |
| **UI 组件库** | **Naive UI**     | 设计感极强，配置主题非常自由，适合定制二次元配色。           |
| **样式引擎**  | **Tailwind CSS** | 极其方便编写自定义 UI。你可以轻松实现“毛玻璃”、“卡片悬浮”等特效。 |
| **编辑器**    | **V-MD-Editor**  | 基于 Vue 3 的 Markdown 编辑器，支持预览、代码高亮和 LaTeX 公式。 |
| **动画库**    | **GSAP**         | 强大的动效库。二次元风格需要细腻的入场和交互动画。           |

### 预计项目结构

```bash
acg-blog/
├── backend/                # FastAPI 后端项目
│   ├── app/
│   │   ├── api/            # 接口层 (v1, v2...)
│   │   │   ├── endpoints/  # 具体业务接口 (posts.py, users.py, etc.)
│   │   │   └── api.py      # 路由汇总
│   │   ├── core/           # 核心配置
│   │   │   ├── config.py   # 环境变量与全局配置
│   │   │   ├── logger.py   # 日志拦截与配置
│   │   │   └── security.py # JWT 与权限相关
│   │   ├── crud/           # 数据库增删改查逻辑
│   │   ├── db/             # 数据库连接与初始化
│   │   ├── models/         # Tortoise-ORM 数据库模型
│   │   ├── schemas/        # Pydantic 数据验证模型
│   │   ├── services/       # 业务服务逻辑 (如：看板娘互动 API)
│   │   └── main.py         # 后端入口
│   ├── logs/               # 日志存储目录 (自动生成 .log 文件)
│   ├── static/             # 静态资源 (用户上传的插图、头像)
│   ├── tests/              # 测试用例
│   ├── .env                # 敏感配置文件
│   ├── pyproject.toml      # Poetry 配置或使用 requirements
│   └── requirements.txt    # 依赖清单
├── frontend/               # Vue 3 前端项目 (Vite)
│   ├── public/             # 公共静态资源 (Live2D 模型、Favicon)
│   ├── src/
│   │   ├── api/            # Axios 接口封装
│   │   ├── assets/         # 样式、二次元字体、插画
│   │   ├── components/     # 组件 (看板娘、播放器、卡片)
│   │   ├── router/         # 路由配置
│   │   ├── store/          # Pinia 状态管理
│   │   ├── views/          # 页面布局 (首页、文章页、归档)
│   │   ├── App.vue         # 根组件
│   │   └── main.ts         # 前端入口
│   ├── tailwind.config.js  # Tailwind CSS 配置
│   └── package.json        # 前端依赖
├── docker-compose.yml      # 全栈 Docker 编排
└── README.md
```

### 后端requirements

```bash
# Web 框架 
fastapi==0.110.0
uvicorn[standard]==0.27.1

# 数据库与异步 ORM
tortoise-orm==0.20.0
aerich==0.7.2              # 数据库迁移工具
asyncpg==0.29.0            # PostgreSQL 驱动
aioredis==2.0.1            # Redis 驱动 

# 日志系统
loguru==0.7.2              # 极简且强大的异步日志处理

# 配置与安全
pydantic[email]==2.6.3      # 包含 Email 校验
pydantic-settings==2.2.1   # 处理 .env 环境变量
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4      # 密码哈希

# 业务
python-multipart==0.0.9     # 处理表单与文件上传
mistune==3.0.2              # 快速 Markdown 解析
pillow==10.2.0              # 处理图片 
httpx==0.27.0               # 异步 HTTP 请求 

# 开发与部署
python-dotenv==1.0.1
gunicorn==21.2.0           # 生产环境容器部署使用
```


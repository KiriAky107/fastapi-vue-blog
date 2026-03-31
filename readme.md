# ACG Blog - 二次元风格博客系统

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.110-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Vue-3.5-brightgreen.svg" alt="Vue">
  <img src="https://img.shields.io/badge/TypeScript-5.9-blue.svg" alt="TypeScript">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
</p>

基于 **FastAPI** 与 **Vue 3** 的前后端分离博客系统，主打二次元视觉体验与高性能响应。支持 Markdown 文章发布、访问量统计、分类标签管理、深色模式切换等功能。

## 技术栈

### 后端
| 技术 | 说明 |
|------|------|
| FastAPI | 高性能异步 Web 框架 |
| Tortoise-ORM | 异步 ORM，支持 PostgreSQL |
| PostgreSQL | 关系型数据库 |
| Redis | 缓存与会话存储 |
| JWT | 无状态身份认证 |
| Pydantic | 数据验证 |
| Loguru | 日志处理 |

### 前端
| 技术 | 说明 |
|------|------|
| Vue 3 | 组合式 API (Script Setup) |
| Vite | 快速构建工具 |
| TypeScript | 类型安全 |
| Pinia | 状态管理 |
| Naive UI | UI 组件库 |
| Tailwind CSS | 样式引擎 |
| Axios | HTTP 客户端 |

## 项目结构

```
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/endpoints/    # API 端点 (auth, posts, comments, users)
│   │   ├── core/             # 核心配置 (config, security, database, logger)
│   │   ├── crud/             # 数据库增删改查
│   │   ├── models/           # Tortoise-ORM 数据模型
│   │   ├── schemas/          # Pydantic 数据验证模型
│   │   └── main.py           # 应用入口
│   ├── Dockerfile             # 后端容器配置
│   ├── schema.sql             # 数据库建表脚本
│   └── requirements.txt       # Python 依赖
│
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── api/              # Axios 接口封装
│   │   ├── components/      # 公共组件
│   │   ├── views/           # 页面视图
│   │   ├── store/           # Pinia 状态管理
│   │   ├── router/          # 路由配置
│   │   └── types/           # TypeScript 类型定义
│   ├── Dockerfile            # 前端容器配置
│   └── nginx.conf            # Nginx 配置
│
├── docker-compose.yml        # Docker 编排
├── schema.sql                # 数据库建表脚本
└── docker-deploy.md          # 部署文档
```

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+ (可选)

### 本地开发

**1. 克隆项目**
```bash
git clone <repository-url>
cd acg-blog
```

**2. 启动后端**
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env  # 修改数据库连接信息

# 初始化数据库 (确保 PostgreSQL 运行中)
psql -U postgres -c "CREATE DATABASE acg_blog;"
psql -U postgres -d acg_blog -f schema.sql

# 启动服务
uvicorn main:app --reload --port 8000
```

**3. 启动前端**
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**4. 访问应用**
- 前端: http://localhost:5173
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### Docker 部署

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

访问 http://localhost 即可使用。

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/v1/auth/register | 用户注册 |
| POST | /api/v1/auth/login | 用户登录 |
| POST | /api/v1/auth/refresh | 刷新 Token |
| GET | /api/v1/auth/me | 获取当前用户 |
| GET | /api/v1/posts | 获取文章列表 |
| GET | /api/v1/posts/{id} | 获取文章详情 |
| POST | /api/v1/posts | 创建文章 |
| PUT | /api/v1/posts/{id} | 更新文章 |
| DELETE | /api/v1/posts/{id} | 删除文章 |
| GET | /api/v1/categories | 获取分类列表 |
| GET | /api/v1/tags | 获取标签列表 |
| GET | /api/v1/comments/post/{id} | 获取文章评论 |

## 默认账户

- 用户名: `admin`
- 邮箱: `admin@acgblog.com`
- 密码: `admin123`

**请在部署后立即修改管理员密码！**

## 功能特性

- [x] 用户认证 (JWT)
- [x] 文章管理 (CRUD)
- [x] 分类与标签
- [x] Markdown 编辑器
- [x] 评论系统
- [x] 浏览量统计
- [x] 深色/浅色模式
- [x] 响应式设计
- [x] Docker 部署

## 开发说明

### 前端组件
- `Navbar.vue` - 顶部导航栏
- `Hero.vue` - 首页横幅
- `PostCard.vue` - 文章卡片
- `Sidebar.vue` - 侧边栏
- `Footer.vue` - 页脚

### 管理后台
- `/admin/dashboard` - 仪表盘
- `/admin/posts` - 文章管理
- `/admin/categories` - 分类管理
- `/admin/tags` - 标签管理

## License

MIT License

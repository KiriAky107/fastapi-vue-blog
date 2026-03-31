# Docker 部署指南

## 快速启动

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 服务地址

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

## 初始化数据库

首次启动时，数据库会自动创建表结构和初始数据。

管理员账户：
- 用户名: `admin`
- 邮箱: `admin@acgblog.com`
- 密码: `admin123`

**重要**: 请在部署后修改管理员密码！

## 常用命令

```bash
# 重新构建镜像
docker-compose build --no-cache

# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 进入后端容器
docker exec -it acg_blog_backend sh

# 进入数据库
docker exec -it acg_blog_db psql -U postgres -d acg_blog
```

## 生产环境部署

1. 修改 `backend/.env.production` 中的配置：
   - `SECRET_KEY` - 使用随机字符串
   - `BACKEND_CORS_ORIGINS` - 改为你的域名

2. 修改 `docker-compose.yml` 中的端口映射（移除端口暴露，仅通过 nginx 反向代理）

3. 使用 Nginx 或 Traefik 等反向代理配置 HTTPS

4. 定期备份数据库：
   ```bash
   docker exec acg_blog_db pg_dump -U postgres acg_blog > backup.sql
   ```

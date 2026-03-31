-- ACG Blog 数据库建表脚本
-- PostgreSQL
-- 运行前请先创建数据库: CREATE DATABASE acg_blog;

-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==================== 用户表 ====================
CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "username" VARCHAR(50) UNIQUE NOT NULL,
    "email" VARCHAR(255) UNIQUE NOT NULL,
    "password_hash" VARCHAR(255) NOT NULL,
    "avatar" VARCHAR(500),
    "bio" TEXT,
    "is_active" BOOLEAN DEFAULT TRUE,
    "is_superuser" BOOLEAN DEFAULT FALSE,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==================== 分类表 ====================
CREATE TABLE IF NOT EXISTS "categories" (
    "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "name" VARCHAR(50) UNIQUE NOT NULL,
    "slug" VARCHAR(50) UNIQUE NOT NULL,
    "description" TEXT,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==================== 标签表 ====================
CREATE TABLE IF NOT EXISTS "tags" (
    "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "name" VARCHAR(50) UNIQUE NOT NULL,
    "slug" VARCHAR(50) UNIQUE NOT NULL,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==================== 文章表 ====================
CREATE TABLE IF NOT EXISTS "posts" (
    "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "title" VARCHAR(200) NOT NULL,
    "slug" VARCHAR(200) UNIQUE NOT NULL,
    "content" TEXT NOT NULL,
    "summary" TEXT,
    "cover_image" VARCHAR(500),

    -- 外键关联
    "author_id" UUID NOT NULL REFERENCES "users"("id") ON DELETE CASCADE,
    "category_id" UUID REFERENCES "categories"("id") ON DELETE SET NULL,

    -- 统计数据
    "view_count" INTEGER DEFAULT 0,
    "like_count" INTEGER DEFAULT 0,
    "comment_count" INTEGER DEFAULT 0,

    -- 状态: draft/published/archived
    "status" VARCHAR(20) DEFAULT 'draft',

    -- SEO
    "meta_title" VARCHAR(200),
    "meta_description" TEXT,

    -- 时间戳
    "published_at" TIMESTAMP,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS "idx_posts_status_published_at" ON "posts"("status", "published_at");
CREATE INDEX IF NOT EXISTS "idx_posts_author_status" ON "posts"("author_id", "status");

-- ==================== 文章标签关联表 ====================
CREATE TABLE IF NOT EXISTS "post_tags" (
    "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "post_id" UUID NOT NULL REFERENCES "posts"("id") ON DELETE CASCADE,
    "tag_id" UUID NOT NULL REFERENCES "tags"("id") ON DELETE CASCADE,
    UNIQUE("post_id", "tag_id")
);

-- ==================== 评论表 ====================
CREATE TABLE IF NOT EXISTS "comments" (
    "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "content" TEXT NOT NULL,
    "is_approved" BOOLEAN DEFAULT TRUE,

    -- 外键关联
    "author_id" UUID NOT NULL REFERENCES "users"("id") ON DELETE CASCADE,
    "post_id" UUID NOT NULL REFERENCES "posts"("id") ON DELETE CASCADE,
    "parent_id" UUID REFERENCES "comments"("id") ON DELETE CASCADE,

    -- 时间戳
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS "idx_comments_post_id" ON "comments"("post_id");
CREATE INDEX IF NOT EXISTS "idx_comments_author_id" ON "comments"("author_id");

-- ==================== 初始化数据 ====================

-- 插入默认分类
INSERT INTO "categories" ("name", "slug", "description") VALUES
    ('动漫资讯', 'anime', '最新动漫新闻、番剧更新、业界动态'),
    ('游戏攻略', 'game', '游戏通关指南、角色培养、剧情解析'),
    ('二次元美图', 'pictures', '精选壁纸、Cosplay、插画作品'),
    ('同人创作', 'fanwork', '同人小说、同人绘画、手办模型')
ON CONFLICT ("slug") DO NOTHING;

-- 插入默认标签
INSERT INTO "tags" ("name", "slug") VALUES
    ('原神', 'genshin'),
    ('崩坏星穹铁道', 'honkai-star-rail'),
    ('我的世界', 'minecraft'),
    ('EVA', 'evangelion'),
    ('约定的梦幻岛', 'neverland'),
    ('咒术回战', 'jujutsu-kaisen'),
    ('Cosplay', 'cosplay'),
    ('手办', 'figure')
ON CONFLICT ("slug") DO NOTHING;

-- 插入管理员用户 (密码: admin123)
-- 密码哈希基于 bcrypt，使用前请替换为实际哈希值
INSERT INTO "users" ("username", "email", "password_hash", "is_superuser") VALUES
    ('admin', 'admin@acgblog.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.TZND60LMTUBu.K', TRUE)
ON CONFLICT ("username") DO NOTHING;

-- ==================== 注释 ====================
COMMENT ON TABLE "users" IS '用户表';
COMMENT ON TABLE "categories" IS '文章分类表';
COMMENT ON TABLE "tags" IS '文章标签表';
COMMENT ON TABLE "posts" IS '文章表';
COMMENT ON TABLE "post_tags" IS '文章标签关联表';
COMMENT ON TABLE "comments" IS '评论表';

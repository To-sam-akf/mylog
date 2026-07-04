# MyLog 个人网页开发文档

## 1. 项目概述

MyLog 是一个用于记录个人生活、展示作品集，并接入个人 Agent 的个人网站项目。

项目当前阶段主要包含两个内容模块：

* Life Notes：记录生活随笔、日常想法、图片内容等。
* Works：展示个人作品、项目经历、研究成果等。

网站面向两类用户：

* 管理者：本人，可以登录后台并编辑内容。
* 访客：其他用户，只能查看内容，不能编辑。

此外，网页右下角提供一个悬浮按钮。点击后展开一个小型对话框，用于和个人 Agent 交互。该 Agent 后续可接入个人知识库，用于回答关于个人经历、作品、研究项目等问题。

---

## 2. 页面架构设计

整体页面结构如下：

```text
主页 Home
├── Life Notes
└── Works

右下角悬浮按钮
└── Personal Agent Chat Box
```

### 2.1 主页 Home

主页用于展示个人网站的入口信息，包括：

* 网站名称，例如 MyLog。
* 简短个人介绍。
* Life Notes 入口。
* Works 入口。
* 右下角个人 Agent 悬浮按钮。

推荐路由：

```text
/
```

### 2.2 Life Notes 页面

Life Notes 页面用于记录生活内容，支持：

* 文字编辑。
* 图片上传。
* 内容实时保存。
* 访客只读。

推荐路由：

```text
/life-notes
```

### 2.3 Works 页面

Works 页面用于展示作品集，支持：

* 项目文字介绍。
* 图片、截图、海报等内容。
* 内容实时保存。
* 访客只读。

推荐路由：

```text
/works
```

### 2.4 Personal Agent 悬浮组件

网页右下角放置一个悬浮按钮。

默认状态：

```text
圆形按钮 / 图标按钮
```

点击后展开：

```text
小型聊天窗口
├── 对话展示区
├── 输入框
└── 发送按钮
```

基础功能：

* 用户输入问题。
* 前端请求后端 Agent 接口。
* 后端返回回答。
* 前端展示对话内容。

后续增强：

* 接入个人知识库。
* 支持查询个人项目、简历、研究方向、作品说明等。
* 支持多轮对话。

---

## 3. 技术栈

### 3.1 前端

```text
HTML + CSS + JavaScript + Vue
```

推荐使用：

```text
Vue 3
Vue Router
Axios
Vite
```

前端主要负责：

* 页面展示。
* 路由切换。
* 内容编辑器。
* 图片上传。
* 权限状态控制。
* Agent 聊天窗口交互。

### 3.2 后端

```text
Python + FastAPI
```

后端主要负责：

* 用户登录认证。
* 页面内容读取与保存。
* 图片上传。
* 权限校验。
* Agent 问答接口。
* 数据库交互。

### 3.3 数据库

```text
MySQL
```

数据库主要存储：

* 用户信息。
* 页面内容。
* 图片资源。
* 页面历史版本。
* Agent 对话记录。
* 后续知识库内容。

---

## 4. 核心功能设计

## 4.1 用户权限设计

系统分为两种角色：

| 角色      | 权限                |
| ------- | ----------------- |
| Admin   | 可以查看、编辑、上传图片、保存内容 |
| Visitor | 只能查看内容，不能编辑       |

权限控制原则：

* 前端根据登录状态决定是否显示编辑按钮。
* 后端必须再次校验权限，不能只依赖前端隐藏按钮。
* 所有编辑、上传、删除接口都需要 Admin 权限。
* 所有查看接口允许公开访问。

---

## 4.2 Life Notes 功能设计

Life Notes 页面功能包括：

```text
1. 打开页面后加载已有内容。
2. 管理者登录后进入可编辑状态。
3. 支持输入文字。
4. 支持插入图片。
5. 编辑内容自动保存。
6. 访客只能查看最终渲染内容。
```

推荐交互：

* 未登录：展示只读页面。
* 已登录：显示“编辑 / 预览”切换按钮。
* 编辑时自动保存。
* 保存状态提示：保存中、已保存、保存失败。

内容存储形式建议：

```text
content_html：用于网页直接渲染
content_json：用于富文本编辑器还原编辑状态
content_markdown：可选，用于后续迁移或导出
```

MVP 阶段可以先只使用：

```text
content_html
```

---

## 4.3 Works 功能设计

Works 页面和 Life Notes 类似，但内容表达更偏作品集展示。

Works 页面建议支持以下内容结构：

```text
作品标题
作品简介
技术栈
核心亮点
项目截图
项目链接
时间信息
```

初版可以将 Works 作为一个整体可编辑页面。

后续如果作品数量增多，可以扩展为独立作品管理：

```text
/works
/works/:id
```

并增加作品表 `work_items`。

---

## 4.4 实时编辑设计

这里的“实时编辑”建议采用“前端即时编辑 + 自动保存”的方式实现。

### 编辑流程

```text
用户输入内容
↓
前端监听内容变化
↓
防抖处理，例如 1000ms
↓
调用后端保存接口
↓
后端写入 MySQL
↓
返回保存成功
↓
前端显示“已保存”
```

### 防抖保存

为了避免用户每输入一个字就请求后端，可以使用防抖机制：

```text
用户停止输入 800ms - 1500ms 后，再自动保存
```

推荐保存策略：

```text
普通输入：自动保存
图片上传：上传完成后立即保存
离开页面前：再次保存一次
```

### 多端同步

当前阶段只有本人编辑，访客只读，因此 MVP 不一定需要复杂协同编辑。

后续可以加入 WebSocket：

```text
/ws/pages/{slug}
```

用于实现：

* 管理者编辑后，访客页面自动更新。
* 多设备打开同一页面时同步内容。
* Agent 回答时实时流式输出。

---

## 4.5 图片上传设计

图片上传流程：

```text
前端选择图片
↓
调用图片上传接口
↓
后端校验文件类型和大小
↓
保存到服务器本地目录或对象存储
↓
返回图片 URL
↓
前端将图片插入编辑器
↓
保存页面内容
```

初版可以将图片保存到：

```text
backend/static/uploads/
```

图片访问路径：

```text
/static/uploads/example.png
```

后续可以改为对象存储，例如 OSS、COS、S3 等。

图片限制建议：

```text
支持格式：jpg、jpeg、png、webp、gif
单张大小：不超过 5MB
```

---

## 4.6 Personal Agent 功能设计

Personal Agent 是网页右下角的悬浮聊天组件。

### 前端功能

```text
1. 默认显示一个悬浮按钮。
2. 点击后展开聊天窗口。
3. 用户输入问题。
4. 前端调用后端 Agent 接口。
5. 展示返回结果。
6. 支持关闭窗口。
```

### 后端接口

```text
POST /api/agent/chat
```

请求示例：

```json
{
  "message": "请介绍一下这个网站主人的作品集",
  "session_id": "optional-session-id"
}
```

返回示例：

```json
{
  "answer": "他目前的作品包括……",
  "session_id": "xxx"
}
```

### 后续知识库设计

后续可以把以下内容加入知识库：

```text
个人简历
项目介绍
论文笔记
研究方向
作品集内容
Life Notes 精选内容
个人博客文章
```

Agent 回答流程可以设计为：

```text
用户问题
↓
问题改写
↓
知识库检索
↓
相关内容召回
↓
生成回答
↓
返回前端
```

---

## 5. 前端模块设计

推荐目录结构：

```text
frontend/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── main.js
    ├── App.vue
    ├── router/
    │   └── index.js
    ├── api/
    │   ├── page.js
    │   ├── auth.js
    │   ├── upload.js
    │   └── agent.js
    ├── views/
    │   ├── Home.vue
    │   ├── LifeNotes.vue
    │   ├── Works.vue
    │   └── Login.vue
    ├── components/
    │   ├── Navbar.vue
    │   ├── RichEditor.vue
    │   ├── ImageUploader.vue
    │   ├── AgentFloatingButton.vue
    │   └── AgentChatBox.vue
    └── styles/
        ├── global.css
        └── variables.css
```

### 5.1 主要组件说明

| 组件                      | 作用         |
| ----------------------- | ---------- |
| Navbar.vue              | 页面导航栏      |
| RichEditor.vue          | 富文本编辑器     |
| ImageUploader.vue       | 图片上传组件     |
| AgentFloatingButton.vue | 右下角悬浮按钮    |
| AgentChatBox.vue        | Agent 聊天窗口 |
| Login.vue               | 管理员登录页     |

---

## 6. 后端模块设计

推荐目录结构：

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── user.py
│   │   ├── page.py
│   │   ├── asset.py
│   │   └── agent.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── page.py
│   │   ├── upload.py
│   │   └── agent.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── pages.py
│   │   ├── upload.py
│   │   └── agent.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── page_service.py
│   │   ├── upload_service.py
│   │   └── agent_service.py
│   └── static/
│       └── uploads/
├── requirements.txt
└── run.py
```

---

## 7. API 接口设计

## 7.1 页面内容接口

### 获取页面内容

```text
GET /api/pages/{slug}
```

示例：

```text
GET /api/pages/life-notes
GET /api/pages/works
```

返回：

```json
{
  "slug": "life-notes",
  "title": "Life Notes",
  "content_html": "<p>Hello MyLog</p>",
  "updated_at": "2026-06-30 17:00:00"
}
```

### 更新页面内容

```text
PUT /api/admin/pages/{slug}
```

需要 Admin 权限。

请求：

```json
{
  "title": "Life Notes",
  "content_html": "<p>今天记录一些生活内容。</p>",
  "content_json": {}
}
```

返回：

```json
{
  "message": "saved",
  "updated_at": "2026-06-30 17:01:00"
}
```

---

## 7.2 图片上传接口

```text
POST /api/admin/upload/image
```

需要 Admin 权限。

请求类型：

```text
multipart/form-data
```

返回：

```json
{
  "url": "/static/uploads/xxx.png",
  "filename": "xxx.png"
}
```

---

## 7.3 登录接口

```text
POST /api/auth/login
```

请求：

```json
{
  "username": "admin",
  "password": "your-password"
}
```

返回：

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

### 获取当前用户

```text
GET /api/auth/me
```

返回：

```json
{
  "username": "admin",
  "role": "admin"
}
```

---

## 7.4 Agent 接口

```text
POST /api/agent/chat
```

请求：

```json
{
  "message": "你有哪些作品？",
  "session_id": "optional-session-id"
}
```

返回：

```json
{
  "answer": "目前作品集主要包括……",
  "session_id": "session-id"
}
```

---

## 8. 数据库设计

## 8.1 users 表

用于存储管理员账号。

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'admin',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## 8.2 pages 表

用于存储 Life Notes 和 Works 页面内容。

```sql
CREATE TABLE pages (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    slug VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    content_html LONGTEXT,
    content_json JSON,
    content_markdown LONGTEXT,
    visibility VARCHAR(50) DEFAULT 'public',
    updated_by BIGINT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id)
);
```

初始数据：

```sql
INSERT INTO pages (slug, title, content_html)
VALUES
('life-notes', 'Life Notes', '<p>记录生活。</p>'),
('works', 'Works', '<p>展示作品。</p>');
```

---

## 8.3 page_versions 表

用于保存历史版本，避免误删内容无法恢复。

```sql
CREATE TABLE page_versions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    page_id BIGINT NOT NULL,
    title VARCHAR(255),
    content_html LONGTEXT,
    content_json JSON,
    content_markdown LONGTEXT,
    created_by BIGINT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (page_id) REFERENCES pages(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

建议策略：

```text
每次手动保存时保存版本。
自动保存可以每隔一段时间保存版本，避免版本数量过多。
```

---

## 8.4 assets 表

用于记录上传的图片资源。

```sql
CREATE TABLE assets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    url VARCHAR(500) NOT NULL,
    mime_type VARCHAR(100),
    size_bytes BIGINT,
    uploaded_by BIGINT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);
```

---

## 8.5 agent_sessions 表

用于记录 Agent 会话。

```sql
CREATE TABLE agent_sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## 8.6 agent_messages 表

用于记录 Agent 对话消息。

```sql
CREATE TABLE agent_messages (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 9. 权限与安全设计

### 9.1 登录认证

推荐使用：

```text
JWT Token
```

流程：

```text
管理员登录
↓
后端验证账号密码
↓
生成 JWT
↓
前端保存 Token
↓
请求编辑接口时携带 Token
```

请求头格式：

```text
Authorization: Bearer <token>
```

### 9.2 编辑权限控制

所有以下接口都必须校验 Admin 权限：

```text
PUT /api/admin/pages/{slug}
POST /api/admin/upload/image
DELETE /api/admin/assets/{id}
```

### 9.3 XSS 防护

由于页面支持富文本和 HTML，需要注意 XSS 风险。

建议：

```text
1. 后端保存前过滤危险标签。
2. 禁止 script 标签。
3. 禁止 onerror、onclick 等危险属性。
4. 图片只允许安全格式。
5. 前端渲染 HTML 时只渲染经过清洗的内容。
```

### 9.4 图片安全

图片上传需要限制：

```text
文件类型
文件大小
文件后缀
文件名随机化
```

不要直接使用用户上传的原始文件名作为服务器文件名。

---

## 10. 页面交互设计

## 10.1 Home 页面

页面结构建议：

```text
顶部导航栏
↓
个人介绍区域
↓
两个入口卡片
    Life Notes
    Works
↓
右下角 Agent 按钮
```

视觉风格建议：

```text
简洁
白底
黑字
少量强调色
卡片式布局
保留留白
```

## 10.2 Life Notes 页面

访客状态：

```text
标题
更新时间
正文内容
图片内容
```

管理员状态：

```text
标题
编辑按钮
富文本编辑器
图片上传
保存状态
预览按钮
```

## 10.3 Works 页面

建议内容模块：

```text
个人作品介绍
项目卡片
项目截图
技术栈标签
项目链接
研究成果
```

MVP 阶段可以先做成一个可编辑页面。

后续再拆成多个作品条目。

## 10.4 Agent 组件

默认：

```text
右下角圆形悬浮按钮
```

展开后：

```text
聊天窗口
├── 标题：My Agent
├── 消息列表
├── 输入框
└── 发送按钮
```

移动端适配：

```text
聊天窗口宽度占屏幕 90%
底部固定显示
```

---

## 11. 开发阶段规划

## 第一阶段：基础页面搭建

目标：

```text
完成主页、Life Notes、Works 的静态页面。
```

任务：

```text
1. 初始化 Vue 项目。
2. 配置 Vue Router。
3. 创建 Home、LifeNotes、Works 页面。
4. 编写基础 CSS。
5. 添加导航栏。
6. 添加右下角悬浮按钮。
```

---

## 第二阶段：后端基础服务

目标：

```text
完成 FastAPI + MySQL 基础接口。
```

任务：

```text
1. 初始化 FastAPI 项目。
2. 连接 MySQL。
3. 创建 users、pages、assets 表。
4. 实现页面读取接口。
5. 实现页面保存接口。
6. 实现管理员登录接口。
```

---

## 第三阶段：编辑与上传功能

目标：

```text
管理员可以在线编辑 Life Notes 和 Works。
```

任务：

```text
1. 前端判断登录状态。
2. 管理员显示编辑器。
3. 访客显示只读页面。
4. 实现自动保存。
5. 实现图片上传。
6. 图片插入正文。
```

---

## 第四阶段：Agent 聊天窗口

目标：

```text
完成网页右下角个人 Agent 对话框。
```

任务：

```text
1. 实现 AgentFloatingButton 组件。
2. 实现 AgentChatBox 组件。
3. 实现 /api/agent/chat 接口。
4. 前后端联调。
5. 保存基础对话记录。
```

---

## 第五阶段：知识库增强

目标：

```text
让 Agent 可以基于个人知识库回答问题。
```

任务：

```text
1. 整理个人知识库内容。
2. 构建文本切分和向量检索流程。
3. 后端接入 RAG。
4. Agent 回答时引用相关内容。
5. 支持询问作品、经历、研究方向。
```

---

## 第六阶段：部署上线

目标：

```text
将项目部署到服务器，支持公网访问。
```

任务：

```text
1. 前端打包。
2. 后端部署。
3. 配置 MySQL。
4. 配置静态资源访问。
5. 配置 Nginx 反向代理。
6. 配置 HTTPS。
7. 设置管理员账号。
```

---

## 12. 推荐开发顺序

建议按照以下顺序开发：

```text
1. 静态前端页面
2. FastAPI 后端项目
3. MySQL 数据库建表
4. 页面内容读取接口
5. 页面内容保存接口
6. 管理员登录
7. 编辑权限控制
8. 图片上传
9. 自动保存
10. Agent 悬浮窗口
11. Agent 后端接口
12. 知识库问答增强
13. 部署上线
```

---

## 13. MVP 功能范围

第一版不要做得过重，建议 MVP 只实现以下功能：

```text
1. 主页
2. Life Notes 页面
3. Works 页面
4. 管理员登录
5. 管理员编辑内容
6. 自动保存
7. 图片上传
8. 访客只读
9. Agent 悬浮按钮
10. Agent 基础对话接口
```

暂时不建议第一版就实现：

```text
多人协同编辑
复杂作品管理后台
评论系统
点赞系统
用户注册系统
复杂权限系统
完整 RAG 知识库
```

这些功能可以在基础版本稳定后逐步加入。

---

## 14. 项目最终形态

MyLog 最终可以发展成一个融合个人主页、生活记录、作品集和个人智能体的长期个人网站。

核心定位：

```text
一个可以长期积累个人内容的 Life + Works + Agent 系统。
```

长期功能方向：

```text
1. Life Notes 变成个人博客和生活记录空间。
2. Works 变成完整作品集和项目展示系统。
3. Agent 变成个人数字助理，可以基于个人知识库回答问题。
4. 后台支持内容管理、图片管理、版本回退。
5. 网站整体形成个人品牌展示入口。
```

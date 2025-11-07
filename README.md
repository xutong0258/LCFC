# LCFC Backend 部署文档

## 项目简介

本项目是 LCFC 的后端服务，基于 FastAPI 框架开发，提供用户管理、部门管理、Issue 管理等功能。

## 环境要求

在开始部署之前，请确保您的系统已安装以下依赖：

- **Python 3.10+**
- **MySQL 5.7+** 或 **MySQL 8.0+**
- **Redis 5.0+**
- **uv** (Python 包管理工具)

## 部署步骤

### 1. 准备基础环境

#### 1.1 安装 MySQL

根据您的操作系统安装 MySQL 数据库：

- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install mysql-server
  sudo systemctl start mysql
  sudo systemctl enable mysql
  ```

- **macOS**:
  ```bash
  brew install mysql
  brew services start mysql
  ```

- **Windows**: 
  从 [MySQL 官网](https://dev.mysql.com/downloads/mysql/) 下载并安装

#### 1.2 安装 Redis

根据您的操作系统安装 Redis：

- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install redis-server
  sudo systemctl start redis
  sudo systemctl enable redis
  ```

- **macOS**:
  ```bash
  brew install redis
  brew services start redis
  ```

- **Windows**: 
  从 [Redis 官网](https://redis.io/download) 下载并安装

#### 1.3 安装 uv

uv 是一个快速的 Python 包管理工具：

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

或使用 pip 安装：

```bash
pip install uv
```

### 2. 克隆项目并安装依赖

```bash
# 克隆项目（如果尚未克隆）
git clone <repository-url>
cd lcfcbackend

# 使用 uv 安装项目依赖
uv sync
```

### 3. 配置环境变量

在项目根目录下创建并配置 `.env.dev` 文件：

```bash
cp .env.example .env.dev  # 如果有示例文件
# 或者直接创建
touch .env.dev
```

编辑 `.env.dev` 文件，配置以下参数（文件中包含详细的注释，说明每个参数的作用）：

主要配置项包括：
- 数据库连接信息（MySQL 地址、端口、用户名、密码、数据库名）
- Redis 连接信息（地址、端口、密码）
- 应用运行端口
- JWT 密钥配置
- 文件上传路径配置
- 其他应用相关配置

> **注意**: `.env.dev` 文件包含敏感信息，请勿提交到版本控制系统中。

### 4. 初始化数据库

在 MySQL 中创建数据库并运行初始化脚本：

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库（根据 .env.dev 中配置的数据库名）
CREATE DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

依次执行 `sql` 目录下的 SQL 文件初始化数据库表结构和数据：

```bash
# 执行主数据库脚本
mysql -u root -p your_database_name < sql/fastapi.sql

# 执行 Issue 相关表结构
mysql -u root -p your_database_name < sql/issue_tables.sql

# 执行更新脚本
mysql -u root -p your_database_name < sql/update_issue_attachment_table.sql
```

> **提示**: 请按照上述顺序执行 SQL 文件，确保数据库结构正确初始化。

### 5. 启动应用

项目提供两种启动方式，您可以根据需要选择：

#### 方式一：使用 uv 直接运行（开发环境推荐）

```bash
# 使用 uv 运行应用
uv run app.py
```

应用将在配置的端口上启动（默认通常为 8000 或 8080）。

#### 方式二：使用 Docker 部署（生产环境推荐）

使用 Dockerfile 构建并运行容器：

```bash
# 构建 Docker 镜像
docker build -t lcfcbackend:latest .

# 运行容器
docker run -d \
  --name lcfcbackend \
  -p 8000:8000 \
  -v $(pwd)/.env.dev:/app/.env.dev \
  -v $(pwd)/vf_admin:/app/vf_admin \
  lcfcbackend:latest
```

或使用 Docker Compose（如果配置了 docker-compose.yml）：

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 6. 验证部署

部署完成后，您可以通过以下方式验证服务是否正常运行：

```bash
# 检查服务状态
curl http://localhost:8000/docs
```

访问浏览器打开 `http://localhost:8000/docs`，您应该能看到 FastAPI 自动生成的 API 文档页面。

## 常用命令

### 查看日志

应用日志存储在 `logs` 目录下：

```bash
# 查看最新日志
tail -f logs/$(date +%Y-%m-%d)_error.log
```

### 停止应用

```bash
# 如果使用 uv run 启动，使用 Ctrl+C 停止

# 如果使用 Docker
docker stop lcfcbackend

# 如果使用 Docker Compose
docker-compose down
```

### 重启应用

```bash
# Docker
docker restart lcfcbackend

# Docker Compose
docker-compose restart
```

## 项目结构

```
lcfcbackend/
├── app.py                  # 应用入口文件
├── server.py              # 服务器启动文件
├── config/                # 配置文件目录
├── module_admin/          # 管理模块
│   ├── controller/        # 控制器层
│   ├── service/           # 服务层
│   ├── dao/              # 数据访问层
│   └── entity/           # 实体类
├── module_task/           # 定时任务模块
├── utils/                 # 工具类
├── exceptions/            # 异常处理
├── middlewares/           # 中间件
├── sql/                   # 数据库脚本
├── logs/                  # 日志目录
└── vf_admin/             # 文件存储目录
```

## 注意事项

1. **环境变量**: 确保 `.env.dev` 文件配置正确，特别是数据库和 Redis 连接信息
2. **数据库编码**: 建议使用 `utf8mb4` 字符集以支持完整的 Unicode 字符
3. **文件权限**: 确保 `logs/` 和 `vf_admin/` 目录有写入权限
4. **防火墙**: 如果部署在服务器上，确保开放相应的端口
5. **生产环境**: 生产环境建议使用 Nginx 作为反向代理，并配置 HTTPS

## 故障排查

### 数据库连接失败

- 检查 MySQL 服务是否正常运行
- 验证 `.env.dev` 中的数据库连接信息是否正确
- 确认数据库用户是否有足够的权限

### Redis 连接失败

- 检查 Redis 服务是否正常运行
- 验证 `.env.dev` 中的 Redis 连接信息是否正确
- 检查 Redis 是否需要密码认证

### 端口被占用

- 使用 `lsof -i :端口号` (Linux/macOS) 或 `netstat -ano | findstr 端口号` (Windows) 查看端口占用
- 修改配置文件中的端口号或停止占用端口的进程

## 技术支持

如有问题或建议，请联系开发团队或提交 Issue。

## 许可证

[根据您的项目添加相应的许可证信息]


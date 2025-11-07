# 基础镜像（Python 3.11，构建时有网拉取）
FROM python:3.11-slim

# 工作目录
WORKDIR /app

# 安装系统依赖（构建时有网下载）
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv（root 用户，构建时有网）
RUN pip install --no-cache-dir uv

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# 第一步：复制依赖清单（仅必要文件，触发缓存）
COPY pyproject.toml uv.lock ./

# 授权 appuser 访问工作目录
RUN chown -R appuser:appuser /app

# 切换到 appuser（构建+运行时统一用户）
USER appuser

# 安装 Python 依赖（构建时有网，创建完整 .venv 虚拟环境）
# 关键：--locked 强制用 uv.lock，--no-cache 不缓存，确保依赖全量打包
RUN uv sync --frozen --no-cache --no-dev \
    --index-url https://pypi.org/simple/

# 第二步：复制应用代码（此时 .dockerignore 已排除本地 .venv，不会覆盖镜像的 .venv）
COPY . .

# 验证依赖是否安装成功（可选，构建时排查问题）
RUN .venv/bin/python -c "import fastapi; import websockets; import uvicorn" || echo "依赖安装失败！"

# 创建应用所需目录（appuser 有权限）
RUN mkdir -p vf_admin/upload_path/issues vf_admin/download_path logs

# 暴露端口
EXPOSE 8080

# 健康检查（延长启动等待时间，适配依赖加载）
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/api/docs || exit 1

# 启动命令：明确指定虚拟环境的 Python 解释器，彻底避免重建
CMD [".venv/bin/python", "app.py"]
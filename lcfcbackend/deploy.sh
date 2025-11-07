#!/bin/bash

# 部署脚本 for LCFC Backend
# 用法: ./deploy.sh [build|start|stop|restart|logs|status]

set -e

PROJECT_NAME="lcfcbackend"
COMPOSE_FILE="docker-compose.yml"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker和docker-compose
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker not found! Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "docker-compose not found! Please install docker-compose first."
        exit 1
    fi
}

# 构建镜像
build() {
    log_info "Building Docker image for $PROJECT_NAME..."
    docker-compose build --no-cache
    log_success "Build completed successfully!"
}

# 启动服务
start() {
    log_info "Starting $PROJECT_NAME services..."
    
    # 创建必要的目录
    mkdir -p vf_admin/upload_path/issues vf_admin/download_path logs
    
    docker-compose up -d
    
    # 等待服务启动
    log_info "Waiting for services to start..."
    sleep 15
    
    # 健康检查
    if health_check; then
        log_success "Services started successfully!"
        show_status
    else
        log_error "Health check failed!"
        exit 1
    fi
}

# 停止服务
stop() {
    log_info "Stopping $PROJECT_NAME services..."
    docker-compose down --timeout 30
    log_success "Services stopped successfully!"
}

# 重启服务
restart() {
    log_info "Restarting $PROJECT_NAME services..."
    stop
    sleep 3
    start
}

# 查看日志
logs() {
    log_info "Showing logs for $PROJECT_NAME..."
    docker-compose logs -f --tail=100
}

# 显示服务状态
show_status() {
    log_info "Service status:"
    docker-compose ps
    
    log_info "Container resource usage:"
    docker stats $PROJECT_NAME --no-stream
    
    log_info "Resource configuration:"
    echo "  - CPU: 2 cores guaranteed, up to 3 cores maximum"
    echo "  - Memory: 2GB guaranteed, up to 4GB maximum"
}

# 健康检查
health_check() {
    log_info "Performing health check..."
    
    local max_attempts=10
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s http://localhost:8080/dev-api/docs > /dev/null 2>&1; then
            log_success "Health check passed!"
            return 0
        fi
        
        log_warn "Health check attempt $attempt/$max_attempts failed, retrying in 5 seconds..."
        sleep 5
        ((attempt++))
    done
    
    log_error "Health check failed after $max_attempts attempts!"
    return 1
}

# 清理资源
cleanup() {
    log_info "Cleaning up unused Docker resources..."
    docker system prune -f
    docker volume prune -f
    log_success "Cleanup completed!"
}

# 备份数据
backup() {
    local backup_dir="backup/$(date +%Y%m%d_%H%M%S)"
    log_info "Creating backup in $backup_dir..."
    
    mkdir -p "$backup_dir"
    
    # 备份上传文件
    if [ -d "vf_admin" ]; then
        cp -r vf_admin "$backup_dir/"
        log_info "Upload files backed up"
    fi
    
    # 备份日志
    if [ -d "logs" ]; then
        cp -r logs "$backup_dir/"
        log_info "Log files backed up"
    fi
    
    # 备份配置文件
    cp -r config "$backup_dir/" 2>/dev/null || true
    cp .env.* "$backup_dir/" 2>/dev/null || true
    
    log_success "Backup created in $backup_dir"
}

# 显示帮助信息
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build Docker image"
    echo "  start     Start services"
    echo "  stop      Stop services"
    echo "  restart   Restart services"
    echo "  logs      Show service logs"
    echo "  status    Show service status"
    echo "  health    Perform health check"
    echo "  cleanup   Clean up unused Docker resources"
    echo "  backup    Backup data files"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start          Start all services"
    echo "  $0 logs           Follow service logs"
    echo "  $0 restart        Restart all services"
}

# 主函数
main() {
    check_dependencies
    
    case "${1:-help}" in
        "build")
            build
            ;;
        "start")
            start
            ;;
        "stop")
            stop
            ;;
        "restart")
            restart
            ;;
        "logs")
            logs
            ;;
        "status")
            show_status
            ;;
        "health")
            health_check
            ;;
        "cleanup")
            cleanup
            ;;
        "backup")
            backup
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"

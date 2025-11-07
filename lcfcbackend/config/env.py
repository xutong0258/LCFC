import argparse
import os
import sys
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Literal  # 限定为固定范围常量
from utils.log_util import logger


"""
BaseSettings 优先级顺序
1、初始化中带设置值
2、配置.evn中加载
3、环境变量中加载从os.environ
4、使用默认配置
"""


class AppSetting(BaseSettings):
    app_env: str = "dev"
    app_name: str = "FastAPI-Demo"
    app_root_path: str = "/dev-api"
    app_host: str = "0.0.0.0"
    app_port: int = 9099
    app_version: str = "1.0.0"
    app_reload: bool = True
    app_ip_location_query: bool = True
    app_same_time_login: bool = True


class JwtSetting(BaseSettings):
    jwt_secret_key: str = (
        "b01c66dc2c58dc6a0aabfe2144256be36226de378bf87f72c0c795dda67f4d55"
    )
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    jwt_redis_expire_minutes: int = 30


class DataBaseSetting(BaseSettings):
    db_type: Literal["mysql", "postgresql"] = "mysql"
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_username: str = "root"
    db_password: str = "root"
    db_database: str = "database"
    db_echo: bool = True
    db_max_overflow: int = 10
    db_pool_size: int = 50
    db_pool_recycle: int = 3600
    db_pool_timeout: int = 30


class RedisSetting(BaseSettings):
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_username: str = ""
    redis_password: str = ""
    redis_database: int = 2


class UploadSettings:
    UPLOAD_PREFIX = "/profile"
    UPLOAD_PATH = "vf_admin/upload_path"
    UPLOAD_MACHINE = "A"
    DEFAULT_ALLOWED_EXTENSION = [
        # 图片
        "bmp",
        "gif",
        "jpg",
        "jpeg",
        "png",
        # word excel powerpoint
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "html",
        "htm",
        "txt",
        # 压缩文件
        "rar",
        "zip",
        "gz",
        "bz2",
        # 视频格式
        "mp4",
        "avi",
        "rmvb",
        # pdf
        "pdf",
        # 日志
        "log",
        "dmp",
    ]
    DOWNLOAD_PATH = "vf_admin/download_path"
    issue_path = "vf_admin/upload_path/issues"

    def __init__(self):
        if not os.path.exists(self.UPLOAD_PATH):
            os.makedirs(self.UPLOAD_PATH)
        if not os.path.exists(self.DOWNLOAD_PATH):
            os.makedirs(self.DOWNLOAD_PATH)
        if not os.path.exists(self.issue_path):
            os.makedirs(self.issue_path)


class CachePathConfig:
    PATH = os.path.join(os.path.abspath(os.getcwd()), "caches")
    PATHSTR = "caches"


class GetConfig:
    def __init__(self):
        self.parse_cli_args()

    @lru_cache()
    def get_app_config(self):
        return AppSetting()

    @lru_cache()
    def get_jwt_config(self):
        return JwtSetting()

    @lru_cache()
    def get_database_config(self):
        return DataBaseSetting()

    @lru_cache()
    def get_redis_config(self):
        return RedisSetting()

    @lru_cache()
    def get_upload_config(self):
        return UploadSettings()

    @staticmethod
    def parse_cli_args():
        if "uvicorn" in sys.argv[0]:
            pass
        else:
            parser = argparse.ArgumentParser(description="命令行参数")
            parser.add_argument("--env", type=str, default="", help="运行环境")
            args = parser.parse_args()
            os.environ["APP_ENV"] = args.env if args.env else "dev"
        run_env = os.environ.get("APP_ENV", "")
        env_file = ".env.dev"
        if run_env:
            env_file = f".env.{run_env}"
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), env_file)
        logger.info(f"加载配置文件:{env_file}")
        load_dotenv(env_file)


get_config = GetConfig()
AppConfig = get_config.get_app_config()
JwtConfig = get_config.get_jwt_config()
DataBaseConfig = get_config.get_database_config()
RedisConfig = get_config.get_redis_config()
UploadConfig = get_config.get_upload_config()

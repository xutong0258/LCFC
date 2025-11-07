import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import Base
from module_admin.entity.do.issue_do import (
    IssueMain, IssueSystemEnv, IssueDiagnosisLog, IssueAttachment, IssueTag
)


@pytest.fixture(scope="function")
def db_session():
    """创建内存数据库会话，用于测试"""
    # 使用SQLite内存数据库进行测试
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # 创建所有表
    Base.metadata.create_all(bind=engine)

    # 创建会话
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def sample_issue_data():
    """创建示例Issue数据"""
    return {
        "title": "测试Issue",
        "priority": "medium",
        "status": "pending",
        "issue_type": "BUG",
        "description": "这是一个测试Issue",
        "issue_source": "测试",
        "create_by": "test_user",
        "update_by": "test_user"
    }


@pytest.fixture(scope="function")
def sample_system_env_data():
    """创建示例系统环境数据"""
    return {
        "cpu_info": "Intel Core i7-11800H",
        "memory_info": "16GB DDR4",
        "gpu_info": "NVIDIA GeForce RTX 3060",
        "os_info": "Windows 11",
        "gpu_driver_version": "517.9",
        "bios_version": "1.07"
    }


@pytest.fixture(scope="function")
def sample_diagnosis_log_data():
    """创建示例诊断日志数据"""
    return {
        "step_name": "初始诊断",
        "method_description": "检查系统日志",
        "operator": "test_user"
    }


@pytest.fixture(scope="function")
def sample_attachment_data():
    """创建示例附件数据"""
    return {
        "file_name": "test_log.txt",
        "file_path": "/test/path/test_log.txt",
        "file_size": 1024,
        "file_type": ".txt",
        "upload_by": "test_user"
    }


@pytest.fixture(scope="function")
def sample_tag_data():
    """创建示例标签数据"""
    return ["bug", "test", "windows"]

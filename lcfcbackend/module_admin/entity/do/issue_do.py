from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, BigInteger, ForeignKey
from config.database import Base


class IssueMain(Base):
    """
    Issue主表
    """

    __tablename__ = "issue_main"

    issue_id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="Issue ID"
    )
    issue_number = Column(
        String(32), nullable=False, unique=True, comment="Issue编号(如ISU-2023-1542)"
    )
    title = Column(String(200), nullable=False, comment="Issue标题")
    priority = Column(
        String(10), nullable=False, default="low", comment="优先级(high,medium,low)"
    )
    status = Column(
        String(20),
        nullable=False,
        default="pending",
        comment="状态(pending待诊断,diagnosing诊断中,completed已完成,cancelled已取消)",
    )
    issue_type = Column(
        String(50), nullable=False, comment="Issue类型(BUG,工单,系统日志,测试报告等)"
    )
    issue_source = Column(String(100), default=None, comment="Issue来源")
    description = Column(Text, comment="问题描述")
    solution = Column(Text, comment="解决方案")
    expected_resolve_date = Column(DateTime, comment="预期解决日期")
    create_by = Column(String(64), default="", comment="创建者")
    create_time = Column(DateTime, comment="创建时间", default=datetime.now())
    update_by = Column(String(64), default="", comment="更新者")
    update_time = Column(DateTime, comment="更新时间", default=datetime.now())
    del_flag = Column(String(1), default="0", comment="删除标志（0代表存在 2代表删除）")


class IssueSystemEnv(Base):
    """
    Issue系统环境表
    """

    __tablename__ = "issue_system_env"

    env_id = Column(BigInteger, primary_key=True, autoincrement=True, comment="环境ID")
    issue_id = Column(
        BigInteger,
        ForeignKey("issue_main.issue_id"),
        nullable=False,
        comment="Issue ID",
    )
    cpu_info = Column(String(200), comment="CPU信息")
    memory_info = Column(String(200), comment="内存信息")
    gpu_info = Column(String(200), comment="显卡信息")
    os_info = Column(String(200), comment="操作系统信息")
    gpu_driver_version = Column(String(100), comment="显卡驱动版本")
    bios_version = Column(String(100), comment="BIOS版本")


class IssueDiagnosisLog(Base):
    """
    Issue诊断记录表
    """

    __tablename__ = "issue_diagnosis_log"

    log_id = Column(BigInteger, primary_key=True, autoincrement=True, comment="记录ID")
    issue_id = Column(
        BigInteger,
        ForeignKey("issue_main.issue_id"),
        nullable=False,
        comment="Issue ID",
    )
    step_name = Column(String(200), nullable=False, comment="诊断步骤名称")
    method_description = Column(Text, comment="具体诊断方法")
    operator = Column(String(64), nullable=False, comment="操作人")
    operate_time = Column(DateTime, comment="操作时间", default=datetime.now())


class IssueAttachment(Base):
    """
    Issue附件表
    """

    __tablename__ = "issue_attachment"

    attachment_id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="附件ID"
    )
    issue_id = Column(
        BigInteger,
        ForeignKey("issue_main.issue_id"),
        nullable=True,  # 改为可空，支持临时附件
        comment="Issue ID",
    )
    file_name = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_size = Column(BigInteger, comment="文件大小(字节)")
    file_type = Column(String(50), comment="文件类型")
    upload_time = Column(DateTime, comment="上传时间", default=datetime.now())
    upload_by = Column(String(64), comment="上传者")
    status = Column(
        String(20), 
        nullable=False, 
        default="temporary", 
        comment="附件状态(temporary临时,linked已关联)"
    )


class IssueTag(Base):
    """
    Issue标签表
    """

    __tablename__ = "issue_tag"

    tag_id = Column(BigInteger, primary_key=True, autoincrement=True, comment="标签ID")
    issue_id = Column(
        BigInteger,
        ForeignKey("issue_main.issue_id"),
        nullable=False,
        comment="Issue ID",
    )
    tag_name = Column(String(50), nullable=False, comment="标签名称")

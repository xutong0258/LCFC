from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size, Xss
from typing import List, Literal, Optional, Union
from module_admin.annotation.pydantic_annotation import as_query


class IssueMainModel(BaseModel):
    """
    Issue主表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    issue_id: Optional[int] = Field(default=None, description="Issue ID")
    issue_number: Optional[str] = Field(default=None, description="Issue编号")
    title: Optional[str] = Field(default=None, description="Issue标题")
    priority: Optional[Literal["high", "medium", "low"]] = Field(
        default=None, description="优先级"
    )
    status: Optional[Literal["pending", "diagnosing", "completed", "cancelled"]] = (
        Field(default=None, description="状态")
    )
    issue_type: Optional[str] = Field(default=None, description="Issue类型")
    issue_source: Optional[str] = Field(default=None, description="Issue来源")
    description: Optional[str] = Field(default=None, description="问题描述")
    solution: Optional[str] = Field(default=None, description="解决方案")
    expected_resolve_date: Optional[datetime] = Field(
        default=None, description="预期解决日期"
    )
    create_by: Optional[str] = Field(default=None, description="创建者")
    create_time: Optional[datetime] = Field(default=None, description="创建时间")
    update_by: Optional[str] = Field(default=None, description="更新者")
    update_time: Optional[datetime] = Field(default=None, description="更新时间")
    del_flag: Optional[Literal["0", "2"]] = Field(
        default=None, description="删除标志（0代表存在 2代表删除）"
    )

    @Xss(field_name="title", message="Issue标题不能包含脚本字符")
    @NotBlank(field_name="title", message="Issue标题不能为空")
    @Size(
        field_name="title",
        min_length=0,
        max_length=200,
        message="Issue标题长度不能超过200个字符",
    )
    def get_title(self):
        return self.title

    @Size(
        field_name="description",
        min_length=0,
        max_length=5000,
        message="问题描述长度不能超过5000个字符",
    )
    def get_description(self):
        return self.description

    def validate_fields(self):
        self.get_title()
        self.get_description()


class IssueSystemEnvModel(BaseModel):
    """
    Issue系统环境表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    env_id: Optional[int] = Field(default=None, description="环境ID")
    issue_id: Optional[int] = Field(default=None, description="Issue ID")
    cpu_info: Optional[str] = Field(default=None, description="CPU信息")
    memory_info: Optional[str] = Field(default=None, description="内存信息")
    gpu_info: Optional[str] = Field(default=None, description="显卡信息")
    os_info: Optional[str] = Field(default=None, description="操作系统信息")
    gpu_driver_version: Optional[str] = Field(default=None, description="显卡驱动版本")
    bios_version: Optional[str] = Field(default=None, description="BIOS版本")


class IssueDiagnosisLogModel(BaseModel):
    """
    Issue诊断记录表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    log_id: Optional[int] = Field(default=None, description="记录ID")
    issue_id: Optional[int] = Field(default=None, description="Issue ID")
    step_name: Optional[str] = Field(default=None, description="诊断步骤名称")
    method_description: Optional[str] = Field(default=None, description="具体诊断方法")
    operator: Optional[str] = Field(default=None, description="操作人")
    operate_time: Optional[datetime] = Field(default=None, description="操作时间")


class IssueAttachmentModel(BaseModel):
    """
    Issue附件表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    attachment_id: Optional[int] = Field(default=None, description="附件ID")
    issue_id: Optional[int] = Field(default=None, description="Issue ID")
    file_name: Optional[str] = Field(default=None, description="文件名")
    file_path: Optional[str] = Field(default=None, description="文件路径")
    file_size: Optional[int] = Field(default=None, description="文件大小")
    file_type: Optional[str] = Field(default=None, description="文件类型")
    upload_time: Optional[datetime] = Field(default=None, description="上传时间")
    upload_by: Optional[str] = Field(default=None, description="上传者")
    status: Optional[Literal["temporary", "linked"]] = Field(
        default="temporary", description="附件状态(temporary临时,linked已关联)"
    )


class IssueTagModel(BaseModel):
    """
    Issue标签表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    tag_id: Optional[int] = Field(default=None, description="标签ID")
    issue_id: Optional[int] = Field(default=None, description="Issue ID")
    tag_name: Optional[str] = Field(default=None, description="标签名称")


class IssueDetailModel(BaseModel):
    """
    Issue详情信息响应模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    issue_info: Union[IssueMainModel, None] = Field(description="Issue基本信息")
    system_env: Union[IssueSystemEnvModel, None] = Field(description="系统环境信息")
    diagnosis_logs: List[Union[IssueDiagnosisLogModel, None]] = Field(
        default=[], description="诊断记录"
    )
    attachments: List[Union[IssueAttachmentModel, None]] = Field(
        default=[], description="附件信息"
    )
    tags: List[Union[IssueTagModel, None]] = Field(default=[], description="标签信息")


class IssueQueryModel(IssueMainModel):
    """
    Issue管理不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description="开始时间")
    end_time: Optional[str] = Field(default=None, description="结束时间")


@as_query
class IssuePageQueryModel(IssueQueryModel):
    """
    Issue管理分页查询模型
    """

    page_num: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=10, description="每页记录数")


class AddIssueModel(IssueMainModel):
    """
    新增Issue模型
    """

    system_env: Optional[IssueSystemEnvModel] = Field(
        default=None, description="系统环境信息"
    )
    tags: Optional[List[str]] = Field(default=[], description="标签列表")
    attachment_ids: Optional[List[int]] = Field(
        default=[], description="附件ID列表（关联已上传的临时附件）"
    )


class EditIssueModel(AddIssueModel):
    """
    编辑Issue模型
    """

    pass


class DeleteIssueModel(BaseModel):
    """
    删除Issue模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    issue_ids: str = Field(description="需要删除的Issue ID列表")
    update_by: Optional[str] = Field(default=None, description="更新者")
    update_time: Optional[datetime] = Field(default=None, description="更新时间")


class AddDiagnosisLogModel(IssueDiagnosisLogModel):
    """
    新增诊断记录模型
    """

    pass


class IssueStatisticsModel(BaseModel):
    """
    Issue统计数据模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    total_count: int = Field(description="Issue总数")
    monthly_new_count: int = Field(description="本月新增Issue数")
    pending_count: int = Field(description="待处理Issue数")
    diagnosis_count: int = Field(description="Issue分析次数")
    high_priority_count: int = Field(description="高优先级Issue数")
    completed_count: int = Field(description="已完成Issue数")


# ==================== 响应 VO 模型 ====================


class IssueStatisticsResponseModel(BaseModel):
    """
    Issue统计数据响应模型
    """

    model_config = ConfigDict(populate_by_name=True)

    total_count: int = Field(description="Issue总数")
    monthly_new_count: int = Field(description="本月新增Issue数")
    pending_count: int = Field(description="待处理Issue数")
    diagnosis_count: int = Field(description="Issue分析次数")
    high_priority_count: int = Field(description="高优先级Issue数")
    completed_count: int = Field(description="已完成Issue数")


class IssueListResponseModel(BaseModel):
    """
    Issue列表查询响应模型（带分页）
    """

    model_config = ConfigDict(populate_by_name=True)

    rows: List[IssueMainModel] = Field(default=[], description="Issue列表数据")
    page_num: Optional[int] = Field(default=None, description="当前页码")
    page_size: Optional[int] = Field(default=None, description="每页记录数")
    total: int = Field(description="总记录数")
    has_next: Optional[bool] = Field(default=None, description="是否有下一页")


class IssueDetailResponseModel(BaseModel):
    """
    Issue详情响应模型
    """

    model_config = ConfigDict(populate_by_name=True)

    issue_info: Optional[IssueMainModel] = Field(default=None, description="Issue基本信息")
    system_env: Optional[IssueSystemEnvModel] = Field(
        default=None, description="系统环境信息"
    )
    diagnosis_logs: List[IssueDiagnosisLogModel] = Field(
        default=[], description="诊断记录列表"
    )
    attachments: List[IssueAttachmentModel] = Field(default=[], description="附件列表")
    tags: List[IssueTagModel] = Field(default=[], description="标签列表")


class IssueOptionItemModel(BaseModel):
    """
    Issue选项项模型
    """

    model_config = ConfigDict(populate_by_name=True)

    label: str = Field(description="选项显示名称")
    value: str = Field(description="选项值")


class IssueOptionsResponseModel(BaseModel):
    """
    Issue选项列表响应模型（用于类型、优先级、状态等选项）
    """

    model_config = ConfigDict(populate_by_name=True)

    options: List[IssueOptionItemModel] = Field(default=[], description="选项列表")


class UploadAttachmentResponseModel(BaseModel):
    """
    上传附件响应模型
    """

    model_config = ConfigDict(populate_by_name=True)

    attachment_id: int = Field(description="附件ID")
    file_name: str = Field(description="文件名")
    file_path: str = Field(description="文件路径")
    file_size: int = Field(description="文件大小")
    file_type: str = Field(description="文件类型")
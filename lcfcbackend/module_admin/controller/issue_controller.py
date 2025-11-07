import os
from datetime import datetime
from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from sqlalchemy.orm.session import Session
from typing import Literal, Optional, Union, List
from pydantic_validation_decorator import ValidateFields
from config.get_db import get_db
from config.enums import BusinessType
from config.env import UploadConfig
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.issue_vo import (
    AddIssueModel,
    DeleteIssueModel,
    EditIssueModel,
    IssueDetailModel,
    IssueMainModel,
    IssuePageQueryModel,
    IssueStatisticsModel,
    AddDiagnosisLogModel,
    IssueStatisticsResponseModel,
    IssueListResponseModel,
    IssueDetailResponseModel,
    IssueOptionsResponseModel,
    IssueOptionItemModel,
    UploadAttachmentResponseModel, IssueAttachmentModel,
)
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.service.login_service import LoginService
from module_admin.service.issue_service import IssueService
from module_admin.service.common_service import CommonService
from module_admin.dao.issue_dao import IssueDao
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from utils.upload_util import UploadUtil
from utils.common_util import bytes2file_response


issueController = APIRouter(
    prefix="/system/issue", dependencies=[Depends(LoginService.get_current_user)]
)


@issueController.get(
    "/statistics",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:list"))],
    response_model=IssueStatisticsResponseModel,
    name="获取Issue统计数据",
)
def get_issue_statistics(request: Request, query_db: Session = Depends(get_db)):
    """
    获取Issue统计数据
    """
    statistics_result = IssueService.get_issue_statistics_services(query_db)
    logger.info("获取Issue统计数据成功")
    return ResponseUtil.success(data=statistics_result)


@issueController.get(
    "/list",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:list"))],
    response_model=IssueListResponseModel,
    name="获取Issue列表",
)
def get_system_issue_list(
    request: Request,
    issue_main: IssuePageQueryModel = Depends(IssuePageQueryModel.as_query),
    query_db: Session = Depends(get_db),
):
    """
    获取Issue列表
    """
    # 获取分页数据
    issue_list_result = IssueService.get_issue_list_services(
        query_db, issue_main, is_page=True
    )
    logger.info("获取成功")
    return ResponseUtil.success(data=issue_list_result)


@issueController.post(
    "/list",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:list"))],
    response_model=IssueListResponseModel,
    name="获取Issue列表（POST方式）",
)
def get_system_issue_list_post(
    request: Request,
    issue_main: IssuePageQueryModel,
    query_db: Session = Depends(get_db),
):
    """
    获取Issue列表（POST方式）
    """
    # 获取分页数据
    issue_list_result = IssueService.get_issue_list_services(
        query_db, issue_main, is_page=True
    )
    logger.info("获取成功")
    return ResponseUtil.success(data=issue_list_result)


@issueController.get(
    "/export", dependencies=[Depends(CheckUserInterfaceAuth("system:issue:export"))], name="导出Issue列表"
)
@Log(title="Issue管理", business_type=BusinessType.EXPORT)
def export_system_issue_list(
    request: Request,
    issue_main: IssuePageQueryModel = Depends(IssuePageQueryModel.as_query),
    query_db: Session = Depends(get_db),
):
    """
    导出Issue列表
    """
    # 获取全量数据 - 直接调用DAO获取数据
    issue_list_data = IssueDao.get_issue_list(query_db, issue_main, is_page=False)
    issue_export_result = IssueService.export_issue_list_services(issue_list_data)
    logger.info("导出成功")

    return ResponseUtil.streaming(data=bytes2file_response(issue_export_result))


@issueController.get(
    "/{issue_id}",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:query"))],
    response_model=IssueDetailResponseModel,
    name="获取Issue详细信息",
)
def query_detail_system_issue(
    request: Request, issue_id: int, query_db: Session = Depends(get_db)
):
    """
    获取Issue详细信息
    """
    issue_detail_result = IssueService.get_issue_detail_services(query_db, issue_id)
    if issue_detail_result is None:
        return ResponseUtil.error(msg="Issue不存在")
    logger.info(f"获取issue_id为{issue_id}的Issue信息成功")
    return ResponseUtil.success(data=issue_detail_result)


@issueController.post(
    "",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:add"))],
    response_model=CrudResponseModel,
    name="新增Issue信息",
)
# @ValidateFields(validate_model="add_issue")  # 暂时禁用
@Log(title="Issue管理", business_type=BusinessType.INSERT)
def add_system_issue(
    request: Request,
    add_issue: AddIssueModel,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    query_db: Session = Depends(get_db),
):
    """
    新增Issue信息
    """
    add_result = IssueService.add_issue_services(query_db, add_issue, current_user)
    logger.info(add_result.message)
    if add_result.is_success:
        return ResponseUtil.success(data=add_result, msg=add_result.message)
    else:
        return ResponseUtil.error(msg=add_result.message)


@issueController.put(
    "",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:edit"))],
    response_model=CrudResponseModel,
    name="编辑Issue信息",
)
@ValidateFields(validate_model="edit_issue")
@Log(title="Issue管理", business_type=BusinessType.UPDATE)
def edit_system_issue(
    request: Request,
    edit_issue: EditIssueModel,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    query_db: Session = Depends(get_db),
):
    """
    编辑Issue信息
    """
    # 设置更新信息
    edit_issue.update_by = current_user.user.user_name
    edit_issue.update_time = datetime.now()

    edit_result = IssueService.edit_issue_services(query_db, edit_issue)
    logger.info(edit_result.message)
    if edit_result.is_success:
        return ResponseUtil.success(data=edit_result, msg=edit_result.message)
    else:
        return ResponseUtil.error(msg=edit_result.message)


@issueController.delete(
    "/{issue_ids}",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:remove"))],
    response_model=CrudResponseModel,
    name="删除Issue信息",
)
@Log(title="Issue管理", business_type=BusinessType.DELETE)
def delete_system_issue(
    request: Request,
    issue_ids: str,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    query_db: Session = Depends(get_db),
):
    """
    删除Issue信息
    """
    delete_issue = DeleteIssueModel(
        issueIds=issue_ids,
        updateBy=current_user.user.user_name,
        updateTime=datetime.now(),
    )
    delete_result = IssueService.delete_issue_services(query_db, delete_issue)
    logger.info(delete_result.message)
    if delete_result.is_success:
        return ResponseUtil.success(data=delete_result, msg=delete_result.message)
    else:
        return ResponseUtil.error(msg=delete_result.message)


@issueController.post(
    "/diagnosis/log",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:edit"))],
    response_model=CrudResponseModel,
    name="新增Issue诊断记录",
)
@Log(title="Issue诊断", business_type=BusinessType.INSERT)
def add_issue_diagnosis_log(
    request: Request,
    diagnosis_log: AddDiagnosisLogModel,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    query_db: Session = Depends(get_db),
):
    """
    新增Issue诊断记录
    """
    # 设置操作信息
    diagnosis_log.operator = current_user.user.user_name
    diagnosis_log.operate_time = datetime.now()

    add_result = IssueService.add_diagnosis_log_services(query_db, diagnosis_log)
    logger.info(add_result.message)
    if add_result.is_success:
        return ResponseUtil.success(data=add_result, msg=add_result.message)
    else:
        return ResponseUtil.error(msg=add_result.message)


@issueController.post(
    "/attachment/upload",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:edit"))],
    response_model=IssueAttachmentModel,
    name="上传Issue附件（临时）",
)
def upload_issue_attachment(
    request: Request,
    file: UploadFile = File(...),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    query_db: Session = Depends(get_db),
):
    """
    上传Issue附件（临时附件，不需要issue_id）
    返回attachment_id，在创建Issue时关联
    """
    try:
        # 检查文件类型和大小
        allowed_types = [
            ".jpg",
            ".jpeg",
            ".png",
            ".pdf",
            ".zip",
            ".dmp",
            ".txt",
            ".log",
        ]
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext not in allowed_types:
            return ResponseUtil.error(msg=f"不支持的文件类型: {file_ext}")

        # 限制文件大小为100MB
        max_size = 1024 * 1024 * 1024 * 2  # 2G
        file.file.seek(0, 2)  # 移动到文件末尾
        file_size = file.file.tell()
        file.file.seek(0)  # 重置到开始位置

        if file_size > max_size:
            return ResponseUtil.error(msg="文件大小不能超过2G")

        # 使用通用上传服务上传文件
        upload_result = CommonService.upload_service(request, file)
        
        if upload_result.is_success:
            # 获取上传的文件信息
            file_info = upload_result.result
            
            # 构建物理文件路径（用于删除）
            # file_name 格式: /profile/upload/2024/01/15/xxx.log
            # 需要转换为物理路径: UploadConfig.UPLOAD_PATH/upload/2024/01/15/xxx.log
            relative_path = file_info.file_name.replace(UploadConfig.UPLOAD_PREFIX, '').lstrip('/')
            physical_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
            
            # 保存临时附件记录（不关联issue_id）
            add_result = IssueService.upload_attachment_services(
                db=query_db,
                file_name=file_info.original_filename,  # 原始文件名
                file_path=physical_path,  # 物理文件路径（用于删除）
                file_size=file_size,
                file_type=file_ext,
                upload_by=current_user.user.user_name,
            )

            logger.info(add_result.message)
            if add_result.is_success:
                # 返回附件ID和相关信息
                return ResponseUtil.success(data=add_result.result, msg=add_result.message)
            else:
                return ResponseUtil.error(msg=add_result.message)
        else:
            return ResponseUtil.error(msg="文件上传失败")

    except Exception as e:
        logger.error(f"上传附件失败: {str(e)}")
        return ResponseUtil.error(msg=f"上传失败: {str(e)}")


@issueController.delete(
    "/attachment/{attachment_id}",
    dependencies=[Depends(CheckUserInterfaceAuth("system:issue:remove"))],
    response_model=CrudResponseModel,
    name="删除Issue附件",
)
@Log(title="Issue附件管理", business_type=BusinessType.DELETE)
def delete_issue_attachment(
    request: Request, attachment_id: int, query_db: Session = Depends(get_db)
):
    """
    删除Issue附件
    """
    delete_result = IssueService.delete_attachment_services(query_db, attachment_id)
    logger.info(delete_result.message)
    if delete_result.is_success:
        return ResponseUtil.success(data=delete_result, msg=delete_result.message)
    else:
        return ResponseUtil.error(msg=delete_result.message)


@issueController.get(
    "/options/types", response_model=List[IssueOptionItemModel], name="获取Issue类型选项"
)
def get_issue_type_options(request: Request):
    """
    获取Issue类型选项
    """
    type_options_result = IssueService.get_issue_type_options()
    return ResponseUtil.success(data=type_options_result)


@issueController.get(
    "/options/priorities", response_model=List[IssueOptionItemModel], name="获取优先级选项"
)
def get_priority_options(request: Request):
    """
    获取优先级选项
    """
    priority_options_result = IssueService.get_priority_options()
    return ResponseUtil.success(data=priority_options_result)


@issueController.get(
    "/options/status", response_model=List[IssueOptionItemModel], name="获取状态选项"
)
def get_status_options(request: Request):
    """
    获取状态选项
    """
    status_options_result = IssueService.get_status_options()
    return ResponseUtil.success(data=status_options_result)


@issueController.patch(
    "/{issue_id}/status", response_model=CrudResponseModel, name="Issue状态管理"
)
@Log(title="Issue状态管理", business_type=BusinessType.UPDATE)
def update_issue_status(
    request: Request,
    issue_id: int,
    status: Literal["pending", "diagnosing", "completed", "cancelled"] = Form(...),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    query_db: Session = Depends(get_db),
):
    """
    更新Issue状态
    """
    # 构建更新对象
    edit_issue = EditIssueModel(
        issue_id=issue_id,
        status=status,
        update_by=current_user.user.user_name,
        update_time=datetime.now(),
    )

    edit_result = IssueService.edit_issue_services(query_db, edit_issue)
    logger.info(edit_result.message)
    if edit_result.is_success:
        return ResponseUtil.success(data=edit_result, msg=edit_result.message)
    else:
        return ResponseUtil.error(msg=edit_result.message)

from datetime import datetime
from sqlalchemy.orm.session import Session
from sqlalchemy import text
from typing import List
from module_admin.dao.issue_dao import IssueDao
from module_admin.entity.do.issue_do import IssueMain
from module_admin.entity.vo.issue_vo import (
    AddIssueModel,
    DeleteIssueModel,
    EditIssueModel,
    IssueMainModel,
    IssuePageQueryModel,
    IssueSystemEnvModel,
    IssueAttachmentModel,
    IssueTagModel,
    AddDiagnosisLogModel,
    IssueStatisticsResponseModel,
    IssueListResponseModel,
    IssueDetailResponseModel,
    IssueOptionsResponseModel,
    IssueOptionItemModel,
)
from utils.response_util import ResponseUtil
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.common_util import export_list2excel


class IssueService:
    """
    Issue管理模块服务层
    """

    @classmethod
    def get_issue_detail_services(cls, db: Session, issue_id: int):
        """
        获取Issue详细信息services

        :param db: orm对象
        :param issue_id: Issue ID
        :return: Issue详细信息响应模型
        """
        issue_detail_result = IssueDao.get_issue_by_id(db, issue_id)

        if not issue_detail_result.get("issue_info"):
            # 返回None表示出错，Controller层会处理
            return None

        # 转换为响应模型
        response_model = IssueDetailResponseModel(
            issue_info=issue_detail_result["issue_info"],
            system_env=issue_detail_result["system_env"],
            diagnosis_logs=issue_detail_result["diagnosis_logs"] or [],
            attachments=issue_detail_result["attachments"] or [],
            tags=issue_detail_result["tags"] or [],
        )

        return response_model

    @classmethod
    def get_issue_list_services(
            cls, db: Session, query_object: IssuePageQueryModel, is_page: bool = False
    ):
        """
        获取Issue列表信息services

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: Issue列表信息响应模型
        """
        issue_list_result = IssueDao.get_issue_list(db, query_object, is_page)

        # 如果开启分页，issue_list_result 是 PageResponseModel，否则是列表
        if is_page:
            # 转换为响应模型
            response_model = IssueListResponseModel(
                rows=issue_list_result.rows,
                page_num=issue_list_result.page_num,
                page_size=issue_list_result.page_size,
                total=issue_list_result.total,
                has_next=issue_list_result.has_next,
            )
        else:
            # 不分页时，只返回列表数据
            response_model = IssueListResponseModel(
                rows=issue_list_result, total=len(issue_list_result)
            )

        return response_model

    @classmethod
    def add_issue_services(
            cls, db: Session, add_issue: AddIssueModel, current_user=None
    ):
        """
        新增Issue信息services

        :param db: orm对象
        :param add_issue: 新增Issue对象
        :return: 新增Issue校验结果
        """
        try:
            # 生成Issue编号
            issue_number = IssueDao.generate_issue_number(db)
            # 创建Issue主记录
            add_issue_dict = add_issue.model_dump(exclude={"system_env", "tags", "attachment_ids"})
            add_issue_dict["issue_number"] = issue_number
            add_issue_dict["create_by"] = (
                current_user.user_name
                if hasattr(current_user, "user_name")
                else "admin"
            )
            add_issue_dict["create_time"] = datetime.now()
            add_issue_dict["update_by"] = (
                current_user.user_name
                if hasattr(current_user, "user_name")
                else "admin"
            )
            add_issue_dict["update_time"] = datetime.now()

            # 直接创建 SQLAlchemy 模型
            db_issue = IssueMain(**add_issue_dict)
            db.add(db_issue)
            db.flush()

            # 检查Issue编号是否已存在（这里应该在插入前检查，但由于我们设置了唯一约束，这里可以省略）

            # 添加系统环境信息
            if add_issue.system_env:
                system_env = add_issue.system_env
                system_env.issue_id = db_issue.issue_id
                IssueDao.add_system_env_dao(db, system_env)

            # 添加标签信息
            if add_issue.tags:
                for tag_name in add_issue.tags:
                    if tag_name.strip():  # 过滤空字符串
                        tag = IssueTagModel(
                            issueId=db_issue.issue_id, tagName=tag_name.strip()
                        )
                        IssueDao.add_tag_dao(db, tag)

            # 关联附件（将临时附件关联到Issue）
            if add_issue.attachment_ids:
                IssueDao.link_attachments_to_issue(db, db_issue.issue_id, add_issue.attachment_ids)

            db.commit()
            return CrudResponseModel(is_success=True, message="新增成功")

        except Exception as e:
            db.rollback()
            return CrudResponseModel(is_success=False, message=f"新增失败: {str(e)}")

    @classmethod
    def edit_issue_services(cls, db: Session, edit_issue: EditIssueModel):
        """
        编辑Issue信息services

        :param db: orm对象
        :param edit_issue: 编辑Issue对象
        :return: 编辑Issue校验结果
        """
        try:
            # 检查Issue是否存在
            existing_issue = IssueDao.get_issue_by_id(db, edit_issue.issue_id)
            if not existing_issue.get("issue_info"):
                return CrudResponseModel(is_success=False, message="Issue不存在")

            # 更新Issue主记录 - 只更新提供的字段，排除None值
            edit_issue_dict = edit_issue.model_dump(
                exclude={"system_env", "tags"}, exclude_none=True
            )
            edit_issue_dict["issue_id"] = edit_issue.issue_id
            edit_issue_dict["update_time"] = datetime.now()

            # 移除issue_number字段，编辑时不允许修改
            if "issue_number" in edit_issue_dict:
                del edit_issue_dict["issue_number"]

            # 验证字段
            if "title" in edit_issue_dict:
                edit_issue_main = IssueMainModel(title=edit_issue_dict["title"])
                edit_issue_main.validate_fields()

            IssueDao.edit_issue_dao(db, edit_issue_dict)

            # 更新系统环境信息
            if edit_issue.system_env:
                system_env_dict = edit_issue.system_env.model_dump()
                system_env_dict["issue_id"] = edit_issue.issue_id

                if existing_issue.get("system_env"):
                    # 更新现有环境信息
                    env_info = existing_issue["system_env"]
                    system_env_dict["env_id"] = (
                        env_info.env_id
                        if hasattr(env_info, "env_id")
                        else env_info.get("env_id")
                    )
                    IssueDao.edit_system_env_dao(db, system_env_dict)
                else:
                    # 新增环境信息
                    system_env = IssueSystemEnvModel(**system_env_dict)
                    IssueDao.add_system_env_dao(db, system_env)

            # 更新标签信息（先删除后新增）
            if edit_issue.tags is not None:
                IssueDao.delete_tags_by_issue_dao(db, edit_issue.issue_id)

                for tag_name in edit_issue.tags:
                    if tag_name.strip():
                        tag = IssueTagModel(
                            issue_id=edit_issue.issue_id, tag_name=tag_name.strip()
                        )
                        IssueDao.add_tag_dao(db, tag)

            db.commit()
            return CrudResponseModel(is_success=True, message="编辑成功")

        except Exception as e:
            db.rollback()
            return CrudResponseModel(is_success=False, message=f"编辑失败: {str(e)}")

    @classmethod
    def delete_issue_services(cls, db: Session, delete_issue: DeleteIssueModel):
        """
        删除Issue信息services

        :param db: orm对象
        :param delete_issue: 删除Issue对象
        :return: 删除Issue校验结果
        """
        try:
            delete_issue_id_list = delete_issue.issue_ids.split(",")

            for issue_id in delete_issue_id_list:
                if issue_id.strip():
                    existing_issue = IssueDao.get_issue_by_id(db, int(issue_id))
                    if existing_issue.get("issue_info"):
                        delete_issue_obj = IssueMainModel(
                            issue_id=int(issue_id),
                            update_by=delete_issue.update_by,
                            update_time=delete_issue.update_time,
                        )
                        IssueDao.delete_issue_dao(db, delete_issue_obj)

            db.commit()
            return CrudResponseModel(is_success=True, message="删除成功")

        except Exception as e:
            db.rollback()
            return CrudResponseModel(is_success=False, message=f"删除失败: {str(e)}")

    @classmethod
    def add_diagnosis_log_services(
            cls, db: Session, diagnosis_log: AddDiagnosisLogModel
    ):
        """
        新增诊断记录services

        :param db: orm对象
        :param diagnosis_log: 诊断记录对象
        :return: 新增诊断记录校验结果
        """
        try:
            # 检查Issue是否存在
            existing_issue = IssueDao.get_issue_by_id(db, diagnosis_log.issue_id)
            if not existing_issue.get("issue_info"):
                return CrudResponseModel(is_success=False, message="Issue不存在")

            # 添加诊断记录
            IssueDao.add_diagnosis_log_dao(db, diagnosis_log)

            # 如果Issue状态为待诊断，则更新为诊断中
            issue_info = existing_issue["issue_info"]
            current_status = (
                issue_info.status
                if hasattr(issue_info, "status")
                else issue_info.get("status")
            )
            if current_status == "pending":
                issue_update_dict = {
                    "issue_id": diagnosis_log.issue_id,
                    "status": "diagnosing",
                    "update_time": datetime.now(),
                }
                IssueDao.edit_issue_dao(db, issue_update_dict)

            db.commit()
            return CrudResponseModel(is_success=True, message="新增诊断记录成功")

        except Exception as e:
            db.rollback()
            return CrudResponseModel(
                is_success=False, message=f"新增诊断记录失败: {str(e)}"
            )

    @classmethod
    def upload_attachment_services(
            cls,
            db: Session,
            file_name: str,
            file_path: str,
            file_size: int,
            file_type: str,
            upload_by: str,
    ):
        """
        上传附件services（临时附件，不需要issue_id）

        :param db: orm对象
        :param file_name: 文件名
        :param file_path: 文件路径
        :param file_size: 文件大小
        :param file_type: 文件类型
        :param upload_by: 上传者
        :return: 上传附件校验结果，包含attachment_id
        """
        try:
            # 创建临时附件记录（不关联issue_id）
            attachment = IssueAttachmentModel(
                issueId=None,  # 临时附件，不关联Issue
                fileName=file_name,
                filePath=file_path,
                fileSize=file_size,
                fileType=file_type,
                uploadBy=upload_by,
                uploadTime=datetime.now(),
                status="temporary",  # 标记为临时状态
            )

            IssueDao.add_attachment_dao(db, attachment)
            db.flush()  # 刷新以获取attachment_id
            
            # 获取生成的attachment_id
            attachment_id = db.execute(
                text("SELECT LAST_INSERT_ID()")
            ).scalar()

            db.commit()
            attachment.attachment_id = attachment_id
            # 返回附件信息
            return CrudResponseModel(
                is_success=True, 
                message="上传附件成功",
                result=attachment,
            )

        except Exception as e:
            db.rollback()
            return CrudResponseModel(
                is_success=False, message=f"上传附件失败: {str(e)}"
            )

    @classmethod
    def delete_attachment_services(cls, db: Session, attachment_id: int):
        """
        删除附件services

        :param db: orm对象
        :param attachment_id: 附件ID
        :return: 删除附件校验结果
        """
        try:
            IssueDao.delete_attachment_dao(db, attachment_id)
            db.commit()

            return CrudResponseModel(is_success=True, message="删除附件成功")

        except Exception as e:
            db.rollback()
            return CrudResponseModel(
                is_success=False, message=f"删除附件失败: {str(e)}"
            )

    @classmethod
    def get_issue_statistics_services(cls, db: Session):
        """
        获取Issue统计数据services

        :param db: orm对象
        :return: 统计数据响应模型
        """
        statistics_result = IssueDao.get_issue_statistics(db)

        # 转换为响应模型
        response_model = IssueStatisticsResponseModel(**statistics_result)

        return response_model

    @classmethod
    def get_issue_type_options(cls):
        """
        获取Issue类型选项

        :return: Issue类型选项响应模型
        """
        issue_types = [
            {"label": "BUG报告", "value": "BUG"},
            {"label": "问题工单", "value": "工单"},
            {"label": "系统日志", "value": "系统日志"},
            {"label": "测试报告", "value": "测试报告"},
            {"label": "功能需求", "value": "功能需求"},
            {"label": "性能优化", "value": "性能优化"},
            {"label": "其他", "value": "其他"},
        ]

        # 转换为响应模型
        response_model = [IssueOptionItemModel(**item) for item in issue_types]

        return response_model

    @classmethod
    def get_priority_options(cls):
        """
        获取优先级选项

        :return: 优先级选项响应模型
        """
        priority_options = [
            {"label": "高", "value": "high"},
            {"label": "中", "value": "medium"},
            {"label": "低", "value": "low"},
        ]

        # 转换为响应模型
        response_model = [IssueOptionItemModel(**item) for item in priority_options]

        return response_model

    @classmethod
    def get_status_options(cls):
        """
        获取状态选项

        :return: 状态选项响应模型
        """
        status_options = [
            {"label": "待诊断", "value": "pending"},
            {"label": "诊断中", "value": "diagnosing"},
            {"label": "已完成", "value": "completed"},
            {"label": "已取消", "value": "cancelled"},
        ]

        # 转换为响应模型
        response_model = [IssueOptionItemModel(**item) for item in status_options]


        return response_model

    @classmethod
    def clean_temporary_attachments_services(cls, db: Session, hours: int = 24):
        """
        清理超过指定时间的临时附件

        :param db: orm对象
        :param hours: 小时数，默认24小时
        :return: 清理结果
        """
        try:
            import os
            
            # 获取需要删除的附件列表
            attachments_to_delete = IssueDao.delete_temporary_attachments(db, hours)
            
            # 删除物理文件
            deleted_count = 0
            for attachment in attachments_to_delete:
                try:
                    file_path = attachment.file_path
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                except Exception as e:
                    # 记录文件删除失败，但继续处理
                    print(f"删除文件失败: {file_path}, 错误: {str(e)}")
            
            db.commit()
            
            return CrudResponseModel(
                is_success=True, 
                message=f"成功清理 {deleted_count} 个临时附件"
            )
        
        except Exception as e:
            db.rollback()
            return CrudResponseModel(
                is_success=False, 
                message=f"清理临时附件失败: {str(e)}"
            )

    @staticmethod
    def export_issue_list_services(issue_list: List):
        """
        导出Issue信息service

        :param issue_list: Issue信息列表
        :return: Issue信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "issueId": "Issue编号",
            "issueNumber": "Issue编号",
            "title": "Issue标题",
            "priority": "优先级",
            "status": "状态",
            "issueType": "Issue类型",
            "issueSource": "Issue来源",
            "description": "问题描述",
            "solution": "解决方案",
            "expectedResolveDate": "预期解决日期",
            "createBy": "创建者",
            "createTime": "创建时间",
            "updateBy": "更新者",
            "updateTime": "更新时间",
        }

        data = issue_list

        # 转换状态和优先级为中文
        priority_map = {"high": "高", "medium": "中", "low": "低"}

        status_map = {
            "pending": "待诊断",
            "diagnosing": "诊断中",
            "completed": "已完成",
            "cancelled": "已取消",
        }

        for item in data:
            # 转换优先级
            if item.get("priority"):
                item["priority"] = priority_map.get(
                    item.get("priority"), item.get("priority")
                )

            # 转换状态
            if item.get("status"):
                item["status"] = status_map.get(item.get("status"), item.get("status"))

            # 格式化日期
            if item.get("createTime"):
                item["createTime"] = (
                    item.get("createTime").strftime("%Y-%m-%d %H:%M:%S")
                    if hasattr(item.get("createTime"), "strftime")
                    else str(item.get("createTime"))
                )
            if item.get("updateTime"):
                item["updateTime"] = (
                    item.get("updateTime").strftime("%Y-%m-%d %H:%M:%S")
                    if hasattr(item.get("updateTime"), "strftime")
                    else str(item.get("updateTime"))
                )
            if item.get("expectedResolveDate"):
                item["expectedResolveDate"] = (
                    item.get("expectedResolveDate").strftime("%Y-%m-%d")
                    if hasattr(item.get("expectedResolveDate"), "strftime")
                    else str(item.get("expectedResolveDate"))
                )

        new_data = [
            {
                mapping_dict.get(key): value
                for key, value in item.items()
                if mapping_dict.get(key)
            }
            for item in data
        ]
        binary_data = export_list2excel(new_data)

        return binary_data

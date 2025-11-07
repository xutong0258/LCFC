from datetime import datetime, time
from typing import List
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.orm.session import Session
from module_admin.entity.do.issue_do import (
    IssueMain,
    IssueSystemEnv,
    IssueDiagnosisLog,
    IssueAttachment,
    IssueTag,
)
from module_admin.entity.vo.issue_vo import (
    IssueMainModel,
    IssuePageQueryModel,
    IssueSystemEnvModel,
    IssueDiagnosisLogModel,
    IssueAttachmentModel,
    IssueTagModel,
)
from utils.page_util import PageUtil


class IssueDao:
    """
    Issue管理模块数据库操作层
    """

    @classmethod
    def get_issue_by_id(cls, db: Session, issue_id: int):
        """
        根据issue_id获取Issue详细信息

        :param db: orm对象
        :param issue_id: Issue ID
        :return: Issue详细信息
        """
        # 获取Issue基本信息
        issue_info = (
            db.execute(
                select(IssueMain)
                .where(IssueMain.del_flag == "0", IssueMain.issue_id == issue_id)
                .distinct()
            )
            .scalars()
            .first()
        )

        # 获取系统环境信息
        system_env = (
            db.execute(
                select(IssueSystemEnv)
                .where(IssueSystemEnv.issue_id == issue_id)
                .distinct()
            )
            .scalars()
            .first()
        )

        # 获取诊断记录
        diagnosis_logs = (
            db.execute(
                select(IssueDiagnosisLog)
                .where(IssueDiagnosisLog.issue_id == issue_id)
                .order_by(desc(IssueDiagnosisLog.operate_time))
                .distinct()
            )
            .scalars()
            .all()
        )

        # 获取附件信息
        attachments = (
            db.execute(
                select(IssueAttachment)
                .where(IssueAttachment.issue_id == issue_id)
                .order_by(desc(IssueAttachment.upload_time))
                .distinct()
            )
            .scalars()
            .all()
        )

        # 获取标签信息
        tags = (
            db.execute(select(IssueTag).where(IssueTag.issue_id == issue_id).distinct())
            .scalars()
            .all()
        )

        results = dict(
            issue_info=issue_info,
            system_env=system_env,
            diagnosis_logs=diagnosis_logs,
            attachments=attachments,
            tags=tags,
        )

        return results

    @classmethod
    def get_issue_by_number(cls, db: Session, issue_number: str):
        """
        根据Issue编号获取Issue信息

        :param db: orm对象
        :param issue_number: Issue编号
        :return: Issue信息
        """
        issue_info = (
            db.execute(
                select(IssueMain)
                .where(
                    IssueMain.del_flag == "0", IssueMain.issue_number == issue_number
                )
                .distinct()
            )
            .scalars()
            .first()
        )

        return issue_info

    @classmethod
    def get_issue_list(
        cls, db: Session, query_object: IssuePageQueryModel, is_page: bool = False
    ):
        """
        根据查询参数获取Issue列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: Issue列表信息对象
        """
        query = (
            select(IssueMain)
            .where(
                IssueMain.del_flag == "0",
                IssueMain.issue_id == query_object.issue_id
                if query_object.issue_id is not None
                else True,
                IssueMain.issue_number.like(f"%{query_object.issue_number}%")
                if query_object.issue_number
                else True,
                IssueMain.title.like(f"%{query_object.title}%")
                if query_object.title
                else True,
                IssueMain.priority == query_object.priority
                if query_object.priority
                else True,
                IssueMain.status == query_object.status
                if query_object.status
                else True,
                IssueMain.issue_type == query_object.issue_type
                if query_object.issue_type
                else True,
                IssueMain.issue_source.like(f"%{query_object.issue_source}%")
                if query_object.issue_source
                else True,
                IssueMain.create_by.like(f"%{query_object.create_by}%")
                if query_object.create_by
                else True,
                IssueMain.create_time.between(
                    datetime.combine(
                        datetime.strptime(query_object.begin_time, "%Y-%m-%d"),
                        time(00, 00, 00),
                    ),
                    datetime.combine(
                        datetime.strptime(query_object.end_time, "%Y-%m-%d"),
                        time(23, 59, 59),
                    ),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .order_by(desc(IssueMain.create_time))
            .distinct()
        )

        issue_list = PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return issue_list

    @classmethod
    def add_issue_dao(cls, db: Session, issue: IssueMainModel):
        """
        新增Issue数据库操作

        :param db: orm对象
        :param issue: Issue对象
        :return: 新增校验结果
        """
        db_issue = IssueMain(**issue.model_dump())
        db.add(db_issue)
        db.flush()

        return db_issue

    @classmethod
    def edit_issue_dao(cls, db: Session, issue: dict):
        """
        编辑Issue数据库操作

        :param db: orm对象
        :param issue: 需要更新的Issue字典
        :return: 编辑校验结果
        """
        db.execute(update(IssueMain), [issue])

    @classmethod
    def delete_issue_dao(cls, db: Session, issue: IssueMainModel):
        """
        删除Issue数据库操作

        :param db: orm对象
        :param issue: Issue对象
        :return:
        """
        db.execute(
            update(IssueMain)
            .where(IssueMain.issue_id == issue.issue_id)
            .values(
                del_flag="2", update_by=issue.update_by, update_time=issue.update_time
            )
        )

    @classmethod
    def add_system_env_dao(cls, db: Session, system_env: IssueSystemEnvModel):
        """
        新增系统环境信息数据库操作

        :param db: orm对象
        :param system_env: 系统环境对象
        :return:
        """
        db_system_env = IssueSystemEnv(**system_env.model_dump())
        db.add(db_system_env)

    @classmethod
    def edit_system_env_dao(cls, db: Session, system_env: dict):
        """
        编辑系统环境信息数据库操作

        :param db: orm对象
        :param system_env: 需要更新的系统环境字典
        :return:
        """
        db.execute(update(IssueSystemEnv), [system_env])

    @classmethod
    def add_diagnosis_log_dao(cls, db: Session, diagnosis_log: IssueDiagnosisLogModel):
        """
        新增诊断记录数据库操作

        :param db: orm对象
        :param diagnosis_log: 诊断记录对象
        :return:
        """
        db_diagnosis_log = IssueDiagnosisLog(**diagnosis_log.model_dump())
        db.add(db_diagnosis_log)

    @classmethod
    def add_attachment_dao(cls, db: Session, attachment: IssueAttachmentModel):
        """
        新增附件信息数据库操作

        :param db: orm对象
        :param attachment: 附件对象
        :return:
        """
        db_attachment = IssueAttachment(**attachment.model_dump())
        db.add(db_attachment)

    @classmethod
    def delete_attachment_dao(cls, db: Session, attachment_id: int):
        """
        删除附件信息数据库操作

        :param db: orm对象
        :param attachment_id: 附件ID
        :return:
        """
        db.execute(
            delete(IssueAttachment).where(
                IssueAttachment.attachment_id == attachment_id
            )
        )

    @classmethod
    def link_attachments_to_issue(cls, db: Session, issue_id: int, attachment_ids: List[int]):
        """
        将临时附件关联到Issue

        :param db: orm对象
        :param issue_id: Issue ID
        :param attachment_ids: 附件ID列表
        :return:
        """
        if attachment_ids:
            db.execute(
                update(IssueAttachment)
                .where(IssueAttachment.attachment_id.in_(attachment_ids))
                .values(issue_id=issue_id, status="linked")
            )

    @classmethod
    def get_attachment_by_id(cls, db: Session, attachment_id: int):
        """
        根据附件ID获取附件信息

        :param db: orm对象
        :param attachment_id: 附件ID
        :return: 附件信息
        """
        attachment = (
            db.execute(
                select(IssueAttachment)
                .where(IssueAttachment.attachment_id == attachment_id)
                .distinct()
            )
            .scalars()
            .first()
        )
        return attachment

    @classmethod
    def delete_temporary_attachments(cls, db: Session, hours: int = 24):
        """
        删除超过指定时间的临时附件

        :param db: orm对象
        :param hours: 小时数，默认24小时
        :return: 删除的附件数量
        """
        from datetime import timedelta
        threshold_time = datetime.now() - timedelta(hours=hours)
        
        # 查询需要删除的附件
        attachments_to_delete = (
            db.execute(
                select(IssueAttachment)
                .where(
                    IssueAttachment.status == "temporary",
                    IssueAttachment.upload_time < threshold_time
                )
                .distinct()
            )
            .scalars()
            .all()
        )
        
        # 删除附件记录
        db.execute(
            delete(IssueAttachment).where(
                IssueAttachment.status == "temporary",
                IssueAttachment.upload_time < threshold_time
            )
        )
        
        return attachments_to_delete

    @classmethod
    def add_tag_dao(cls, db: Session, tag: IssueTagModel):
        """
        新增标签信息数据库操作

        :param db: orm对象
        :param tag: 标签对象
        :return:
        """
        db_tag = IssueTag(**tag.model_dump(by_alias=False))
        db.add(db_tag)

    @classmethod
    def delete_tags_by_issue_dao(cls, db: Session, issue_id: int):
        """
        根据Issue ID删除所有标签数据库操作

        :param db: orm对象
        :param issue_id: Issue ID
        :return:
        """
        db.execute(delete(IssueTag).where(IssueTag.issue_id == issue_id))

    @classmethod
    def get_issue_statistics(cls, db: Session):
        """
        获取Issue统计数据

        :param db: orm对象
        :return: 统计数据字典
        """
        # Issue总数
        total_count = db.execute(
            select(func.count("*"))
            .select_from(IssueMain)
            .where(IssueMain.del_flag == "0")
        ).scalar()

        # 本月新增Issue数
        current_month_start = datetime.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        monthly_new_count = db.execute(
            select(func.count("*"))
            .select_from(IssueMain)
            .where(
                IssueMain.del_flag == "0", IssueMain.create_time >= current_month_start
            )
        ).scalar()

        # 待处理Issue数
        pending_count = db.execute(
            select(func.count("*"))
            .select_from(IssueMain)
            .where(IssueMain.del_flag == "0", IssueMain.status == "pending")
        ).scalar()

        # Issue诊断次数(诊断记录总数)
        diagnosis_count = db.execute(
            select(func.count("*")).select_from(IssueDiagnosisLog)
        ).scalar()

        # 高优先级Issue数
        high_priority_count = db.execute(
            select(func.count("*"))
            .select_from(IssueMain)
            .where(IssueMain.del_flag == "0", IssueMain.priority == "high")
        ).scalar()

        # 已完成Issue数
        completed_count = db.execute(
            select(func.count("*"))
            .select_from(IssueMain)
            .where(IssueMain.del_flag == "0", IssueMain.status == "completed")
        ).scalar()

        return {
            "total_count": total_count or 0,
            "monthly_new_count": monthly_new_count or 0,
            "pending_count": pending_count or 0,
            "diagnosis_count": diagnosis_count or 0,
            "high_priority_count": high_priority_count or 0,
            "completed_count": completed_count or 0,
        }

    @classmethod
    def generate_issue_number(cls, db: Session) -> str:
        """
        生成Issue编号

        :param db: orm对象
        :return: Issue编号
        """
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day

        # 查询当天最大的Issue编号
        max_number = db.execute(
            select(func.max(IssueMain.issue_number)).where(
                IssueMain.issue_number.like(f"ISU-{year}-{month:02d}-{day:02d}-%")
            )
        ).scalar()

        print(f"Debug: max_number = {max_number}")  # 调试输出

        if max_number:
            # 提取序号并递增
            try:
                seq_num = int(max_number.split("-")[-1]) + 1
            except (ValueError, IndexError):
                seq_num = 1
        else:
            seq_num = 1

        result = f"ISU-{year}-{month:02d}-{day:02d}-{seq_num:04d}"
        print(f"Debug: generated issue_number = {result}")  # 调试输出
        return result

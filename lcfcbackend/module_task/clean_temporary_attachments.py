"""
定时清理临时附件任务
"""
from datetime import datetime
from config.database import SessionLocal
from module_admin.service.issue_service import IssueService
from utils.log_util import logger


def clean_temporary_attachments(*args, **kwargs):
    """
    清理超过24小时的临时附件
    
    这个任务会：
    1. 删除超过24小时未关联到Issue的临时附件记录
    2. 同时删除对应的物理文件
    
    :param args: 位置参数（可选）
    :param kwargs: 关键字参数（可选，可传入hours参数自定义清理时间）
    """
    try:
        # 获取清理时间（默认24小时）
        hours = kwargs.get('hours', 24) if kwargs else 24
        
        logger.info(f"[定时任务] 开始清理超过{hours}小时的临时附件...")
        
        # 创建数据库会话
        with SessionLocal() as db:
            # 调用服务层方法清理临时附件
            result = IssueService.clean_temporary_attachments_services(db, hours)
            
            if result.is_success:
                logger.info(f"[定时任务] {result.message}")
            else:
                logger.error(f"[定时任务] 清理失败: {result.message}")
        
        logger.info(f"[定时任务] 临时附件清理任务完成，时间: {datetime.now()}")
        
    except Exception as e:
        logger.error(f"[定时任务] 清理临时附件任务异常: {str(e)}")


async def async_clean_temporary_attachments(*args, **kwargs):
    """
    异步版本的清理临时附件任务
    
    :param args: 位置参数（可选）
    :param kwargs: 关键字参数（可选，可传入hours参数自定义清理时间）
    """
    clean_temporary_attachments(*args, **kwargs)


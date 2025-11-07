from config.database import engine, SessionLocal, Base
from utils.log_util import logger


def get_db():
    """
    每次使用时都从数据库中取出一个连接，使用完后放回
    :return:
    """
    return SessionLocal()


def create_table():
    """创建数据库所有的表的表"""
    logger.info('创建数据表...')
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
    logger.info('创建数据表成功')


def delete_table():
    """创建数据库所有的表的表"""
    logger.info('删除数据表...')
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
    logger.info('删除数据表成功')

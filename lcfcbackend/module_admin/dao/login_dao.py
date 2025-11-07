from sqlalchemy import and_, select
from sqlalchemy.orm.session import Session
from module_admin.entity.do.dept_do import SysDept
from module_admin.entity.do.user_do import SysUser


def login_by_account(db: Session, user_name: str):
    """
    根据用户名查询用户信息

    :param db: orm对象
    :param user_name: 用户名
    :return: 用户对象
    """
    user = (
        db.execute(
            select(SysUser, SysDept)
            .where(SysUser.user_name == user_name, SysUser.del_flag == '0')
            .join(
                SysDept,
                and_(SysUser.dept_id == SysDept.dept_id, SysDept.status == '0', SysDept.del_flag == '0'),
                isouter=True,
            )
            .distinct()
        )
    ).first()

    return user

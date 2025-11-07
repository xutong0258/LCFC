from fastapi import FastAPI
from config.get_db import create_table
from fastapi.openapi.docs import (
    get_swagger_ui_html,
)

from fastapi.staticfiles import StaticFiles
from middlewares.handle import handle_middleware
from exceptions.handle import handle_exception
from config.env import AppConfig
from config.get_scheduler import SchedulerUtil
from starlette.responses import FileResponse
from sub_applications.handle import handle_sub_applications
from utils.common_util import worship
from config.get_redis import RedisUtil
from utils.log_util import logger
from module_admin.controller import login_controller
from module_admin.controller import user_controller
from module_admin.controller import role_controller
from module_admin.controller import menu_controller
from module_admin.controller import dept_controller
from module_admin.controller import post_controler
from module_admin.controller import dict_controller
from module_admin.controller import config_controller
from module_admin.controller import online_controller
from module_admin.controller import job_controller
from module_admin.controller import server_controller
from module_admin.controller import captcha_controller
from module_admin.controller import common_controller
from module_admin.controller import notice_controller
from module_admin.controller import cache_controller
from module_admin.controller import log_controller
from module_admin.controller import issue_controller

app = FastAPI(
    docs_url=f"{AppConfig.app_root_path}/docs",
    redoc_url=f"{AppConfig.app_root_path}/redoc",
    openapi_url=f"{AppConfig.app_root_path}/openapi.json",
    title=AppConfig.app_name,
    description=f"{AppConfig.app_name}接口文档",
    version=AppConfig.app_version,
)


@app.on_event("startup")
def startup():
    logger.info(f"{AppConfig.app_name}开始启动")
    logger.info(f"✅ 配置验证:")
    logger.info(f"   - app_root_path: {AppConfig.app_root_path}")
    logger.info(f"   - FastAPI root_path: {app.root_path}")
    logger.info(f"   - docs_url: {app.docs_url}")
    logger.info(f"   - openapi_url: {app.openapi_url}")
    logger.info(
        f"🌐 正确访问地址: http://127.0.0.1:{AppConfig.app_port}{AppConfig.app_root_path}/docs"
    )
    worship()
    # create_table()
    app.state.redis = RedisUtil.create_redis_pool()
    RedisUtil.init_sys_dict(app.state.redis)
    RedisUtil.init_sys_config(app.state.redis)
    SchedulerUtil.init_system_scheduler()
    logger.info(f"{AppConfig.app_name}启动成功")


@app.on_event("shutdown")
def shutdown():
    RedisUtil.close_redis_pool(app)
    SchedulerUtil.close_system_scheduler()
    logger.info(f"{AppConfig.app_name}关闭")


handle_sub_applications(app)
handle_middleware(app)
handle_exception(app)

app.include_router(prefix=AppConfig.app_root_path,router=login_controller.loginController, tags=["登录模块"])
app.include_router(prefix=AppConfig.app_root_path,router=captcha_controller.captchaController, tags=["验证码模块"])
app.include_router(prefix=AppConfig.app_root_path,router=user_controller.userController, tags=["用户模块"])
app.include_router(prefix=AppConfig.app_root_path,router=role_controller.roleController, tags=["角色模块"])
app.include_router(prefix=AppConfig.app_root_path,router=menu_controller.menuController, tags=["菜单模块"])
app.include_router(prefix=AppConfig.app_root_path,router=dept_controller.deptController, tags=["部门模块"])
app.include_router(prefix=AppConfig.app_root_path,router=post_controler.postController, tags=["职位模块"])
app.include_router(prefix=AppConfig.app_root_path,router=dict_controller.dictController, tags=["字典模块"])
app.include_router(prefix=AppConfig.app_root_path,router=config_controller.configController, tags=["参数模块"])
app.include_router(prefix=AppConfig.app_root_path,router=notice_controller.noticeController, tags=["通知模块"])
app.include_router(prefix=AppConfig.app_root_path,router=log_controller.logController, tags=["日志模块"])
app.include_router(prefix=AppConfig.app_root_path,router=online_controller.onlineController, tags=["监控模块"])
app.include_router(prefix=AppConfig.app_root_path,router=job_controller.jobController, tags=["定时任务模块"])
app.include_router(prefix=AppConfig.app_root_path,router=server_controller.serverController, tags=["菜单管理模块"])
app.include_router(prefix=AppConfig.app_root_path,router=cache_controller.cacheController, tags=["缓存监控模块"])
app.include_router(prefix=AppConfig.app_root_path,router=common_controller.commonController, tags=["通用模块"])
app.include_router(prefix=AppConfig.app_root_path,router=issue_controller.issueController, tags=["Issue管理模块"])

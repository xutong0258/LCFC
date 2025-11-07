from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config.env import UploadConfig


def mount_staticfiles(app: FastAPI):
    """
    挂载静态文件
    """
    # 作用访问127.0.0.1:8080/assets/authRole-BXfygfQq.js -> 127.0.0.1:8080/public/assets/authRole-BXfygfQq.js
    # app.mount("/assets", StaticFiles(directory="public/assets"), name='assets')
    app.mount(f'{UploadConfig.UPLOAD_PREFIX}', StaticFiles(directory=f'{UploadConfig.UPLOAD_PATH}'), name='profile')


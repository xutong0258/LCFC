from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware


def add_gzip_middleware(app: FastAPI):
    """
    添加gzip压缩中间件
    当客户端（浏览器或其他 HTTP 客户端）支持 GZip 压缩并在请求头中包含 Accept-Encoding: gzip 时，
    GZipMiddleware 会自动对响应进行压缩。对于支持 GZip 的客户端来说，这可以减少带宽占用、
    加快响应速度。
    :param app: FastAPI对象
    :return:
    """
    app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=9)

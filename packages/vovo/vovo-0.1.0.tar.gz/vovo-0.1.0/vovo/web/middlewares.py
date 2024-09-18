from starlette.middleware.cors import CORSMiddleware

from vovo.settings import global_settings


def add_cors_middleware(app):
    """cors中间件"""
    origins = [str(origin).strip("/") for origin in global_settings.CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # 允许的来源
        allow_credentials=True,  # 允许发送 cookies
        allow_methods=["*"],  # 允许的 HTTP 方法，例如 GET, POST 等
        allow_headers=["*"],  # 允许的 HTTP 头
    )
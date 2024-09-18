import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


def get_env_file(env: Optional[str] = None) -> str:
    """
    获取环境的 .env 文件路径。
    如果未指定环境，默认返回 `.env` 文件。
    如果指定了环境，则返回 `.env.{environment}` 文件。
    """
    if env is None:
        # 如果没有传递任何环境，并且系统环境变量 `APP_ENV` 也未设置，则使用默认的 `.env` 文件
        return ".env"

    # 如果明确指定了环境，加载对应的 `.env.{env}` 文件
    return f".env.{env}"


# 在程序启动时只加载一次 .env 文件
@lru_cache()
def load_env_file():
    env_file = get_env_file()
    load_dotenv(env_file)


class VovoBaseSettings(BaseSettings):
    # 应用的配置项
    SENTRY_URI: str

    # 使用 ConfigDict 替代 class-based Config
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding='utf-8',
        extra="allow"  # 允许 .env 文件中存在未定义的字段
    )

    def __init__(self, **kwargs):
        # 确保每次实例化时，.env 文件已经加载
        load_env_file()
        super().__init__(**kwargs)


# 运行时手动指定环境（可以通过传参或系统环境变量）
global_settings = VovoBaseSettings()

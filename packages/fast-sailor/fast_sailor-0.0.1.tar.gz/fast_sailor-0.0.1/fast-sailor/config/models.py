from typing import Any, Dict, Literal, Optional, Union

from pydantic import BaseModel, Field
from uvicorn.config import LOGGING_CONFIG

from core.const import CONFIG_DIR_PATH, LOGGER_CONFIGS


# uvicorn服务器配置
class ServerConfig(BaseModel):
    app: str = Field(default="core.app:App._app_", frozen=True)
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False
    log_config: Union[Dict[str, Any], str] = Field(
        default_factory=lambda: ServerConfig.get_log_config()
    )
    workers: int = 0
    factory: bool = False

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        # 根据 factory 属性设置 app 字段
        if self.factory:
            object.__setattr__(self, "app", "core.app:App._init_app")
        else:
            object.__setattr__(self, "app", "core.app:App._app_")

    @staticmethod
    def get_log_config() -> Union[Dict[str, Any], str]:
        for log_config in LOGGER_CONFIGS:
            log_config_path = CONFIG_DIR_PATH / log_config
            if log_config_path.exists():
                return str(log_config_path)

        return LOGGING_CONFIG


# FastAPI配置
class FastAPIConfig(BaseModel):
    debug: bool = False
    title: str = "FastAPI Project"
    description: str = "A fastAPI project"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    version: str = "0.0.1"
    root_path: str = Field(default="/", alias="prefix")
    server: ServerConfig = ServerConfig()


# Nacos配置
class NacosConfig(BaseModel):
    enabled: bool = False
    host: str = "127.0.0.1:8848"
    namespace: str = "public"
    data_id: Optional[str] = None  # data_id 可能为空
    group: str = "DEFAULT_GROUP"
    username: str = "nacos"
    password: str = "nacos"


# Redis配置
class RedisConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0


# 数据库配置
class DatabaseConfig(BaseModel):
    name: Optional[str] = None
    database_type: Literal["mysql", "postgresql"] = Field(default="mysql", alias="type")
    host: str = "127.0.0.1"
    port: int
    username: str
    password: str
    database: str


# 整体应用配置
class AppConfig(BaseModel):
    active: str = "default"
    app: Optional[FastAPIConfig] = FastAPIConfig()  # FastAPI 应用配置
    nacos: Optional[NacosConfig] = None  # Nacos配置
    redis: Optional[RedisConfig] = None  # Redis 配置
    database: Optional[DatabaseConfig] = None  # 数据源配置

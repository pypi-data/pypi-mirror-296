import os
from typing import Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.environ.get("API_KEY") or self.api_key
        self.base_url = os.environ.get("BASE_URL") or self.base_url
        self.model = os.environ.get("MODEL") or self.model


settings = Config()

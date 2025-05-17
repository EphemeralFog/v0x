from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings, env_file=".env"):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    MAX_SIZE: int = 2 * 1024 * 1024 * 1024  # 2 GB
    PORT: int = 8080
    HOST_URL: str = 'http://localhost'
    DB_URI: str
    LOG_TO_FILE: bool = True
    
    API_BASE_URL: str = "https://api.telegram.org"
    
    @computed_field
    @property
    def TELEGRAM_API_URL_BASE(self) -> str:
        return f"{self.API_BASE_URL}/bot{self.TELEGRAM_BOT_TOKEN}"
    
    @computed_field
    @property
    def TELEGRAM_FILE_URL_BASE(self) -> str:
        return f"{self.API_BASE_URL}/file/bot{self.TELEGRAM_BOT_TOKEN}"


settings = Settings() 
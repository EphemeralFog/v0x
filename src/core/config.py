from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings, env_file=".env"):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    MAX_SIZE: int = 2 * 1024 * 1024 * 1024  # 2 GB
    PORT: int = 8080
    DB_URI: str
    
    @computed_field
    @property
    def TELEGRAM_API_URL_BASE(self) -> str:
        return f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}"

settings = Settings() 
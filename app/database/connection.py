from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # Telegram
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str

    # Database - Make it required with no default
    MONGODB_URI: str

    REDIS_URL: Optional[str] = None

    # Bot Config
    OWNER_ID: int
    ADMINS: str = ""
    FORCE_SUB_CHANNELS: str = ""
    CHANNEL_ID: Optional[int] = None

    # Server
    BASE_URL: str
    PORT: int = 8000
    DEBUG: bool = False

    DEFAULT_EXPIRY: int = 24

    SESSIONS: str = ""

    @property
    def admin_list(self) -> List[int]:
        if not self.ADMINS.strip():
            return [self.OWNER_ID]
        return [int(x.strip()) for x in self.ADMINS.split(",") if x.strip()]

    @property
    def fsub_list(self) -> List[int]:
        if not self.FORCE_SUB_CHANNELS.strip():
            return []
        return [int(x.strip()) for x in self.FORCE_SUB_CHANNELS.split(",") if x.strip()]

    @property
    def session_list(self) -> List[str]:
        if not self.SESSIONS.strip():
            return []
        return [x.strip() for x in self.SESSIONS.split(",") if x.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        case_sensitive = True


# Initialize
settings = Settings()

# MongoDB
client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client.get_database("tg_media_bot")

files_col = db.files
users_col = db.users
settings_col = db.settings
logs_col = db.logs


async def create_indexes():
    await files_col.create_index("short_code", unique=True)
    await files_col.create_index("file_id")
    await users_col.create_index("user_id", unique=True)
    await files_col.create_index("expiry_time", expireAfterSeconds=0)


# Debug
if settings.DEBUG:
    print("✅ Settings Loaded!")
    print(f"MongoDB URI: {settings.MONGODB_URI[:50]}...")  # Partial for security
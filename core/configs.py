import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(dotenv_path=".env", override=True)
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

class Configs(BaseSettings):
    APP_BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_STORAGE_DIR: str = os.path.join(APP_BASE_DIR, "storage")

    APP_NAME: str = "aivt"
    APP_SERVES: str = "api"
    OWNER_USERNAME: str
    GEMINI_API_KEY: str
    DISCORD_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

configs = Configs()
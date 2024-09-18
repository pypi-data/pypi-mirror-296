from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="POSTGRES_",
    )

    user: str
    password: str
    host: str
    port: str
    db: str

    @property
    def url(self) -> str:
        """Concatenate .env db-params to url."""
        db_url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        return db_url


database_config = DatabaseConfig()

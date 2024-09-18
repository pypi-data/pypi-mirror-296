from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class NetworkConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="FACECLOUD_",
    )

    base_url: str
    access_token: str


network_config = NetworkConfig()

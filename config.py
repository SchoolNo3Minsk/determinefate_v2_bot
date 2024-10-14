from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: SecretStr
    db_url: SecretStr

    chromedriver_path: str

    model_config = SettingsConfigDict(
        env_file="./data/.env",
        env_file_encoding="utf-8"
    )


settings: Settings = Settings()

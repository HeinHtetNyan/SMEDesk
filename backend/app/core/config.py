from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "SMEDesk API"
    environment: str = "development"

    database_url: str = "postgresql+asyncpg://smedesk:smedesk@localhost:5432/smedesk"

    jwt_secret: str = "change-me-in-.env"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 12

    cors_origins: list[str] = ["http://localhost:5173", "tauri://localhost", "capacitor://localhost"]


settings = Settings()

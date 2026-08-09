"""Application configuration management."""


from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "InsightForge"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "local-dev-secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"

    # A list of trusted origins for CORS. e.g., ["http://localhost:3000"]
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "insightforge"

    SALESFORCE_CLIENT_ID: str | None = None
    SALESFORCE_CLIENT_SECRET: str | None = None
    SALESFORCE_REDIRECT_URI: AnyHttpUrl | None = None
    SALESFORCE_LOGIN_URL: str = "https://login.salesforce.com"
    SALESFORCE_TOKEN_FILE: str = ".salesforce_token.json"
    SALESFORCE_PKCE_CACHE_FILE: str = ".salesforce_pkce_cache.json"
    PARDOT_BUSINESS_UNIT_ID: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.example"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

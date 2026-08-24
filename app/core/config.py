from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # -------------------------
    # Gemini
    # -------------------------
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"

    # -------------------------
    # Upstage
    # -------------------------
    UPSTAGE_API_KEY: str = ""
    SOLAR_MODEL: str = "solar-pro3"

    MAX_RETRY: int = 3
    RETRY_DELAY: int = 2

    # -------------------------
    # DB
    # -------------------------
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
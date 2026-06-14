from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ------------------------
    # DATABASE & AUTH
    # ------------------------
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200

    # ------------------------
    # OPENAI / AI GENERATOR
    # ------------------------
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "mistralai/mistral-7b-instruct:free"
    ENABLE_AI_GENERATOR: bool = True

    # ------------------------
    # EMAIL (DAILY AI TIPS)
    # ------------------------
    EMAIL_FROM: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int

    # ------------------------
    # ENVIRONMENT
    # ------------------------
    ENV: str = "development"

    class Config:
        env_file = ".env"
        extra = "ignore"   # ✅ prevents crashes if you add new env vars later

settings = Settings()

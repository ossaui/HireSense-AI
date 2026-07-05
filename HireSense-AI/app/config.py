from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HireSense AI"
    environment: str = "development"
    database_url: str = "sqlite:///./hiresense.db"
    backend_cors_origins: str = "http://localhost:8501,http://127.0.0.1:8501"
    use_sentence_transformers: bool = False
    hiresense_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    openai_api_key: str | None = Field(default=None)
    ollama_base_url: str = "http://localhost:11434"
    llm_provider: str = "template"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

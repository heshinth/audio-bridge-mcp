from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Read from environment variables (set via the MCP client's `env` block)."""

    model_config = SettingsConfigDict(env_prefix="AUDIO_", env_file=".env", extra="ignore")

    api_key: str
    base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    model: str = "gemini-3.5-flash"
    max_file_mb: int = 20
    timeout_seconds: float = 120


def load_settings() -> Settings:
    return Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""  # rename if using a different provider
    openai_model: str = "gpt-4o-mini"  # update to match your chosen model

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://imp:imp@postgres:5432/imp"
    cors_origins: str = "http://localhost:5173"
    imp_bootstrap_defaults: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [value.strip() for value in self.cors_origins.split(",") if value.strip()]


settings = Settings()

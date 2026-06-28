from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    app_name: str = "ReviewDibo API"
    debug: bool = False

    model_config = {"env_file": ".env"}


settings = Settings()

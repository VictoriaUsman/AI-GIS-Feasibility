from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/gis_feasibility"
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    data_dir: str = "./data"

    class Config:
        env_file = ".env"


settings = Settings()

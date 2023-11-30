from pydantic import BaseSettings


class Settings(BaseSettings):
    # mongodb_uri: str = "mongodb://db:27017" when running in container
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "google_calendar_assistant_database"

    class Config:
        env_file = ".env"


settings = Settings()

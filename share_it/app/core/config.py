import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    app_title: str = 'Share It'
    description: str = 'Description'
    database_url: str

    class Config:
        env_file = 'C:\\Users\\stein\\PycharmProjects\\techTasks\\share_it\\.env'


settings = Settings()

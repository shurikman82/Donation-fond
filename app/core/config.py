from pydantic import BaseSettings

class Settings(BaseSettings):
    app_title: str = 'Кошачий фонд'
    app_description: str = 'Поддержи пушистых друзей!'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()

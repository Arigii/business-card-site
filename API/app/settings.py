from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    PREFIX: str = ''
    ALGORITHM: str = 'HS256'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()


def get_auth_data():
    return {
        'secret_key': settings.SECRET_KEY,
        'algorithm': settings.ALGORITHM
    }

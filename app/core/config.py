from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME:str='Footy Connects'
    DEBUG:bool=True
    DATABASE_URL:str=Field(...,env="DATABASE_URL")
    JWT_SECRET_KEY:str =Field(...,env='JWT_SECRET_URL')
    JWT_ALGORITHM :str =Field(...,env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES :str=Field(...,env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file='.env'

settings=Settings()

from pydantic_settings import BaseSettings

class DBSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    class Config:
        env_file = '.env'
        extra = 'ignore'
        
class BotSettings(BaseSettings):
    BOT_TOKEN: str
    
    class Config:
        env_file = '.env'
        extra = 'ignore'        

class LogSettings(BaseSettings):
    LOG_LEVEL: str
    LOG_FORMAT: str

    class Config:
        env_file = '.env'
        extra = 'ignore'

db_settings = DBSettings()
bot_settings = BotSettings()
log_settings = LogSettings()
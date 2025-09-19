from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str 
    JWT_SECRET_KEY: str = "test"

    INSTANCE_ID:str = "c23f9095-0974-406c-9d58-2b53346bc6ff"
    SH_CLIENT_ID:str= "09c0e84a-114e-45c4-9b31-5d8aee8ce1bd"
    SH_CLIENT_SECRET:str = "aBFUCIS9NtDez8JvpLnbyS1m1ngtyDCA"    
    
    model_config = SettingsConfigDict(env_file=".env")



settings = Settings()
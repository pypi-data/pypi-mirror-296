from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class MyConfig(BaseSettings):
    # Keep sorted
    db_name: str = Field(env="DB_NAME")
    db_password: str = Field(env="DB_PASSWORD")
    db_uri: str = Field(env="DB_URI")
    db_username: str = Field(env="DB_USERNAME")

    class Config:
        env_file = ".env"
        extra = "allow"


config = MyConfig()

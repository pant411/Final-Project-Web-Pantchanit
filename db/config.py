from pydantic import BaseSettings

class Settings(BaseSettings):
    userDB: str 
    passwdDB: str
    hostDB: str 
    portDB: int
    nameDB: str
    serviceDB: str

    class Config:
        env_file = "../.env"
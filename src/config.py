from pydantic import BaseSettings

class Settings(BaseSettings):
    
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    class Config:
        env_file = "C:/Users/Master/PycharmProjects/Vidhyadhan_Attendance_Management/src/.env"
       
settings = Settings()


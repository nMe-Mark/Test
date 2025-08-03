import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://auth-db:27017/auth-db")

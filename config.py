from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
  # SQLALCHEMY_DATABASE_URI = "postgres://u5ukamjvoufs81:pddbfe72a878c0a72501a5ed0941fc6f95180e09d91330dfd9de9492705abb595@cet8gijgk7sjl9.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6fnkkfeco37q9"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY = os.environ.get("SECRET_KEY")
  CACHE_TYPE = "SimpleCache"
  CACHE_REDIS_URL = os.environ.get("REDIS_URL")
  CELERY = {
    "broker_url": os.environ.get("REDIS_URL"),
    "result_backend": os.environ.get("REDIS_URL"),
  }
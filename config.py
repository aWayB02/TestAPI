import os


class Config:
    DATABASE_URL = "sqlite:///./todo.db"

    DEBUG = True
    ENV = "development"

    API_TITLE = "To-Do List API"
    API_VERSION = "1.0.0"
    OPENAPI_VERSION = "3.0.2"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

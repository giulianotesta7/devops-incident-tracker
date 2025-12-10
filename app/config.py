import os

class config:
    DB_HOST = os.getenv('DB_HOST')
    DB_MYSQL= os.getenv('DB_MYSQL')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
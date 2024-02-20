import json
# import pymysql       

with open('flaskapp/config.json') as config_file:
    config = json.load(config_file)

class Config:
    SECRET_KEY = config.get("SECRET_KEY")
    JWT_SECRET_KEY = config.get("JWT_SECRET_KEY")

    MAIL_PORT = 587
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_USE_TLS = True
    MAIL_USERNAME = "temansehatapp@gmail.com"
    MAIL_PASSWORD = config.get("MAIL_PASSWORD")
    

    DATABASE_INFORMATION = ""

    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://temansehatadmin:{password}@34.101.152.141/temansehatdb?unix_socket=/cloudsql/nlp-project-for-gsc:asia-southeast2:mysql-database-temansehat".format(password=config.get("DATABASE_USER_PASSWORD"))


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = "Content-Type"
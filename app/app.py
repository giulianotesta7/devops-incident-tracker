from flask import Flask
from flask_migrate import Migrate
from routes import bp
from flask_sqlalchemy import SQLAlchemy
from config import config
from database import db

user = config.DB_USER
password = config.DB_PASSWORD
host = config.DB_HOST
dbname = config.DB_MYSQL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os




app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

#handles all routes to blog path

db = SQLAlchemy(app)

migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_commamd('db', MigrateCommand)
# Use the app context to create the database tables
# with app.app_context():
#     if not os.path.exists('Database.db'):
#         db.create_all()

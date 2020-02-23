from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import os

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)


base_folder = os.path.split(os.path.abspath(__file__))[0]
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# from .views import , AnonymousView, Login, Logout, VerifyToken
#
# api.add_resource(PostList, '/list', '/detail/<uuid:path>/')
# api.add_resource(AnonymousView, '/session')
# api.add_resource(Login, '/login')
# api.add_resource(VerifyToken, '/verify')
# api.add_resource(Logout, '/logout')

from . import views

api.add_resource(views.Login, '/login')
api.add_resource(views.Register, '/register')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port="5500")

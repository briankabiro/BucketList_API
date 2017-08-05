from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from instance.config import app_config
from app.resources import BucketListApi
db = SQLAlchemy()
from app.models import User, Bucket, BucketItem

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	with app.app_context():
		db.create_all()
	return app

app = create_app(config_name="development")
api = Api(app)

api.add_resource(BucketListApi, '/bucketlists/<id>')
if __name__ == '__main__':
	app.run(debug=True)
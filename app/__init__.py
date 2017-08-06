from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from instance.config import app_config
db = SQLAlchemy()
from app.models import User, Bucket, BucketItem
from app.resources.bucketlist import BucketListApi, BucketListsApi

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	return app

app = create_app(config_name='development')
api = Api(app)
api.add_resource(BucketListApi, '/bucketlists/<id>')
api.add_resource(BucketListsApi, '/bucketlists/')

if __name__ == '__main__':
	app.run(debug=True)
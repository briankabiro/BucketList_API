from app import create_app
from flask_restful import Api
from app.models import User, Bucket, BucketItem
from app.resources.bucketlist import BucketListApi, BucketListsApi

app = create_app(config_name='development')
api = Api(app)
api.add_resource(BucketListApi, '/bucketlists/<id>')
api.add_resource(BucketListsApi, '/bucketlists/')

if __name__ == '__main__':
	app.run()
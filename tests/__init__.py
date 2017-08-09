from app import create_app, db
from flask_restful import Api
from app.models import User, Bucket, BucketItem
from app.resources.bucketlist import BucketListApi, BucketListsApi


class TestBase(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config_name='testing')
		self.client = self.app.test_client()
		self.test_user = {'username':'john', 'password':'32331'}
		self.test_user1 = {'username':'john', 'password':'12356'}

		with self.app.app_context():
			db.create_all()

		api = Api(app)
		api.add_resource(BucketListApi, '/bucketlists/<id>')
		api.add_resource(BucketListsApi, '/bucketlists/')

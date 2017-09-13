import unittest
from app import create_app
from app import db
from flask_restful import Api
from app.resources.items import ItemApi, ItemsApi
from app.resources.bucketlist import BucketListApi, BucketListsApi
from app.resources.auth import Register, Login, ResetPassword, Logout
import json

class AuthTestBase(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config_name='testing')

		# api config
		api = Api(self.app)
		api.add_resource(BucketListApi, '/bucketlists/<id>')
		api.add_resource(BucketListsApi, '/bucketlists/')
		api.add_resource(Register, '/auth/register')
		api.add_resource(Login, '/auth/login')
		api.add_resource(Logout, '/auth/logout')
		api.add_resource(ResetPassword, '/auth/reset-password')
		api.add_resource(ItemsApi, '/bucketlists/<id>/items/')
		api.add_resource(ItemApi, '/bucketlists/<id>/items/<item_id>')
		self.client = self.app.test_client()

		self.test_user = {'username':'john', 'password':'32331'}
		self.test_user1 = {'username':'john', 'password':'12356'}
		# data parameters
		db.create_all(app=self.app)

	def tearDown(self):
		db.session.remove()
		db.drop_all(app=self.app)

	def register_user(self):
		# register a user
		return self.client.post('/auth/register', data=self.test_user)

class TestBase(unittest.TestCase):
	def register_user(self):
		# register a user
		return self.client.post('/auth/register', data=self.test_user)
	
	def login_user(self):
		# login a user
		return self.client.post('/auth/login', data=self.test_user)

	def setUp(self):
		self.app = create_app(config_name='testing')

		# api config
		api = Api(self.app)
		api.add_resource(BucketListApi, '/bucketlists/<id>')
		api.add_resource(BucketListsApi, '/bucketlists/')
		api.add_resource(Register, '/auth/register')
		api.add_resource(Login, '/auth/login')
		api.add_resource(ResetPassword, '/auth/reset-password')
		api.add_resource(ItemsApi, '/bucketlists/<id>/items/')
		api.add_resource(ItemApi, '/bucketlists/<id>/items/<item_id>')
		self.client = self.app.test_client()

		# data parameters
		self.bucket = {'name': 'Hiking'}
		self.bucket1 = {'name': 'Under 30'}
		self.test_user = {'username':'loki', 'password': 'pwd12345'}
		self.item = {'description': 'sleep'}
		self.item1 = {'description':'produce'}

		# init config
		self.register_user()
		self.token = json.loads(self.login_user().data.decode())['token']
		self.headers = dict(Authorization="Bearer " + self.token)
		db.create_all(app=self.app)

	def create_bucket(self, token):
		return self.client.post(
			'/bucketlists/',
			headers=self.headers,	
			data=self.bucket
		)

	def create_item(self, token):
		return self.client.post(
			'/bucketlists/1/items/',
			headers=self.headers,	
			data=self.item
		)

	def tearDown(self):
		db.session.remove()
		db.drop_all(app=self.app)

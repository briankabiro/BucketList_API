import unittest

from app import db
from run import app
from flask import json

class AppTestCase(unittest.TestCase):
	def setUp(self):
		# initial config before each test is run
		self.app = app
		self.client = self.app.test_client()
		self.bucket = {'name': 'Hiking'}
		self.bucket1 = {'name': 'Under 30'}
		self.test_user = {'username':'loki', 'password': 'pwd12345'}
		self.item = {'description':'go to zanzibar'}
		self.item1 = {'description':'work on house'}
		with self.app.app_context():
			db.create_all()
	
	
	def register_user(self):
		# register a user
		return self.client.post('/auth/register', data=self.test_user)
	
	def login_user(self):
		# login a user
		return self.client.post('/auth/login', data=self.test_user)

	def create_bucket(self, token):
		return self.client.post(
			'/bucketlists/',
			headers=dict(Authorization="Bearer " + token),	
			data=self.bucket
		)
	
	def create_item(self, token):
		return self.client.post(
			'/bucketlists/1',
			headers=dict(Authorization="Bearer " + token),
			data=self.item
		)

	def Test_bucket_created(self):
		# test to check that bucket list is created
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		rv = self.create_bucket(token)

		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		self.assertEqual(data['owned_by'], 1)

	def Test_user_buckets_are_returned(self):
		# test to check that all bucketlists are returned
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		self.create_bucket(token)

		response = self.client.get(
			'/bucketlists/', 
			headers=dict(Authorization="Bearer " + token))
		
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.data)
		self.assertEqual(data[0]['owned_by'], 1)

	def Test_get_bucketlist_by_id(self):
		# test that bucket is returned by appending id to path
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		rv = self.create_bucket(token)
		self.assertEqual(rv.status_code, 201)
		
		result = self.client.get(
			'/bucketlists/1', 
			headers=dict(Authorization="Bearer " + token))
		# expect to fail because of str(result.data)
		self.assertIn('Hiking', str(result.data))

	def Test_can_update_bucketlist(self):
		# test that the name of bucket list can be updated
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		rv = self.create_bucket(token)
		self.assertEqual(rv.status_code, 201)

		rv = self.client.post(
			'/bucketlists/',
			headers=dict(Authorization="Bearer " + token),
			data={'name':'Grooving'})
		self.assertEqual(rv.status_code, 201)
		
		rv = self.client.put(
			'/bucketlists/1',
			headers=dict(Authorization="Bearer " + token),
			data={'name':'Sleeping'})
		
		bucket = self.client.get(
			'/bucketlists/1',
			headers=dict(Authorization="Bearer " + token))
		
		self.assertIn('Sleeping',str(bucket.data))

	def Test_can_delete_bucketlist(self):
		# test that bucket list can be deleted
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		rv = self.client.post('/bucketlists/',
			headers=dict(Authorization="Bearer " + token),
			data={'name':'Cook'})
		self.assertEqual(rv.status_code, 201)

		response = self.client.delete(
			'/bucketlists/1', 
			headers=dict(Authorization="Bearer " + token))
		self.assertEqual(response.status_code, 200)

		result = self.client.get(
			'bucketlists/1',
			headers=dict(Authorization="Bearer " + token))
		self.assertEqual(result.status_code, 404)

	def Test_item_is_created(self):
		# test to check item is created
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		self.create_bucket(token)

		rv = self.client.post(
			'/bucketlists/1/items/',
			headers=dict(Authorization="Bearer " + token),
			data=self.item
		)
		self.assertEqual(rv.status_code, 201)

	def Test_item_is_updated(self):
		# test to check item is updated
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		self.create_bucket(token)

		self.client.post(
			'/bucketlists/1/items/',
			headers=dict(Authorization="Bearer " + token),
			data=self.item
		)

		rv = self.client.put(
			'/bucketlists/1/items/1',
			headers=dict(Authorization="Bearer " + token),
			data=self.item1
		)
		self.assertEqual(rv.status_code, 201)


	def Test_item_is_deleted(self):
		# test to check that an item is deleted from bucketlist
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		self.create_bucket(token)

		rv = self.client.post(
			'/bucketlists/1/items/',
			headers=dict(Authorization="Bearer " + token),
			data=self.item
		)
		self.assertEqual(rv.status_code, 201)
		
		self.client.delete(
			'/bucketlists/1/items/1',
			headers=dict(Authorization="Bearer " + token)
		)
		
		response = self.client.delete(
			'/bucketlists/1/items/1',
			headers=dict(Authorization="Bearer " + token))
		self.assertEqual(response.status_code, 404)

	def Test_pagination_when_getting_bucketlists(self):
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		for i in range(1, 12):
			self.create_bucket(token)

		response = self.client.get(
			'/bucketlists/?limit=5',
			headers=dict(Authorization="Bearer " + token)
		)
		print('this is the response', response)
		self.assertEqual(response.status_code, 200)

	'''
	def Test_pagination_when_getting_items(self):
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		
		for i in range(1, 10):
			self.create_item(token)
	'''
	def Test_search_functionality_on_bucketlists(self):
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		self.create_bucket(token)
		response = self.client.get(
			'/bucketlists/?q=Hiking',
			headers=dict(Authorization="Bearer " + token)
		)
		self.assertNotEqual(response.data, None)

	def Test_search_functionality_on_items(self):
		self.register_user()
		response = self.login_user()
		token = json.loads(response.data.decode())['token']
		self.create_bucket(token)
		self.create_item(token)
		response = self.client.get(
			'/bucketlists/1/items/?q=Hiking',
			headers=dict(Authorization="Bearer " + token)
		)
		self.assertNotEqual(response.data, None)	
		
	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()

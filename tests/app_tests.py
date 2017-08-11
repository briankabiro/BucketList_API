import unittest
from app import db
from run import app

class AppTestCase(unittest.TestCase):
	def setUp(self):
		# initial config before tests are run
		self.app = app
		self.client = self.app.test_client()
		self.bucket = {'name':'Hiking'}

		with self.app.app_context():
			db.create_all()

	def Test_bucket_created(self):
		# test to check that bucket list is created
		rv = self.client.post('/bucketlists/', data=self.bucket)
		self.assertEqual(rv.status_code, 201)

	def Test_all_buckets_are_returned(self):
		# test to check that all bucketlists are returned
		rv = self.client.post('/bucketlists/', data=self.bucket)
		self.assertEqual(rv.status_code, 201)
		response = self.client.get('/bucketlists/')
		self.assertEqual(response.status_code, 200)

	def Test_get_bucketlist_by_id(self):
		# test that bucket is returned by appending id to path
		rv = self.client.post('/bucketlists/', data=self.bucket)
		self.assertEqual(rv.status_code, 201)
		result = self.client.get('/bucketlists/1')
		# expect to fail because of str(result.data)
		self.assertIn('Hiking', str(result.data))

	def Test_can_update_bucketlist(self):
		# test that the name of bucket list can be updated
		rv = self.client.post('/bucketlists/', data={'name':'Grooving'})
		self.assertEqual(rv.status_code, 201)
		rv = self.client.put('/bucketlists/1', data={'name':'Sleeping'})
		bucket = self.client.get('/bucketlists/1')
		self.assertIn('Sleeping',str(bucket.data))

	def Test_can_delete_bucketlist(self):
		# test that bucket list can be deleted
		rv = self.client.post('/bucketlists/', data={'name':'Cook'})
		self.assertEqual(rv.status_code, 201)
		response = self.client.delete('/bucketlists/1')
		self.assertEqual(response.status_code, 200)
		result = self.client.get('bucketlists/1')
		self.assertEqual(result.status_code, 404)

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()

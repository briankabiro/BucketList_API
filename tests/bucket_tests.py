from flask import json
from tests import TestBase

class TestBuckets(TestBase):

	def test_bucket_created(self):
		# test to check that bucket list is created
		rv = self.create_bucket(self.token)
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertIn('Hiking', str(data))
		response = self.client.get(
			'/bucketlists/', 
			headers=self.headers)
		buckets = json.loads(response.data)
		self.assertEqual(len(buckets), 1)


	def test_user_buckets_are_returned(self):
		# test to check that all bucketlists are returned
		rv = self.create_bucket(self.token)
		data = json.loads(rv.data)

		response = self.client.get(
			'/bucketlists/', 
			headers=self.headers)
		# self.assertEqual(response.status_code, 200)
		data = json.loads(response.data)
		self.assertEqual(len(data), 1)
		self.assertIn('Hiking', str(data))

	def test_get_bucketlist_by_id(self):
		# test that bucket is returned by appending id to path
		rv = self.create_bucket(self.token)
		self.assertEqual(rv.status_code, 201)
		
		result = self.client.get(
			'/bucketlists/1', 
			headers=self.headers)
		self.assertIn('Hiking', str(result.data))


	def test_can_update_bucketlist(self):
		# test that the name of bucket list can be updated
		rv = self.create_bucket(self.token)
		self.assertEqual(rv.status_code, 201)
		
		rv = self.client.put(
			'/bucketlists/1',
			headers=self.headers,
			data={'name':'Sleeping'})
		
		bucket = self.client.get(
			'/bucketlists/1',
			headers=self.headers)
		
		self.assertIn('Sleeping', str(bucket.data))

	def test_can_delete_bucketlist(self):
		# test that bucket list can be deleted
		self.create_bucket(self.token)

		response = self.client.delete(
			'/bucketlists/1', 
			headers=self.headers)
		self.assertEqual(response.status_code, 200)

		result = self.client.get(
			'bucketlists/1',
			headers=self.headers)
		self.assertEqual(result.status_code, 404)

	
	def test_pagination_when_getting_bucketlists(self):
		for i in range(1, 12):
			self.create_bucket(self.token)

		response = self.client.get(
			'/bucketlists/?limit=5',
			headers=self.headers
		)
		data = json.loads(response.data)
		self.assertEqual(len(data), 5)

	def test_pagination_with_several_pages(self):
		for i in range(1, 6):
			self.create_bucket(self.token)

		response = self.client.get(
			'/bucketlists/?limit=3&page=2',
			headers=self.headers
		)
		data = json.loads(response.data)
		self.assertEqual(len(data), 2)
	
	def test_search_functionality_on_bucketlists(self):
		self.create_bucket(self.token)
		response = self.client.get(
			'/bucketlists/?q=Hiking',
			headers=self.headers
		)
		self.assertIn('Hiking', str(response.data))

	def test_when_limit_is_not_integer(self):
		for i in range(1, 6):
			self.create_bucket(self.token)

		response = self.client.get(
			'/bucketlists/?limit=a',
			headers=self.headers
		)
		self.assertEqual(response.status_code, 400)

	def test_when_page_is_not_integer(self):
		for i in range(1, 6):
			self.create_bucket(self.token)

		response = self.client.get(
			'/bucketlists/?limit=1&page=s',
			headers=self.headers
		)
		self.assertEqual(response.status_code, 400)
		
if __name__ == '__main__':
	unittest.main()

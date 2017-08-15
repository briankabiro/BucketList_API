import unittest
from app import db
from run import app

class ItemTestCase(unittest.TestCase):
	def setUp(self):
		# initial config before tests are run
		self.app = app
		self.client = self.app.test_client()
		self.bucket = {'name':'Over 30'}
		self.item = {'description':'go to zanzibar'}
		self.item1 = {'description':'work on house'}
		self.client.post('/bucketlists/', data=self.bucket)

		with self.app.app_context():
			db.create_all()

	def Test_item_created(self):
		# test to check that bucket list is created
		rv = self.client.post('/bucketlists/1/items', data=self.item)
		self.assertEqual(rv.status_code, 201)

	def Test_can_add_multiple_items(self):
		response = self.client.post('/bucketlists/1/items/', data=self.item1)
		response1 = self.client.post('/bucketlists/1/items/', data=self.item)
		self.assertEqual(response1.status_code, 201)
		self.assertEqual(response.status_code, 201)
		# check the list of items
		
	def Test_can_update_item(self):
		# test that the name of bucket list can be updated
		self.client.post('/bucketlists/1/items', data=self.bucket)
		rv = self.client.put('/bucketlists/1/items/1', data={'name':'Grooving'})
		self.assertEqual(rv.status_code, 201)
		
	def Test_can_delete_item(self):
		# test that bucket list can be deleted
		rv = self.client.post('/bucketlists/1/items/', data={'name':'Cook'})
		self.assertEqual(rv.status_code, 201)
		response = self.client.delete('/bucketlists/1/items/1')
		self.assertEqual(response.status_code, 200)
		result = self.client.get('bucketlists/1/items/1')
		self.assertEqual(result.status_code, 404)

	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()
	
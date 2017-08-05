from app.models import Bucket
import unittest
from app import db, create_app

class BucketTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config_name='testing')


	def Test_bucket_saved_to_db(self):
		# check that a created bucket is saved to db
		bucket = Bucket(name="Hiking")
		result = bucket.save()
		self.assertEqual(result, True)

	def Test_all_buckets_returned(self):
		# test that all buckets in table are returned
		bucket = Bucket(name='21')
		bucket1 = Bucket(name='Before 30')
		buckets = bucket.get_all()
		self.assertIn(buckets, bucket)

	def Test_bucket_deleted_from_db(self):
		# test to check that bucket is deleted from db
		bucket = Bucket(name="30 under 30")
		result = bucket.delete()
		buckets = bucket.get_all()
		self.assertNotIn(buckets, bucket)
	
	def tearDown(self):
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

if __name__ == '__main__':
	unittest.main()
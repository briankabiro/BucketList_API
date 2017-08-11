import unittest
from app import db
from run import app

class AuthTests(unittest.TestCase):
	def setUp(self):
		self.app = app
		self.client = self.app.test_client()
		self.test_user = {'username':'john', 'password':'32331'}
		self.test_user1 = {'username':'john', 'password':'12356'}

		with self.app.app_context():
			db.create_all()

	def Test_register(self):
		# test post request for register endpoint
		response = self.client.post('/auth/register', data=self.test_user)
		self.assertEqual(response.status_code, 201)

	def Test_unique_registration(self):
		rv = self.client.post('/auth/register', data=self.test_user1)
		print("this is rv", rv)
		self.assertEqual(rv, "User already exists")

	def Test_login(self):
		# test post request for login endpoint
		rv = self.client.post('/auth/login', data=self.test_user)
		self.assertEqual(rv.status_code, 200)
		
	def Test_invalid_login(self):
		# test to check if invalid login works
		rv = self.client.post('/auth/login', data=self.test_user1)
		self.assertEqual(rv, "Invalid credentials")

	def Test_reset_password(self):
		# test post request for reset-password endpoint
		rv = self.client.post('/auth/reset-password', data=self.test_user1)
		self.assertEqual(rv, "Password successfully changed")
	
	'''def Test_logout(self):
		# test post request for logout endpoint
		self.client.post('/auth/logout')
	'''
	def tearDown(self):
		# check how to tear down db
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

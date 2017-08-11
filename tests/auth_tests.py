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
		self.client.post('/auth/register', data=self.test_user)
		self.assertEqual(response.status_code, 201)

	def Test_unique_registration(self):
		pass

	def Test_login(self):
		# test post request for login endpoint
		self.client.post('/auth/login', data=self.test_user)
		# self.assertEqual(response_status_code(redirect),)

	def Test_invalid_login(self):
		# test to check if invalid login works
		self.client('/auth/login', data=self.test_user1)

	def Test_logout(self):
		# test post request for logout endpoint
		self.client.post('/auth/logout')

	def Test_reset_password(self):
		# test post request for reset-password endpoint
		self.client.post('/auth/reset-password', data=self.test_user1)

	def tearDown(self):
		# check how to tear down db
		with self.app.app_context():
			db.session.remove()
			db.drop_all()

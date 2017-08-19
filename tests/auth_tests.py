import unittest
from tests import AuthTestBase

class AuthTests(AuthTestBase):
	def Test_register(self):
		# test post request for register endpoint
		response = self.client.post('/auth/register', data=self.test_user)
		self.assertEqual(response.status_code, 201)

	def Test_login(self):
		# test post request for login endpoint
		self.client.post('/auth/register', data=self.test_user)
		rv = self.client.post('/auth/login', data=self.test_user)
		self.assertEqual(rv.status_code, 200)

	def Test_unique_registration(self):
		self.client.post('/auth/register', data=self.test_user)
		rv = self.client.post('/auth/register', data=self.test_user1)
		self.assertEqual(rv.status_code, 303)

	def Test_invalid_username(self):
		self.client.post('/auth/register', data=self.test_user)
		response = self.client.post('/auth/login', data={'username': 'lee', 'password': '23233'})
		self.assertEqual(response.status_code, 401)
		
	def Test_invalid_password(self):
		# test to check if invalid login works
		self.client.post('/auth/register', data=self.test_user)
		rv = self.client.post('/auth/login', data=self.test_user1)
		self.assertEqual(rv.status_code, 403)

	def Test_reset_password(self):
		# test post request for reset-password endpoint
		self.client.post('/auth/register', data=self.test_user)
		rv = self.client.post('/auth/reset-password', data=self.test_user1)
		self.assertEqual(rv.status_code, 201)
	
	'''	
	def Test_logout(self):
		# test post request for logout endpoint
		self.client.post('/auth/logout')
	'''
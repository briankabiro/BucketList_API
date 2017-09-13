import unittest
from tests import AuthTestBase
import json
from app.models import User

class TestAuth(AuthTestBase):
	def test_register(self):
		# test post request for register endpoint
		response = self.client.post('/auth/register', data=self.test_user)
		data = json.loads(response.data)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(self.test_user['username'], data['username'])


	def test_null_values(self):
		rv = self.client.post(
			'/auth/register',
			data={'username':'', 'password':''})
		data = json.loads(rv.data)
		self.assertIn("blank", data['message'])

	def test_login(self):
		# test post request for login endpoint
		self.client.post('/auth/register', data=self.test_user)
		rv = self.client.post('/auth/login', data=self.test_user)
		self.assertEqual(rv.status_code, 200)

	def test_unique_registration(self):
		self.client.post('/auth/register', data=self.test_user)
		rv = self.client.post('/auth/register', data=self.test_user1)
		self.assertEqual(rv.status_code, 400)

	def test_invalid_username(self):
		self.client.post('/auth/register', data=self.test_user)
		response = self.client.post(
			'/auth/login', 
			data={'username': 'lee', 'password': '23233'})
		self.assertEqual(response.status_code, 404)
		
	def test_invalid_password(self):
		# test to check if invalid login works
		self.client.post('/auth/register', data=self.test_user)
		rv = self.client.post('/auth/login', data=self.test_user1)
		self.assertEqual(rv.status_code, 403)

	def test_reset_password(self):
		# test post request for reset-password endpoint
		self.client.post('/auth/register', data=self.test_user)
		rv = self.client.post('/auth/reset-password', data=self.test_user1)
		self.assertEqual(rv.status_code, 200)

	def test_auth_decorator(self):
		# test the auth decorator returns unauthorized
		rv = self.client.get('/bucketlists/')
		self.assertEqual(rv.status_code, 401)
	
	
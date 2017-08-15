from flask_restful import Resource, abort, reqparse
from flask import jsonify
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
import os
import jwt
from functools import wraps
parser = reqparse.RequestParser()

def get_user(username):
	return User.query.filter_by(username=username).first()

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		
		return f(*args, **kwargs)
	return decorated

class Register(Resource):
	def post(self):
		parser.add_argument('username', required=True)
		parser.add_argument('password', required=True)
		args = parser.parse_args()
		username, password = args['username'], generate_password_hash(args['password'])
		
		if get_user(username) != None:
			response = jsonify({"message": "User already exists"})
			response.status_code = 303
			return response
			
		user = User(username=username, password=password)
		user.save()
		
		response = jsonify({
			"message":"Account successfully created"
		})
		response.status_code = 201
		return response

class Login(Resource):
	def post(self):
		parser.add_argument('username')
		parser.add_argument('password')
		args = parser.parse_args()
		username, password = args['username'], args['password']
		user = get_user(username)

		if not user:
			response =  jsonify({"message": "User doesn't exist"})
			response.status_code = 401
			return response

		if check_password_hash(user.password, password):
			#login the person
			token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, os.getenv('SECRET'))
			response = jsonify({"message": "Successfully logged in", "token": token.decode('UTF-8')})
			response.status_code = 200
			return response

		response = jsonify({"message": "Invalid password"})
		response.status_code = 403
		return response
	
			
class ResetPassword(Resource):
	def post(self):
		parser.add_argument('username')
		parser.add_argument('password')
		args = parser.parse_args()	
		user = get_user(args['username'])
		user.password = args['password']
		user.save()
		response = jsonify({"message": "Password successfully changed"})
		response.status_code = 201
		return response


class Logout(Resource):
	
	def post(self):
		user = get_user(args['username'])
		# delete token
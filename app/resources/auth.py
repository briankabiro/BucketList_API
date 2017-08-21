from flask_restful import Resource, abort, reqparse, marshal
from flask import jsonify
from app.models import User
from functools import wraps
from app.serializers.serializers import user_serializer
parser = reqparse.RequestParser()

def get_user(username):
	return User.query.filter_by(username=username).first()

class Register(Resource):
	def post(self):
		parser.add_argument('username', required=True)
		parser.add_argument('password', required=True)
		args = parser.parse_args()
		username, password = args['username'], args['password']
		
		if not username or not password:
			return {"message": "Username or Password cannot be blank"}

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
		return marshal(user, user_serializer), 201

class Login(Resource):
	def post(self):
		"""
		---
		tags:
		  - restful
		parameters:
		  - in: path
		  name: username
		  required: true
		responses:
		  200:
		     description: name of user
		"""
		parser.add_argument('username', required=True)
		parser.add_argument('password', required=True)
		args = parser.parse_args()
		username, password = args['username'], args['password']
		user = get_user(username)

		if not user:
			response =  jsonify({"message": "User doesn't exist"})
			response.status_code = 401
			return response

		if user.authenticate_password(password):
			#login the person
			token = user.generate_token(user.id)
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
		username, password = args['username'], args['password']
		user = get_user(username)

		if password == None:
			return {"message": "Password cannot be blank"}

		if user:
			user.reset_password(password)
			user.save()
			response = jsonify({"message": "Password successfully changed"})
			response.status_code = 201
			return response
		else:
			return {"message": "User doesn't exist"}


class Logout(Resource):
	
	def post(self):
		user = get_user(args['username'])
		# delete token
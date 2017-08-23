from flask_restful import Resource, abort, reqparse, marshal
from flask import jsonify
from app.models import User
from functools import wraps
from app.serializers.serializers import user_serializer
parser = reqparse.RequestParser()
from flasgger import swag_from
from app.swagger_dicts import login_dict, register_dict, reset_dict

def get_user(username):
	return User.query.filter_by(username=username).first()

class Register(Resource):
	@swag_from(register_dict)
	def post(self):
		""" validate request to create a user """
		parser.add_argument('username', required=True)
		parser.add_argument('password', required=True)
		args = parser.parse_args()
		username, password = args['username'], args['password']
		
		if not username or not password or username.isspace() or password.isspace():
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
	@swag_from(login_dict)
	def post(self):
		""" validate request to login """
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
	@swag_from(reset_dict)
	def post(self):
		# reset existing user's password
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
			response.status_code = 200
			return response
		else:
			return {"message": "User doesn't exist"}


class Logout(Resource):
	
	def post(self):
		user = get_user(args['username'])
		# delete token
from flask_restful import Resource, abort, reqparse
from flask import jsonify
from app.models import User
parser = reqparse.RequestParser()

def get_user(username):
	return User.query.filter_by(username=username).first()

class Register(Resource):
	def post(self):
		args = parser.parse_args()
		parser.add_argument('username')
		parser.add_argument('password')
		if get_user(args['username']) != None:
			return jsonify({"message": "User already exists"})
		user = User(username=args['username'], password=args['password'])
		user.save()
		response = jsonify({
			"message":"Account successfully created"
		})
		response.status_code = 201
		return response

class Login(Resource):
	def post(self):
		args = parser.parse_args()
		parser.add_argument('username')
		parser.add_argument('password')
		user = get_user(args['username'])
		if user:
			if args['password'] == user.password:
				#login the person
				response = jsonify({"message": "Successfully logged in"})
				response.status_code = 200
		else:
			return {"message": "Invalid credentials"}

class ResetPassword(Resource):
	def post(self):
		args = parser.parse_args()
		parser.add_argument('username')
		parser.add_argument('password')	
		user = get_user(args['username'])
		user.password = args['password']
		user.save()
		return {"message": "Password successfully changed"}


class Logout(Resource):
	def post(self):
		user = get_user(args['username'])

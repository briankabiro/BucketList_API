from flask_restful import abort
import jwt
from flask import request, current_app, json, make_response
from functools import wraps
from flask import session, jsonify

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		# check if token exists
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			abort(401)

		try:
			auth_token = auth_header.split(" ")[1]
			
		except:
			return make_response(
				jsonify({"message": "Invalid Header format"}), 400)
		
		try:
			user_id_dict = jwt.decode(
				auth_token,
				current_app.config['SECRET_KEY'])
			user_id = user_id_dict['id']
		except jwt.ExpiredSignatureError:
			return make_response(jsonify('Signature Expired. Please log in again'), 400)
		except jwt.InvalidTokenError:
			return make_response(jsonify('Invalid token. please login again'), 400)

		return f(*args, user_id, **kwargs)

	return decorated

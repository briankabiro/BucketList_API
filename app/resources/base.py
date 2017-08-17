from flask_restful import abort
import jwt
from flask import request, current_app, json
from functools import wraps

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		# check if token exists
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			abort(401)		
		auth_token = auth_header.split(" ")[1]

		try:
			user_id_dict = jwt.decode(auth_token, current_app.config['SECRET_KEY'])
			user_id = user_id_dict['id']
		except jwt.ExpiredSignatureError:
			return 'Signature Expired. Please log in again'
		except jwt.InvalidTokenError:
			return 'Invalid token. please login again'

		return f(*args, user_id, **kwargs)
	return decorated

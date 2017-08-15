from flask_restful import abort
import jwt
from flask import request
from run import app

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		# check if token exists
		auth = request.authorization
		if not auth.token:
			abort(401)
		
		try:
			user_id = jwt.decode(auth.token, app.config.get('SECRET_KEY'))
			
		except jwt.ExpiredSignatureError:
			return 'Signature Expired. Please log in again'
		except jwt.InvalidTokenError:
			return 'Invalid token. please login again'

		return f(*args, **kwargs)
	return decorated

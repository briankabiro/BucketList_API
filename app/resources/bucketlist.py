from flask_restful import Resource, abort, reqparse
from app.models import Bucket
parser = reqparse.RequestParser()

def get_bucket(id):
	# Return the bucket from db using id
	return Bucket.query.filter_by(id=id).first()

def abort_if_bucket_doesnt_exist(id):
	if get_bucket(id) == None:
		abort(404, message="Bucket {} doesn't exist".format(id))


class BucketListsApi(Resource):
	def get(self):
		return Bucket.query.all()

	def post(self):
		parser.add_argument('name')
		args = parser.parse_args()
		bucket = Bucket(name=args['name'])
		bucket.save()
		return "Bucket created successfully"

class BucketListApi(Resource):

	# handler for get method
	def get(self, id):
		abort_if_bucket_doesnt_exist(id)
		bucket = get_bucket(id)
		return bucket

	'''
	def put(self, id, data):
		# handler for put method
		abort_if_bucket_doesnt_exist(id)
		bucket = get_bucket(id)
		bucket.name = name
		bucket.save()
		return "successfully updated the bucket"
	'''
	
	def delete(self, id):
		# handler for delete method
		abort_if_bucket_doesnt_exist(id)
		bucket = get_bucket(id)
		bucket.delete()
		return {
			"message":"the bucketlist was deleted successfully"
		}


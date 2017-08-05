from flask_restful import Resource, reqparse

'''def abort_if_bucket_doesnt_exist(bucket_id):
	if bucket_id not in
'''
class BucketListApi(Resource):
	def get(self, id):
		bucket = Bucket.query.filter_by(id=id).first()
		return bucket

	def put(self, id, data):
		bucket = Bucket.query.filter_by(id=id).first()
		# set bucket.name = data

	def delete(self, bucket_id):
		bucket = Bucket.query.filter_by(id=id).first()
		bucket.delete()



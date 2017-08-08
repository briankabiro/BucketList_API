from flask_restful import Resource, abort, reqparse
from flask import jsonify
from app.models import Bucket
parser = reqparse.RequestParser()


def get_bucket(id):
    # Return the bucket from db using id
    return Bucket.query.filter_by(id=id).first()


def abort_if_bucket_doesnt_exist(id):
    if get_bucket(id) == None:
        abort(404, message="Bucket {} doesn't exist".format(id))


class BucketListsApi(Resource):
    #endpoint /bucketlists/
    def get(self):
        buckets = Bucket.query.all()
        results = []
        for bucket in buckets:
            bucket_obj = {
                'id': bucket.id,
                'name': bucket.name,
                'date_created': bucket.date_created,
                'date_modified': bucket.date_modified
            }
            results.append(bucket_obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    def post(self):
        parser.add_argument('name')
        args = parser.parse_args()
        bucket = Bucket(name=args['name'])
        bucket.save()
        # return 201
        response = jsonify({
            'id': bucket.id,
            'name': bucket.name,
            'date_created': bucket.date_created,
            'date_modified': bucket.date_modified
        })
        response.status_code = 201
        return response


class BucketListApi(Resource):
    # endpoint: /bucketlists/<id>
    # handler for get method 
    def get(self, id):
        abort_if_bucket_doesnt_exist(id)
        bucket = get_bucket(id)
        response = jsonify({
            'id': bucket.id,
            'name': bucket.name,
            'date_created': bucket.date_created,
            'date_modified': bucket.date_modified
        })
        response.status_code = 200
        return response

    
    def put(self, id):
        # handler for put method
        parser.add_argument('name')
        args = parser.parse_args()
        abort_if_bucket_doesnt_exist(id)
        bucket = get_bucket(id)
        print('this is args[name]', args['name'])
        bucket.name = args['name']
        bucket.save()
        return "successfully updated the bucket"

    def delete(self, id):
        # handler for delete method
        abort_if_bucket_doesnt_exist(id)
        bucket = get_bucket(id)
        bucket.delete()
        return {"message": "the bucketlist was deleted successfully"}
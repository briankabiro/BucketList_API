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
        # get all bucket lists
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
        # create a bucketlist
        parser.add_argument('name')
        args = parser.parse_args()
        bucket = Bucket(name=args['name'])
        bucket.save()
        # return the created bucketlist
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
    def get(self, id):
        # return bucketlist with id from parameter
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
        # update the name of a bucketlist
        parser.add_argument('name')
        args = parser.parse_args()
        abort_if_bucket_doesnt_exist(id)
        bucket = get_bucket(id)
        bucket.name = args['name']
        bucket.save()
        return "successfully updated the bucket"

    def delete(self, id):
        # delete a bucketlist
        abort_if_bucket_doesnt_exist(id)
        bucket = get_bucket(id)
        bucket.delete()
        return {"message": "the bucketlist was deleted successfully"}
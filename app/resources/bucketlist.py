from flask_restful import Resource, abort, reqparse
from flask import jsonify, request
from app.models import Bucketlist
from app.resources.base import requires_auth
parser = reqparse.RequestParser()


def get_bucket(id, user_id):
    # Return the bucket from db using id
    return Bucketlist.query.filter_by(id=id, owned_by=user_id).first()


def abort_if_bucket_doesnt_exist(id, user_id):
    if get_bucket(id, user_id) == None:
        abort(404, message="Bucketlist {} doesn't exist".format(id))


class BucketListsApi(Resource):
    #endpoint /bucketlists/
    @requires_auth
    def get(self, user_id):
        # get all bucket lists
        query = request.args.get('q')
        limit = request.args.get('limit')
        if query:
            bucket = Bucketlist.query.filter(Bucketlist.name == query).first()
            print("this is bucket", bucket)
            response = jsonify({
                'id': bucket.id,
                'name': bucket.name,
                'date_created': bucket.date_created,
                'date_modified': bucket.date_modified,
                'owned_by': bucket.owned_by
            })
            response.status_code = 200
            return response         
            abort(404, message="Bucketlist with name '{}' doesn't exist".format(query))
        
        if limit:
            limit = int(limit)
            buckets = Bucketlist.get_all(user_id).paginate(page=1, per_page=limit, error_out=False)
            print('this is the pagination object', buckets)
        
        buckets = Bucketlist.get_all(user_id)
        results = []
        for bucket in buckets:
            bucket_obj = {
                'id': bucket.id,
                'name': bucket.name,
                'date_created': bucket.date_created,
                'date_modified': bucket.date_modified,
                'owned_by': bucket.owned_by
            }
            results.append(bucket_obj)
        response = jsonify(results)
        response.status_code = 200
        return response
    
    @requires_auth
    def post(self, user_id):
        # create a bucketlist
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        bucket = Bucketlist(name=args['name'], owned_by=user_id)
        bucket.save()
        # return the created bucketlist
        response = jsonify({
            'id': bucket.id,
            'name': bucket.name,
            'date_created': bucket.date_created,
            'date_modified': bucket.date_modified,
            'owned_by': bucket.owned_by
        })
        response.status_code = 201
        return response


class BucketListApi(Resource):
    # endpoint: /bucketlists/<id>
    @requires_auth
    def get(self, user_id, id):
        # return bucketlist with id from parameter
        abort_if_bucket_doesnt_exist(id, user_id)
        bucket = get_bucket(id, user_id)
        response = jsonify({
            'id': bucket.id,
            'name': bucket.name,
            'date_created': bucket.date_created,
            'date_modified': bucket.date_modified,
            'owned_by': bucket.owned_by
        })
        response.status_code = 200
        return response

    @requires_auth
    def put(self, user_id, id):
        # update the name of a bucketlist
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        abort_if_bucket_doesnt_exist(id, user_id)
        bucket = get_bucket(id, user_id)
        bucket.name = args['name']
        bucket.save()
        return "successfully updated the bucket"

    @requires_auth
    def delete(self, user_id, id):
        # delete a bucketlist
        abort_if_bucket_doesnt_exist(id, user_id)
        bucket = get_bucket(id, user_id)
        bucket.delete()
        return {"message": "the bucketlist was deleted successfully"}
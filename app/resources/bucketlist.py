from flask_restful import Resource, abort, reqparse, marshal
from flask import jsonify, request, json
from app.models import Bucketlist
from app.resources.base import requires_auth
from app.serializers.serializers import bucketlist_item_serializer, bucketlist_serializer
from flasgger import swag_from
from app.swagger_dicts import bucketlists_get_dict, bucketlists_post_dict
from app.swagger_dicts import bucketlist_get_dict, bucketlist_put_dict, bucketlist_delete_dict

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
    @swag_from(bucketlists_get_dict)
    def get(self, user_id):
        """ get all bucket lists """
        query = request.args.get('q')
        limit = request.args.get('limit')
        
        if query:
            bucket = Bucketlist.query.filter(Bucketlist.name == query).first()
            if bucket and bucket.owned_by == user_id:
                return marshal(bucket, bucketlist_serializer), 200
            else:
                abort(404, message="Bucketlist with name '{}' doesn't exist".format(query))
        
        if limit:
            limit = int(limit)
            page = 1
            buckets = Bucketlist.query.filter_by(owned_by=user_id).paginate(page, limit, error_out=False)
            results = []
            for bucket in buckets.items:
                bucket_obj = marshal(bucket, bucketlist_serializer)
                results.append(bucket_obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        
        else:
            buckets = Bucketlist.get_all(user_id)
            results = []
            for bucket in buckets:
                bucket_obj = marshal(bucket, bucketlist_serializer)
                results.append(bucket_obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    
    @requires_auth
    @swag_from(bucketlists_post_dict)
    def post(self, user_id):
        """ create a bucketlist """
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        name = args['name']

        if not name or name.isspace():
            return {"message": "Name of Bucketlist cannot be blank"}
        bucket = Bucketlist(name=name, owned_by=user_id)
        bucket.save()
        # return the created bucketlist
        return marshal(bucket, bucketlist_serializer), 201


class BucketListApi(Resource):
    # endpoint: /bucketlists/<id>
    @requires_auth
    @swag_from(bucketlist_get_dict)
    def get(self, user_id, id):
        """ return bucketlist with id from parameter """
        abort_if_bucket_doesnt_exist(id, user_id)
        bucket = get_bucket(id, user_id)
        return marshal(bucket, bucketlist_serializer), 200

    @requires_auth
    @swag_from(bucketlist_put_dict)
    def put(self, user_id, id):
        """ update the name of a bucketlist """
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        name = args['name']
        abort_if_bucket_doesnt_exist(id, user_id)
        if not name or name.isspace():
            return {"message": "Name of Bucketlist cannot be blank"}
        bucket = get_bucket(id, user_id)
        bucket.name = args['name']
        bucket.save()
        return marshal(bucket, bucketlist_serializer), 200

    @requires_auth
    @swag_from(bucketlist_delete_dict)
    def delete(self, user_id, id):
        """ delete a bucketlist """
        abort_if_bucket_doesnt_exist(id, user_id)
        bucket = get_bucket(id, user_id)
        bucket.delete()
        return make_response(jsonify({"message": "the bucketlist was deleted successfully"}), 200)
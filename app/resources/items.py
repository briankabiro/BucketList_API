from flask_restful import Resource, abort, reqparse, marshal
from flask import jsonify, make_response, request
from app.models import BucketlistItem, Bucketlist
from app.resources.base import requires_auth
parser = reqparse.RequestParser()
from flasgger import swag_from
from app.serializers.serializers import bucketlist_item_serializer
from app.swagger_dicts import item_put_dict, item_delete_dict
from app.swagger_dicts import items_get_dict, items_post_dict

def get_bucket(id, user_id):
    # Return the bucket from db using id
    return Bucketlist.query.filter_by(id=id, owned_by=user_id).first()

def get_item(id, item_id):
    return BucketlistItem.query.filter_by(id=item_id, bucketlist_id=id).first()


class ItemsApi(Resource):
    '''
        endpoint: /bucketlists/<id>items/
    '''
    @requires_auth
    @swag_from(items_get_dict)
    def get(self, user_id, id):
        """ Return items depending on limit and query """
        q = request.args.get('q')
        limit = request.args.get('limit')
        page = request.args.get('page')
        
        if q:
            items = BucketlistItem.query.filter(BucketlistItem.description.contains(q)).all()
            results = []
            if items:
                for item in items:
                    if item.bucketlist_id == int(id):
                        item_obj = marshal(item, bucketlist_item_serializer)
                        results.append(item_obj)
                response = jsonify(results)
                response.status_code = 200
                return response
            else:
                abort(
                    404, message="Item with name '{}' doesn't exist".format(q)
                    )

        if limit:
            try:
                limit = int(limit)
            except:
                return make_response(jsonify({
                    "message": "limit needs to be an integer"}),
                    400)       
            if not page: 
                page = 1
            else:
                try:
                    page = int(page)
                except:
                    return make_response(jsonify(
                        {"message": "page needs to be an integer"}),
                        400)
                    
            items = BucketlistItem.query.filter_by(
                owned_by=user_id, 
                bucketlist_id=id
                ).paginate(page, limit, error_out=False)

            results = []
            for item in items.items:
                item_obj = marshal(item, bucketlist_item_serializer)
                results.append(item_obj)
            response = jsonify(results)
            response.status_code = 200
            return response

        return make_response(
            jsonify({
                "message":
                    "You need to specify the limit or the query parameters"}),
                400)

    @requires_auth
    @swag_from(items_post_dict)
    def post(self, user_id, id):
        """ add items to a bucket """
        parser.add_argument('description', required=True)
        args = parser.parse_args()
        description = args['description']
        if not description or description.isspace():
            return {
                "message": "The description of an item cannot be blank"
            }

        if get_bucket(id, user_id) is None:
            abort(404, message="Bucketlist {} doesn't exist".format(id))
        
        item = BucketlistItem(
            description=args['description'],
            bucketlist_id=id, owned_by=user_id)
        item.save()

        return make_response(jsonify({
            'id': item.id,
            'description': item.description,
            'bucketlist_id': item.bucketlist_id,
            'owned_by': item.owned_by
        }), 201)


class ItemApi(Resource):
    '''
        endpoint: /bucketlists/<id>/items/<item_id>
    '''
    @requires_auth
    @swag_from(item_put_dict)
    def put(self, user_id, id, item_id):
        """ update item in bucketlist """
        parser.add_argument('description')
        parser.add_argument('done')
        args = parser.parse_args()
        description, done = args['description'], args['done']
        
        if get_bucket(id, user_id) is None:
            abort(404, message="Bucketlist {} doesn't exist".format(id))

        item = get_item(id, item_id)
        if not item:
            abort(404, message="Item {} doesn't exist".format(item_id))
        
        if description and not description.isspace():
            item.description = description
            item.save()
        
        elif done and not done.isspace():
            
            if done == "true":
                item.done = True
            elif done == "false":
                item.done == False
            else:
                return make_response(
                    jsonify(
                        {"message": "Done should be passed as a boolean value (true or false)"}
                        ), 400
                    )
            item.save()

        else:
            return make_response(jsonify
                ({"message": 
                    "You need to specify the description or done in the request"}),
                400)
        
        return make_response(jsonify({"message": "Item updated successfully"}), 200)

    @requires_auth
    @swag_from(item_delete_dict)
    def delete(self, user_id, id, item_id):
        """ delete item from bucketlist """
        if get_bucket(id, user_id) == None:
            abort(404, message="Bucketlist {} doesn't exist".format(id))

        item = get_item(id, item_id)
        if not item:
            abort(404, message="Item {} doesn't exist".format(item_id))

        item.delete()
        return make_response(jsonify({"message": "Item was deleted"}), 200)
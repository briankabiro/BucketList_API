from flask_restful import Resource, abort, reqparse
from flask import jsonify, make_response, request
from app.models import BucketlistItem
from app.resources.base import requires_auth
parser = reqparse.RequestParser()


def get_item(id, item_id):
    return BucketlistItem.query.filter_by(id=item_id, bucketlist_id=id).first()


class ItemsApi(Resource):
    '''
        endpoint: /bucketlists/<id>items/
    '''
    @requires_auth
    def get(self, user_id, id):
        query = request.args.get('q')
        limit = request.args.get('limit')
        if query:
            item = BucketlistItem.query.filter(BucketlistItem.description == query).first()
            if item:
                response = jsonify({
                    'id': item.id,
                    'description': item.description,
                    'date_created': item.date_created,
                    'date_modified': item.date_modified,
                    'owned_by': item.owned_by,
                    'bucketlist_id': item.bucketlist_id
                })
                response.status_code = 200
                return response         
            else:
                abort(404, message="Item with name '{}' doesn't exist".format(query))

        if limit:
            limit = int(limit)
            page = 1
            items = BucketlistItem.query.filter_by(
                owned_by=user_id, 
                bucketlist_id=id
                ).paginate(page, limit, error_out=False)

            print('this is the pagination object', dir(items))
            print(items.items)
            results = []
            for item in items.items:
                item_obj = {
                    'id': item.id,
                    'description': item.description,
                    'date_created': item.date_created,
                    'date_modified': item.date_modified,
                    'owned_by': item.owned_by,
                    'bucketlist_id': item.bucketlist_id
                }
                results.append(item_obj)
            response = jsonify(results)
            response.status_code = 200
            return response      
        
    @requires_auth
    def post(self, user_id, id):
        # add items to a bucket
        parser.add_argument('description', required=True)
        args = parser.parse_args()
        item = BucketlistItem(description=args['description'], bucketlist_id=id, owned_by=user_id)
        item.save()

        return make_response(jsonify({
            'id': item.id,
            'description': item.description,
            'date_created': item.date_created,
            'date_modified': item.date_modified,
            'bucketlist_id': item.bucketlist_id,
            'owned_by': item.owned_by
        }), 201)


class ItemApi(Resource):
    '''
        endpoint: /bucketlists/<id>/items/<item_id>
    '''
    @requires_auth
    def put(self, user_id, id, item_id):
        # update item in bucketlist
        parser.add_argument('description', required=True)
        args = parser.parse_args()
        item = get_item(id, item_id)
        if not item:
            abort(404, message="Item {} doesn't exist".format(item_id))

        item.description = args['description']
        item.save()
        return make_response(jsonify({"message": "Item updated successfully"}), 201)

    @requires_auth
    def delete(self, user_id, id, item_id):
        # delete item from bucketlist
        item = get_item(id, item_id)
        if not item:
            abort(404, message="Item {} doesn't exist".format(item_id))

        item.delete()
        return make_response(jsonify({"message": "Item was deleted"}), 200)
        # add deleted status code
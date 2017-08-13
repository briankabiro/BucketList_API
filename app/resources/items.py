from flask_restful import Resource, abort, reqparse
from flask import jsonify
from app.models import BucketItem
parser = reqparse.RequestParser()


def get_item(id, item_id):
    return BucketItem.query.filter(id=item_id, bucketlist_id=id).first()


class ItemsApi(Resource):
    '''
        endpoint: /bucketlists/<id>items/
    '''

    def post(self, id):
        # add items to a bucket
        parser.add_argument('description')

        args = parser.parse_args()
        item = BucketItem(description=args['description'], bucketlist_id=id)
        item.save()

        return jsonify({
            'id': item.id,
            'description': item.name,
            'date_created': item.date_created,
            'date_modified': item.date_modified,
            'bucketlist_id': item.bucketlist_id
        }), 201


class ItemApi(Resource):
    '''
        endpoint: /bucketlists/<id>/items/<item_id>
    '''

    def put(self, id, item_id):
        # update item in bucketlist
        parser.add_argument('description')
        args = parser.parse_args()
        item = get_item(id, item_id)
        if not item:
            abort(404, message="Item {} doesn't exist".format(item_id))

        item.description = args['description']
        item.save()
        return jsonify({"message": "Item updated successfully"}), 201

    def delete(self, id, item_id):
        # delete item from bucketlist
        item = get_item(id, item_id)
        if not item:
            abort(404, message="Item {} doesn't exist".format(item_id))

        item.delete()
        return jsonify({"message": "Item was deleted"}), 200
        # add deleted status code
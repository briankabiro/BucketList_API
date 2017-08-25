from flask_restful import fields

bucketlist_item_serializer = {
	'id': fields.Integer,
	'description': fields.String,
	'is_done': fields.Boolean,
	'owned_by': fields.Integer,
	'bucketlist_id': fields.Integer
}

bucketlist_serializer = {
	'name': fields.String,
	'id': fields.Integer,
	'owned_by': fields.Integer,
	'items': fields.Nested(bucketlist_item_serializer)
}

user_serializer = {
	'username': fields.String
}
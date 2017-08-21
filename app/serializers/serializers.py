from flask_restful import fields

bucketlist_item_serializer = {
	'id': fields.Integer,
	'description': fields.String,
	'is_done': fields.Boolean,
	'date_created': fields.DateTime,
	'date_modified': fields.DateTime,
	'owned_by': fields.Integer,
	'bucketlist_id': fields.Integer
}

bucketlist_serializer = {
	'name': fields.String,
	'id': fields.Integer,
	'date_created': fields.DateTime,
	'date_modified': fields.DateTime,
	'owned_by': fields.Integer,
	'items': fields.Nested(bucketlist_item_serializer)
}

user_serializer = {
	'username': fields.String
}
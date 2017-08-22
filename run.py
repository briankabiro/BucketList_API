from app import create_app
from app.resources.items import ItemApi, ItemsApi
from app.resources.bucketlist import BucketListApi, BucketListsApi
from app.resources.auth import Register, Login, ResetPassword, Logout
from flask_restful import Api

app = create_app(config_name='development')
api = Api(app)
api.add_resource(BucketListApi, '/bucketlists/<id>')
api.add_resource(BucketListsApi, '/bucketlists/')
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(ResetPassword, '/auth/reset-password')
api.add_resource(ItemsApi, '/bucketlists/<id>/items/')
api.add_resource(ItemApi, '/bucketlists/<id>/items/<item_id>')


if __name__ == '__main__':
	app.run()
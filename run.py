from app import create_app
from flask_restful import Api
from app.resources.bucketlist import BucketListApi, BucketListsApi
from app.resources.auth import Register, Login, ResetPassword, Logout

app = create_app(config_name='development')
api = Api(app)
api.add_resource(BucketListApi, '/bucketlists/<id>')
api.add_resource(BucketListsApi, '/bucketlists/')
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(ResetPassword, '/auth/reset_password')

if __name__ == '__main__':
	app.run()
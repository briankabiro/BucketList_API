from app import create_app
from app.resources.items import ItemApi, ItemsApi
from app.resources.bucketlist import BucketListApi, BucketListsApi
from app.resources.auth import Register, Login, ResetPassword, Logout
from flask_restful import Api
from flasgger import Swagger
import os

app = create_app(config_name='development')
api = Api(app)
app.config['SWAGGER'] = {
	'title': 'Bucketlist API'
}
Swagger(app)

api.add_resource(BucketListApi, '/bucketlists/<id>')
api.add_resource(BucketListsApi, '/bucketlists/')
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(ResetPassword, '/auth/reset-password')
api.add_resource(ItemsApi, '/bucketlists/<id>/items/')
api.add_resource(ItemApi, '/bucketlists/<id>/items/<item_id>')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
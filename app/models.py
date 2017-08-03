class User(db.Model):
	"""
		Class for a User
		Attributes:
			id: id of a user
			username: name of the user
			password: the password of the user
	"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	password = 	db.Column(db.String)

	def __repr__(self):
		# return the name of the User
		return '<User %s>' % self.username

class Bucket(Model):
	""" 
		Class for a creating a bucket object
		Attributes:
			id: unique id of the bucket
			name: name of the bucket
			items: the items that the bucket contains
	"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	items = db.Column()
	def __repr__(self):
		# return the name of the bucket
		return "Bucket %s>" % self.name

class BucketItem(Model):
	"""
		Class for creating an item object
		Attributes:
			id: unique id for identifying each item
			description: the text/description of an item
	"""
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.Text)

	def __repr__(self):
		# return the description of an item
		return "BucketItem %s>" % self.description
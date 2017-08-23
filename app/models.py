import os
import jwt
import datetime
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """
        Class for a User
        Attributes:
            id: id of a user
            username: name of the user
            password: the password of the user
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String())
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    bucketlists = db.relationship('Bucketlist', order_by='Bucketlist.id')
    
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
    
    def authenticate_password(self, password):
        # check if passwords match
        return check_password_hash(self.password, password)

    def generate_token(self, id):
        # generate token on authentication
        return jwt.encode({'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, os.getenv('SECRET_KEY'))

    def reset_password(self, new_password):
        # reset password
        self.password = generate_password_hash(new_password)
    
    def save(self):
        # save a user to the db
        db.session.add(self)
        db.session.commit()

    def get_all(self):
        # return all the users in table
        return User.query.all()

    def __repr__(self):
        # return the name of the User
        return '<User %s>' % self.username


class Bucketlist(db.Model):
    """
        Class for creating a bucket object
        Attributes:
                id: unique id of the bucket
                name: name of the bucket
                items: the items that the bucket contains
        """
    __tablename__ = "bucketlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    owned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship("BucketlistItem", backref=db.backref("bucketlists"))
    
    def save(self):
        # save a bucket to the table
        db.session.add(self)
        db.session.commit()

    def get_all(user_id):
        # return all the buckets that belong to a given user
        return Bucketlist.query.filter_by(owned_by=user_id)

    def delete(self):
        # delete a bucket from the table
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        # return the name of the bucket
        return "<Bucketlist %s>" % self.name


class BucketlistItem(db.Model):
    """
        Class for creating an item object
        Attributes:
            id: unique id for identifying each item
            description: the text/description of an item
    """

    __tablename__ = "bucketlist_items"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    is_done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    owned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def save(self):
        # save an item to the table
        db.session.add(self)
        db.session.commit()

    def get_all(user_id, bucketlist_id):
        # return all the items that belong to user's bucketlist
        return BucketlistItem.query.all(owned_by=user_id, bucketlist_id=bucketlist_id)

    def delete(self):
        # delete an item from the table
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        # return the description of an item
        return "<BucketlistItem %s>" % self.description
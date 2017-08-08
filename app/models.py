from app import db


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
    password = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        # return the name of the User
        return '<User %s>' % self.username


class Bucket(db.Model):
    """
                Class for a creating a bucket object
                Attributes:
                        id: unique id of the bucket
                        name: name of the bucket
                        items: the items that the bucket contains
        """
    __tablename__ = "buckets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def save(self):
        # save a bucket to the table
        db.session.add(self)
        db.session.commit()

    def get_all(self):
        # return all the buckets in table
        return Bucket.query.all()

    def delete(self):
        # delete a bucket from the table
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        # return the name of the bucket
        return "<Bucket %s>" % self.name


class BucketItem(db.Model):
    """
                Class for creating an item object
                Attributes:
                        id: unique id for identifying each item
                        description: the text/description of an item
        """

    __tablename__ = "bucket_items"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def save(self):
        # save an item to the table
        db.session.add(self)
        db.session.commit()

    def get_all():
        # return all the items in the table
        return BucketItem.query.all()

    def delete(self):
        # delete an item from the table
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        # return the description of an item
        return "<BucketItem %s>" % self.description
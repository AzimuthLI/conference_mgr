from app.db import db

class Conferences(db.Model):
    """This class represents the conference table."""

    __tablename__ = 'conferences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_start = db.Column(db.DateTime, default=db.func.current_timestamp())
    signup_until = db.Column(db.DateTime)
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Conferences.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Conferences: {}>".format(self.name)

class User_admin(db.Model):
    """ This class represents the user-admin table """

    __tablename__ = 'user_admin'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255), unique = True)

    def __init__(self, username, password):
        """initialize with name"""
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User_admin.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User_admin: {}>".format(self.username)

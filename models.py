from datetime import datetime

from flask_security import UserMixin, RoleMixin

from app import db

# Modelos para Usuario y Rol
# https://pythonhosted.org/Flask-Security/quickstart.html#mongoengine-application
# http://docs.mongoengine.org/


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    def __str__(self):
        return self.name


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def __str__(self):
        return self.email


class Category(db.Document):
    name = db.StringField(max_length=50, required=True)

    def __str__(self):
        return '<Category %r>' % self.name


class Post(db.Document):
    title = db.StringField(max_length=80, required=True)
    body = db.StringField()
    pub_date = db.DateTimeField(default=datetime.utcnow)
    category = db.ReferenceField(Category)

    def __str__(self):
        return '<Post %r>' % self.title

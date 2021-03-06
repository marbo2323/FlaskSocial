import datetime

from flask_bcrypt import generate_password_hash
from flask_login.mixins import UserMixin
from peewee import *

DATABASE = SqliteDatabase('social.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(
            Post.user == self
        )

    @classmethod
    def create_user(cls, username, email, password, is_admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_admin=is_admin)
        except IntegrityError:
            raise ValueError("User already exists")

    @classmethod
    def user_exists(cls, username):
        return cls.select().where(User.username == username).exists()


class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User,
        related_name='posts'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()

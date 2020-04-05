from flask import Flask, g
from flask_login import LoginManager
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = "23wer234.ewfewq4554tr.32534rfew!f34e4543"

login_namager = LoginManager()
login_namager.init_app(app)
login_namager.login_view = 'login'


@login_namager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


if __name__ == '__main__':
    models.initialize()
    models.User.create(
        username="admin",
        email="admin@snw.com",
        password="admin.123",
        is_admin=True
    )
    app.run(debug=DEBUG, host=HOST, port=PORT)

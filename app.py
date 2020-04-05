from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_login import LoginManager

import forms
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


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/')
def index():
    return 'Hey!'


if __name__ == '__main__':
    models.initialize()
    # try:
        # models.User.create(
        #     username="admin",
        #     email="admin@snw.com",
        #     password="admin.123",
        #     is_admin=True
        # )
    # except ValueError:
    #     pass
    app.run(debug=DEBUG, host=HOST, port=PORT)

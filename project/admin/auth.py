import pdb

from flask.ext.login import LoginManager
from flask.ext.login import login_user
from forms import LoginForm, RegistrationForm
from flask import render_template, request, escape, redirect, url_for

from project import app
from models import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("admin/login.html", form=form)

@app.route("/register", methods=('POST', 'GET',))
def register():
    form = RegistrationForm(request.form or None)
    if request.method == 'GET':
        return render_template('admin/register.html', form=form)
    else:
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            user.save()
            return redirect(url_for('login'))






# -*- coding: utf-8 -*-
import pdb

from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm
from flask import render_template, request, escape, redirect, url_for, flash

from project import app
from models import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(userid):
    return User.get(id=userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form or None)
    if form.validate_on_submit():
        user = User.get(login = form.login.raw_data)
        login_user(user)
        flash(u"Успішний вхід. Привіт %s" % user.login)
        return redirect(url_for("admin.index"))
    return render_template("admin/login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

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






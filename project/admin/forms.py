# -*- coding: utf-8 -*-
import pdb

from flask.ext import login, wtf
from flask.ext.wtf import Form, IntegerField, BooleanField, validators
from models import User

from project import bcrypt

class ImageSettingsForm(Form):
	allow_image_resize = BooleanField(u'Allow Image Resizing', [validators.required()])
	image_size_width = IntegerField(u'Image Width', [validators.required()])
	image_size_height = IntegerField(u'Image Height', [validators.required()])
	thumb_size_width = IntegerField(u'Thumbnail Width', [validators.required()])
	thumb_size_height = IntegerField(u'Thumbnail Height', [validators.required()])

class LoginForm(wtf.Form):
    login = wtf.TextField(
        label=u"Ім&#96;я",
        validators=[wtf.required()]
    )

    password = wtf.PasswordField(
        label=u"Пароль",
        validators=[wtf.required()]
    )

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise wtf.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise wtf.ValidationError('Invalid password')

    def get_user(self):
    	user_set = [u for u in User.select().where(nickname__eq=self.login)][0]
        return user_set

class RegistrationForm(wtf.Form):
    login = wtf.TextField(validators=[wtf.required()])
    email = wtf.TextField(validators=[wtf.required(), wtf.validators.Email()])
    password = wtf.PasswordField(validators=[wtf.required()])

    def validate_login(self, field):
        current_ident_hash = bcrypt.generate_password_hash(self.login.raw_data)
        if User.filter(ident_hash=current_ident_hash).count():
            raise wtf.ValidationError(u'Користувач з ніком %s вже зареєстрований. Оберіть інше ім&#96;я')

class NewAlbumForm(wtf.Form):
    title = wtf.TextField(validators=[wtf.required()])
    description = wtf.TextAreaField()

class MetaDataForm(wtf.Form):
    meta_d = wtf.TextAreaField(
        label=u'"Пошуковий" опис',
        description=u"Пошукові системи відображають цю інформацію при виводі результатів пошуку",
        validators=[wtf.required()]
    )
    meta_k = wtf.TextAreaField(
        label=u"Ключові слова",
        description=u"Перелік ключових слів, які будуть застосовуватися на кожній сторінці сайту",
        validators=[wtf.required()]
    )


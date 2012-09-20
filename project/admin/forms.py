from flask.ext import login, wtf
from flask.ext.wtf import Form, IntegerField, BooleanField, validators
from models import User

class ImageSettingsForm(Form):
	allow_image_resize = BooleanField(u'Allow Image Resizing', [validators.required()])
	image_size_width = IntegerField(u'Image Width', [validators.required()])
	image_size_height = IntegerField(u'Image Height', [validators.required()])
	thumb_size_width = IntegerField(u'Thumbnail Width', [validators.required()])
	thumb_size_height = IntegerField(u'Thumbnail Height', [validators.required()])

class LoginForm(wtf.Form):
    login = wtf.TextField(validators=[wtf.required()])
    password = wtf.PasswordField(validators=[wtf.required()])

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
    email = wtf.TextField()
    password = wtf.PasswordField(validators=[wtf.required()])

    def validate_login(self, field):
        if len([u for u in User.select().where(nickname__eq=self.login)]) > 0:
            raise wtf.ValidationError('Duplicate username')

class NewAlbumForm(wtf.Form):
    title = wtf.TextField(validators=[wtf.required()])
    description = wtf.TextAreaField()


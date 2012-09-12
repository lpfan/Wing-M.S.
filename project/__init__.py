import os

from flask import Flask
from flask.ext.admin import Admin
from admin.models import Article, Category, User
from admin.settings import SettingsView
from admin.utils import My_ModelView, UsersView

def rel(*x):
	return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

app = Flask(__name__)
UPLOAD_FOLDER = rel('uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SETTINGS_PATH = rel('settings.cfg')

from admin.file_upload import *

admin = Admin(app)

admin.add_view(My_ModelView(
	Article,
	name="Articles",
    category='Content')
)
admin.add_view(My_ModelView(
	Category,
	name="Categories",
    category='Content')
)
admin.add_view(UsersView(
	User,
	name="Users",
    category='Administration')
)

admin.add_view(SettingsView(
	name="Settings",
	category='Administration')
)

app.debug = True
SECRET_KEY = 'misha1987'

app.config.from_object(__name__)

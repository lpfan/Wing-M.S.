import os, pdb

from flask import Flask
from flask.ext.admin.base import Admin
from flask.ext.admin import expose
from admin.models import Article, Category, User
from admin.settings import SettingsView
from admin.gallery import GalleryView
from admin.utils import My_ModelView, UsersView
from flask.ext.admin.contrib import fileadmin
from admin.index import GeneralView

def rel(*x):
	return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(rel('static'), 'uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SETTINGS_PATH = rel('settings.cfg')

admin = Admin(index_view=GeneralView())

admin.init_app(app)

from admin.file_upload import *
from frontend.controllers import index

admin.add_view(My_ModelView(
	Article,
	name="Articles"
	)
)
admin.add_view(My_ModelView(
	Category,
	name="Categories",
	endpoint='category_mgm')
)
admin.add_view(UsersView(
	User,
	name="Users")
)

admin.add_view(SettingsView(
	name="Settings")
)

admin.add_view(GalleryView(
	name = 'Gallery'
	)
)

admin.add_view(fileadmin.FileAdmin(
	UPLOAD_FOLDER, '/uploads/', name='File Manager')
)

app.debug = True
SECRET_KEY = 'misha1987'

app.config.from_object(__name__)

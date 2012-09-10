import os

from flask import Flask
from flask.ext.admin import Admin
from admin.models import Article, Category
from admin.utils import My_ModelView

def rel(*x):
	return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

app = Flask(__name__)
UPLOAD_FOLDER = rel('uploads')
from admin.file_upload import *

admin = Admin(app)
admin.add_view(My_ModelView(
	Article,
	name="Articles")
)
admin.add_view(My_ModelView(
	Category,
	name="Categories")
)

app.debug = True
SECRET_KEY = 'misha1987'

app.config.from_object(__name__)

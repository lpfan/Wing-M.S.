# -*- coding: utf-8 -*-

import os, pdb

from flask import Flask
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

from flask.ext.admin.base import Admin
from flask.ext.admin import expose
from admin.models import Article, Category, User, GeneralMeta, Menu
from admin.gallery import GalleryView
from flask.ext.admin.contrib import fileadmin
from flask.ext.assets import Environment, Bundle
from admin.utils import My_ModelView, UsersView
from admin.index import GeneralView
from admin.settings import SettingsView
from admin.auth import *

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

login_manager.setup_app(app)

UPLOAD_FOLDER = os.path.join(rel('static'), 'uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SETTINGS_PATH = rel('settings.cfg')

admin = Admin(index_view=GeneralView())

admin.init_app(app)

from admin.file_upload import *
from frontend.controllers import index


@app.context_processor
def teardown_request(exception=None):
    general_meta_k = ''
    general_meta_d = ''
    menu = Menu.select()
    try:
        general_meta_k = GeneralMeta.get(id=1).meta_k
        general_meta_d = GeneralMeta.get(id=1).meta_d
    except GeneralMeta.DoesNotExist, e:
        print "Meta is empty, %s" % e
    return dict(general_meta_d = general_meta_d, general_meta_k=general_meta_k, menu=menu)

admin.add_view(My_ModelView(
    Article,
    name=u"Сторінки"
    )
)
admin.add_view(My_ModelView(
    Category,
    name=u"Розділи",
    endpoint='category_mgm')
)
admin.add_view(UsersView(
    User,
    name=u"Користувачі")
)

admin.add_view(SettingsView(
    name=u"Налаштування")
)

admin.add_view(GalleryView(
    name = u'Галерея'
    )
)

admin.add_view(fileadmin.FileAdmin(
    UPLOAD_FOLDER, '/uploads/', name='File Manager')
)

app.debug = True
SECRET_KEY = 'misha1987'

# Flask Assets 
assets = Environment(app)
js = Bundle(
    'js/jquery-1.8.1.min.js',
    'js/jquery.form.js',
    'js/jquery.lightbox-0.5.min.js',
    'js/admin/jquery.cookie.js',
    'js/admin/tmpl.min.js',
    'js/admin/load-image.min.js',
    'js/admin/bootstrap.min.js',
    'js/admin/bootstrap-image-gallery.min.js',
    'js/admin/jquery-ui.custom.min.js',
    'js/admin/jquery.dynatree.min.js',
    output='gen/admin_pack.js'
    )
js_public = Bundle(
    'js/jquery-1.8.1.min.js',
    'js/jquery.lightbox-0.5.min.js',
    'js/jquery.form.js',
    'js/imagepreloader.js',
    'js/jquery.nivo.slider.pack.js',
    output='gen/public_pack.js'
    )

assets.register('js_all', js)
assets.register('js_public', js_public)

app.config.from_object(__name__)
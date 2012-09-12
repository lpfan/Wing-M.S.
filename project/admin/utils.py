import pdb

import project

from flask.ext.admin.contrib.peeweemodel import ModelView
import ConfigParser

class My_ModelView(ModelView):
    edit_template = 'admin/custom_edit.html'
    create_template = 'admin/custom_create.html'

class UsersView(ModelView):
    excluded_list_columns = ('password')

class ConfigManager():

	def __init__(self):
		self.settings = project.SETTINGS_PATH
		self.config = ConfigParser.RawConfigParser()
		self.config.read(self.settings)

	def get_config(self):
		return self.config

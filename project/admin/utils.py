import pdb, project, ConfigParser

from flask.ext.admin.contrib.peeweemodel import ModelView
from flask.ext.wtf import SelectField


class My_ModelView(ModelView):
    edit_template = 'admin/custom_edit.html'
    create_template = 'admin/custom_create.html'
    excluded_list_columns = ('text')

class UsersView(ModelView):
    excluded_list_columns = ('password')
    form_overrides = dict(group=SelectField)
    form_args = dict(
    		group = dict(
            	choices=[(0, 'admin'), (1, 'editor')]
        	)
        )

class ConfigManager():

	def __init__(self):
		self.settings = project.SETTINGS_PATH
		self.config = ConfigParser.RawConfigParser()
		self.config.read(self.settings)

	def get_config(self):
		return self.config

	def get_section_configs(self, aConfigSection):
		raw_config = self.config.items(aConfigSection) 
		return dict(raw_config)

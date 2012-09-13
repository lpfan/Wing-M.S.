import pdb, project, os

from flask.ext.admin import Admin, BaseView, expose
from utils import ConfigManager
from forms import ImageSettingsForm
from flask import request, flash, redirect, url_for
from werkzeug.datastructures import MultiDict



class SettingsView(BaseView):
	@expose('/', methods=("GET", "POST"))
	def index(self):
		config = ConfigManager()
		settings_dict={}
		if config.get_section_configs('ImageSettings')['allow_image_resizing'].lower() == 'true':
			settings_dict['allow_image_resize'] = bool(True)
		else:
			settings_dict['allow_image_resize'] = bool(False)
		settings_dict['image_size_width'] = config.get_section_configs('PictureSize')['width']
		settings_dict['image_size_height'] = config.get_section_configs('PictureSize')['height']
		settings_dict['thumb_size_width'] = config.get_section_configs('ThumbnailSize')['width']
		settings_dict['thumb_size_height'] = config.get_section_configs('ThumbnailSize')['height']
		image_form_setting = ImageSettingsForm(formdata=MultiDict(mapping=settings_dict))
		if request.method == 'POST':
			form = ImageSettingsForm(request.form)
			if form.validate():
				config.get_config().set('ImageSettings', 'allow_image_resizing', form.allow_image_resize._value())
				config.get_config().set('PictureSize', 'width', form.image_size_width._value())
				config.get_config().set('PictureSize', 'height', form.image_size_height._value())
				config.get_config().set('ThumbnailSize', 'width', form.thumb_size_width._value())
				config.get_config().set('ThumbnailSize', 'height', form.thumb_size_height._value())
				with open(project.SETTINGS_PATH, 'wb') as configfile:
					config.get_config().write(configfile)
				flash('Data has been written succesfuly')
				return redirect(url_for('.index'))
		return self.render(
			'admin/settings.html',
			image_form_setting = image_form_setting
		)
import pdb

from flask.ext.admin import Admin, BaseView, expose
from utils import ConfigManager
from forms import ImageSettingsForm


class SettingsView(BaseView):
	@expose('/')
	def index(self):
		config = ConfigManager().get_config()
		image_form_setting = ImageSettingsForm()
		#pdb.set_trace()
		return self.render(
			'admin/settings.html',
			image_form_setting = image_form_setting
		)
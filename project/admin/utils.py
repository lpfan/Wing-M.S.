from flask.ext.admin.contrib.peeweemodel import ModelView

class My_ModelView(ModelView):
	edit_template = 'admin/custom_edit.html'
	create_template = 'admin/custom_create.html'


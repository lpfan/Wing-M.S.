from flask.ext.wtf import Form, TextField, BooleanField

class ImageSettingsForm(Form):
	allow_image_resize = BooleanField(label='Allow Image Resizing', description='')
	image_size_width = TextField()
	image_size_height = TextField()
	thumb_size_width = TextField()
	thumb_size_height = TextField()
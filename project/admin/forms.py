from flask.ext.wtf import Form, IntegerField, BooleanField, validators

class ImageSettingsForm(Form):
	allow_image_resize = BooleanField(u'Allow Image Resizing', [validators.required()])
	image_size_width = IntegerField(u'Image Width', [validators.required()])
	image_size_height = IntegerField(u'Image Height', [validators.required()])
	thumb_size_width = IntegerField(u'Thumbnail Width', [validators.required()])
	thumb_size_height = IntegerField(u'Thumbnail Height', [validators.required()])
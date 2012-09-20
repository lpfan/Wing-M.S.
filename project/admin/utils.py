import pdb, project, ConfigParser, os, Image

from flask.ext.admin.contrib.peeweemodel import ModelView
from flask.ext.wtf import SelectField
from project.config import UPLOAD_FOLDER
from werkzeug import secure_filename


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


class GalleryManager():

    def __init__(self):
        self.upload_folder = UPLOAD_FOLDER 
        self.pict_folder = os.path.join(UPLOAD_FOLDER, 'pict')
        self.thumb_folder = os.path.join(UPLOAD_FOLDER, 'thumb')

    def create_album(self, aAlbum_title):
        pass

    def add_photo(self, album, raw_file):
        pass

    #save all uploaded images in png 
    def save_as_png(self, img_obj, pict_path='', thumb_path=''):
        img = Image.open(img_obj)
        image_width = int(ConfigManager().get_section_configs('PictureSize')['width'])
        image_height = int(ConfigManager().get_section_configs('PictureSize')['height'])
        if img.size[0] > image_width:
            img = img.resize((image_width, image_height), Image.ANTIALIAS)
        img_filename = secure_filename(os.path.splitext(img_obj.filename)[0]) + '.png'
        img.save(os.path.join(pict_path or self.pict_folder, img_filename))
        img = Image.open(os.path.join(pict_path or self.pict_folder, img_filename))
        self.create_thumbnail(pil_image = img, png_pict_filename = img_filename, thumb_path = thumb_path)
        return img

    def create_thumbnail(self, pil_image = '', png_pict_filename = '', thumb_path=''):
        thumb_width = int(ConfigManager().get_section_configs('ThumbnailSize')['width'])
        thumb_height = int(ConfigManager().get_section_configs('ThumbnailSize')['height'])
        pil_img = pil_image.resize((thumb_width, thumb_height), Image.ANTIALIAS)
        pil_img.save(os.path.join(thumb_path or self.thumb_folder, png_pict_filename))


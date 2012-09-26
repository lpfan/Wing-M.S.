import pdb, project, ConfigParser, os, Image

from flask.ext.admin.contrib.peeweemodel import ModelView
from flask.ext.wtf import SelectField
from project.config import UPLOAD_FOLDER
from werkzeug import secure_filename
from hurry.filesize import size, si
from pytils.translit import slugify


class My_ModelView(ModelView):
    edit_template = 'admin/custom_edit.html'
    create_template = 'admin/custom_create.html'
    excluded_list_columns = ('text')
    excluded_form_columns = ('slug',)

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
        album_path = os.path.join(self.pict_folder, aAlbum_title)
        if not os.path.exists(album_path):
            os.makedirs(album_path)
        thumb_path = os.path.join(self.thumb_folder, aAlbum_title)
        if not os.path.exists(thumb_path):
            os.makedirs(thumb_path)
        return (album_path, thumb_path,)
    
    def add_photo(self, album, raw_file):
        pict_path = album.album_path
        pict_thumb = album.thumb_path
        pict_url = self.create_url(pict_path)
        thumb_url = self.create_url(pict_thumb)
        img = self.save_as_png(raw_file, pict_path=pict_path, thumb_path=pict_thumb)
        pict_file_name = self.get_filename(img)
        size = self.return_size(img)
        return (
            pict_file_name,
            size,
            os.path.join(pict_path,pict_file_name+'.png'),
            pict_url + '/' + pict_file_name+'.png',
            thumb_url + '/' + pict_file_name+'.png',
            os.path.join(pict_thumb,pict_file_name+'.png'),
        )

    def get_filename(self, file):
        base = os.path.basename(file.filename)
        return secure_filename(os.path.splitext(base)[0])

    def create_url(self, pict_path):
        path = pict_path.split('/')[-3:]
        url = '/'.join(path)
        return url

    def return_size(self, file):
        return size(os.path.getsize(file.filename), system=si)

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

def return_slug(aTitle=''):
    return slugify(aTitle.lower())


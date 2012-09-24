import peewee

from datetime import datetime as dt
from random import choice
from datetime import datetime as dt

_database = peewee.MySQLDatabase('wing_cms', user='wing_user', passwd='wing_cms')

class BaseModel(peewee.Model):

	class Meta:
		database = _database

class Category(BaseModel):
	title = peewee.CharField(max_length=100)
	text = peewee.TextField(null=True)
	is_visible = peewee.BooleanField(default=False)
	date = peewee.DateField(default = dt.today().date())

	def __unicode__(self):
		return self.title


class Article(BaseModel):
	title = peewee.CharField(max_length=100)
	category = peewee.ForeignKeyField(Category)
	text = peewee.TextField(null=True)
	is_visible = peewee.BooleanField(default=False)
	date = peewee.DateField(default = dt.today().date())

class User(BaseModel):
    nickname = peewee.CharField()
    fullname = peewee.CharField()
    group = peewee.CharField()
    password = peewee.CharField()
    email = peewee.CharField()
    is_active = peewee.BooleanField(default = True)

    def __unicode__(self):
        return "%s, %s, %s" % self.nickname, self.group, self.password

    def is_admin(self):
        status = True if self.group == "admin" else False
        return status

    def is_editor(self):
        status = True if self.group == "editor" else False
        return status

class Album(BaseModel):
    title = peewee.CharField(max_length=100)
    description = peewee.TextField(null=True)
    album_path = peewee.CharField()
    thumb_path = peewee.CharField()

    def get_album_thumbnail(self):
        try:
            photos = [f for f in self.photo_set]
            thumbnail = choice(photos)
            return thumbnail.get_thumbnail()
        except IndexError:
            return 'images/default_empty_album.png'
        return 'Album is empty'

class Photo(BaseModel):
    album = peewee.ForeignKeyField(Album)
    title = peewee.CharField()
    photo_path = peewee.CharField()
    thumb_path = peewee.CharField()
    photo_url = peewee.CharField()
    thumb_url = peewee.CharField()
    size = peewee.CharField()
    date = peewee.DateField(default=dt.now().date())

    def get_thumbnail(self):
        return self.thumb_url

    def __unicode__(self):
        return self.title


_database.connect()
Article.create_table(True)
Category.create_table(True)
User.create_table(True)
Album.create_table(True)
Photo.create_table(True)

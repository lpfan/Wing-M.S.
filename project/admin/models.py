import peewee

from datetime import datetime as dt
from random import choice
from datetime import datetime as dt
from utils import return_slug

_database = peewee.MySQLDatabase('wing_cms', user='wing_user', passwd='wing_cms')

class BaseModel(peewee.Model):

	class Meta:
		database = _database

class Category(BaseModel):
    title = peewee.CharField(max_length=100)
    text = peewee.TextField(null=True)
    is_visible = peewee.BooleanField(default=False)
    date = peewee.DateField(default = dt.today().date())
    slug = peewee.CharField()

    def save(self):
        self.slug  = return_slug(aTitle=self.title)
        super(Category, self).save()

    def __unicode__(self):
        return self.title

    def get_permalink(self, **kwargs):
        return '<a href="/categories/%s" title="%s">%s</a>' % (self.slug, self.title, self.title)

    def get_link(self):
        return '/categories/%s' % self.slug


class Article(BaseModel):
    title = peewee.CharField(max_length=100)
    category = peewee.ForeignKeyField(Category, null=True)
    text = peewee.TextField(null=True)
    is_visible = peewee.BooleanField(default=False)
    is_index = peewee.BooleanField(default=False, unique = True)
    date = peewee.DateField(default = dt.today().date())
    slug = peewee.CharField()

    def save(self):
        self.slug  = return_slug(aTitle=self.title)
        super(Article, self).save()

    def get_permalink(self):
        return '<a href="/articles/%s" title="%s">%s</a>' % (self.slug, self.title, self.title)

    def get_link(self):
        return '/categories/%s/articles/%s' % (self.category.id, self.slug)

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

class Menu(BaseModel):
    title = peewee.CharField()
    url = peewee.CharField()
    template = peewee.TextField()
    utility_template = peewee.TextField()

_database.connect()
Article.create_table(True)
Category.create_table(True)
User.create_table(True)
Album.create_table(True)
Photo.create_table(True)
Menu.create_table(True)

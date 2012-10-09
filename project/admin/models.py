# -*- coding: utf-8 -*-

import peewee, pickle, pdb

from datetime import datetime as dt
from random import choice
from datetime import datetime as dt
from utils import return_slug

from project import bcrypt

_database = peewee.MySQLDatabase('wing_cms', user='wing_user', passwd='wing_cms')


class BaseModel(peewee.Model):

	class Meta:
		database = _database

class ArticleRevision(BaseModel):
    pickle_obj = peewee.TextField()
    creation_date = peewee.DateField(default = dt.today().date())

    def __unicode__(self):
        return 'rev. from %s. v%s' % (self.creation_date.strftime('%Y-%m-%d'), self.id)

class CategoryRevision(BaseModel):
    pickle_obj = peewee.TextField()
    creation_date = peewee.DateField(default = dt.today().date())

    def __unicode__(self):
        return 'rev. from %s. v%s' % (self.creation_date.strftime('%Y-%m-%d'), self.id)

class Menu(BaseModel):
    title = peewee.CharField()
    slug = peewee.CharField()
    url = peewee.CharField()
    template = peewee.TextField()
    utility_template = peewee.TextField()


class Category(BaseModel):
    revision = peewee.ForeignKeyField(CategoryRevision, related_name='revisions', null=True)
    title = peewee.CharField(max_length=100)
    text = peewee.TextField(null=True)
    is_visible = peewee.BooleanField(default=False)
    date = peewee.DateField(default = dt.today().date())
    slug = peewee.CharField(unique=True)

    def save(self):
        self.slug  = return_slug(aTitle=self.title)
        rev = CategoryRevision()
        rev.pickle_obj = pickle.dumps(self)
        rev.save()
        self.revision = rev
        super(Category, self).save()

    def delete_instance(self, recursive=True):
        try:
            Menu.get(slug=self.slug).delete_instance()
        except Menu.DoesNotExist, e:
            print "Error while removing menu item, %s" % e
        super(Category, self).delete_instance(recursive=recursive)

    def __unicode__(self):
        return self.title

    def get_permalink(self, **kwargs):
        return '<a href="/categories/%s" title="%s">%s</a>' % (self.slug, self.title, self.title)

    def get_link(self):
        return '/categories/%s' % self.slug

    def get_config_link(self):
        return '/config/categories/%s' %self.id


class Article(BaseModel):
    title = peewee.CharField(max_length=100)
    category = peewee.ForeignKeyField(Category, null=True)
    text = peewee.TextField(null=True)
    is_visible = peewee.BooleanField(default=False)
    is_index = peewee.BooleanField(default=False, unique = True)
    revision = peewee.ForeignKeyField(ArticleRevision, related_name='revisions', null=True)
    date = peewee.DateField(default = dt.today().date())
    slug = peewee.CharField(unique=True)

    def save(self):
        self.slug  = return_slug(aTitle=self.title)
        rev = ArticleRevision()
        rev.pickle_obj = pickle.dumps(self)
        rev.save()
        self.revision = rev 
        super(Article, self).save()

    def delete_instance(self, recursive=False):
        try:
            Menu.get(slug=self.slug).delete_instance()
        except Menu.DoesNotExist, e:
            print "Error while removing menu item, %s" % e
        super(Article, self).delete_instance(recursive=recursive) 

    def get_permalink(self):
        return '<a href="/articles/%s" title="%s">%s</a>' % (self.slug, self.title, self.title)

    def get_link(self):
        url = '/categories/%s/articles/%s' % (self.category.id, self.slug) if self.category else '/%s' % self.slug
        return url

    def get_config_link(self):
        return '/config/articles/%s' % self.id


class User(BaseModel):
    login = peewee.CharField()
    fullname = peewee.CharField(null=True)
    group = peewee.CharField(null=True)
    password = peewee.CharField()
    email = peewee.CharField()
    salt = peewee.CharField()
    is_active = peewee.BooleanField(default = True)
    ident_hash = peewee.CharField(unique=True)

    def save(self):
        self.salt = bcrypt.generate_password_hash(
            self.login[::-1]
        )
        self.ident_hash = bcrypt.generate_password_hash(self.login)
        self.password = bcrypt.generate_password_hash(self.salt+self.password)
        super(User, self).save()

    def __unicode__(self):
        return "%s" % self.login

    def is_admin(self):
        status = True if self.group == "admin" else False
        return status

    def is_editor(self):
        status = True if self.group == "editor" else False
        return status

    def is_anonymous(self):
        return False

    def is_authenticated(self, aUser='', aPassword=''):
        salt = self.salt
        salted_passwd = salt + str(aPassword)
        if bcrypt.check_password_hash(self.password, salted_passwd):return True
        return None

    def is_active(self):
        if not self.is_active: return False
        return True

    def get_id(self):
        return self.id


class Album(BaseModel):
    title = peewee.CharField(max_length=100)
    description = peewee.TextField(null=True)
    album_path = peewee.CharField()
    thumb_path = peewee.CharField()
    slug = peewee.CharField(unique=True)

    def save(self):
        self.slug = return_slug(aTitle=self.title)
        super(Album, self).save()

    def get_album_thumbnail(self):
        try:
            photos = [f for f in self.photo_set]
            thumbnail = choice(photos)
            return thumbnail.get_thumbnail()
        except IndexError:
            return 'images/default_empty_album.png'
        return 'Album is empty'

    def get_link(self):
        return "/albums/%s" % self.slug

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

class GeneralMeta(BaseModel):
    meta_d = peewee.TextField(null=True)
    meta_k = peewee.TextField(null=True)

_database.connect()
ArticleRevision.create_table(True)
CategoryRevision.create_table(True)
Article.create_table(True)
Category.create_table(True)
User.create_table(True)
Album.create_table(True)
Photo.create_table(True)
Menu.create_table(True)
GeneralMeta.create_table(True)


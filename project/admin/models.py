import peewee

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


_database.connect()
Article.create_table(True)
Category.create_table(True)
User.create_table(True)

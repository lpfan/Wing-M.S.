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

_database.connect()
Article.create_table(True)
Category.create_table(True)
import peewee

_database = peewee.MySQLDatabase('wing_cms', user='wing_user', passwd='wing_cms')

class Articles(peewee.Model):
	title = peewee.CharField(max_length=100)
	text = peewee.TextField(null=True)

	class Meta:
		database = _database


_database.connect()
Articles.create_table(True)
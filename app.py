from flask import Flask
from flask.ext.admin import Admin
from admin.models import Articles
from flask.ext.admin.contrib.peeweemodel import ModelView

app = Flask(__name__)

admin = Admin(app)
admin.add_view(ModelView(
	Articles,
	name="Articles")
)

app.debug = True
SECRET_KEY = 'misha1987'
app.config.from_object(__name__)

if __name__ == '__main__':
	app.run()
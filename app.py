from flask import Flask
from flask.ext.admin import Admin
from admin.index import GeneralView


app = Flask(__name__)

admin = Admin(app)
admin.add_view(GeneralView(name='Articles'))

app.debug = True

if __name__ == '__main__':
	app.run()
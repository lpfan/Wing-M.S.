from flask import request
from flask.ext.admin import BaseView, expose
from forms import NewAlbumForm
from models import Album

class GalleryView(BaseView):
	@expose('/')
	def index(self):
		albums = Album.select()
		return self.render('admin/gallery.html', albums=albums)

	@expose('/new_album/', methods=('GET', 'POST'))
	def new_album(self):
		form = NewAlbumForm(request.form or None)
		if request.method == 'POST':
			pass
		return self.render('admin/new_album.html', form=form)
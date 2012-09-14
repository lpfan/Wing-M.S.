from flask.ext.admin import BaseView, expose

class GalleryView(BaseView):
	@expose('/')
	def index(self):
		return self.render('admin/gallery.html')
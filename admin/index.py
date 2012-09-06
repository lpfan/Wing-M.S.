from flask.ext.admin import Admin, BaseView, expose

class GeneralView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class ArticlesView(BaseView):
	@expose('/')
	def index(self):
		return self.render('admin/articles.html')
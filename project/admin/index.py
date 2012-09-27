import pdb, json, pickle

from flask import Response, request, url_for
from flask.ext.admin import Admin, BaseView, expose
from models import Category, Article, MenuItem
from flask.ext.admin.base import AdminIndexView

class GeneralView(AdminIndexView):
    @expose('/')
    def index(self):
    	menu = MenuItem.select()
    	categories = Category.select()
        return self.render('admin/index.html', categories=categories, menu=menu)

    @expose('/content_structure')
    def content_structure(self):
    	children = []
    	categories = Category.select()
    	for category in categories:
    		articles = category.article_set
    		if articles.count() > 0:
    			children.append({
    				'title':category.title,
    				'isFolder': 'true',
                    'key':pickle.dumps(category),
    				'children':self.get_children(articles)
    				})
    		else:	
    			children.append({
                    'title':category.title,
                    'key':pickle.dumps(category)
                    })
    	return json.dumps(children)

    @expose('/new_menu_item', methods=('POST','GET'))
    def new_menu_item(self):
        obj = pickle.loads(str(request.form['key']))
        pdb.set_trace()
        #print obj.title
        return obj.title

    def get_children(self, children_set):
    	result = []
    	for child in children_set:
            result.append({
                    'title':child.title,
                    'key':"%s" % pickle.dumps(child),
                    'href':child.slug
                })
        return result

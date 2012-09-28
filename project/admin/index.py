# -*- coding: utf-8 -*-

import pdb, json, pickle

from flask import Response, request, url_for, redirect, flash
from flask.ext.admin import Admin, BaseView, expose
from models import Category, Article, Menu
from flask.ext.admin.base import AdminIndexView

class GeneralView(AdminIndexView):
    @expose('/')
    def index(self):
    	menu = None
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
        for article in Article.select().where(category__is=None):
            children.append({
                'title':article.title
            })
    	return json.dumps(children)

    @expose('/new_menu_item', methods=('POST','GET'))
    def new_menu_item(self):
        '''
        obj = pickle.loads(str(request.form['key']))
        set_name = obj._meta.reverse_relations.keys()[0]
        rel_set = getattr(obj, set_name)
        pdb.set_trace()
        #print obj.title
        return obj.title
        '''
        form = request.form
        itemTitle = form.get('itemTitle', None)
        itemUrl = form.get('itemUrl', None)
        itemTemplate = form.get('itemTemplate', None)
        menu = Menu()
        menu.title = itemTitle
        menu.url = itemUrl
        menu.template = itemTemplate
        try:
            flash(u'Новий пункт меню успішно збережений')
            menu.save()
        except Exception, e:
            flash(u'Помилка під час зберігання')
        return 'done'

    def get_children(self, children_set):
    	result = []
    	for child in children_set:
            result.append({
                    'title':child.title,
                    'key':"%s" % pickle.dumps(child),
                    'href':child.slug
                })
        return result

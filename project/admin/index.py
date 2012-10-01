# -*- coding: utf-8 -*-

import pdb, json, pickle

from flask import Response, request, url_for, redirect, flash
from flask.ext.admin import Admin, BaseView, expose
from models import Category, Article, Menu
from flask.ext.admin.base import AdminIndexView

class GeneralView(AdminIndexView):
    @expose('/')
    def index(self):
    	menu = Menu.select()
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
                    'href':category.get_link(),
    				'isFolder': 'true',
    				'children':self.get_children(articles)
    				})
    		else:	
    			children.append({
                    'title':category.title,
                    'href':category.get_link()
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
        itemUtilityTemplate = form.get('itemUtilityTemplate', None)
        menu = Menu()
        menu.title = itemTitle
        menu.url = itemUrl
        menu.template = itemTemplate
        menu.utility_template = itemUtilityTemplate
        status = None
        try:
            status = u'Новий пункт меню успішно збережений'
            menu.save()
        except Exception, e:
            status = u'Помилка під час зберігання'
        return Response(status)

    def get_children(self, children_set):
    	result = []
    	for child in children_set:
            result.append({
                    'title':child.title,
                    'key':"%s" % pickle.dumps(child),
                    'href':child.get_link()
                })
        return result

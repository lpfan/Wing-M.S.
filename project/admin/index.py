# -*- coding: utf-8 -*-

import pdb, json, pickle

from flask import Response, request, url_for, redirect, flash
from flask.ext.admin import Admin, BaseView, expose
from models import Category, Article, Menu, Album, GeneralMeta
from forms import MetaDataForm
from flask.ext.admin.base import AdminIndexView
from flask.ext import login

class GeneralView(AdminIndexView):

    def is_accessible(self):
        if not login.current_user.is_anonymous(): return True

    @expose('/')
    def index(self):
    	menu = Menu.select()
        g_m = GeneralMeta.get_or_create(id=1)
        form = MetaDataForm(obj=g_m)
    	categories = Category.select()
        return self.render(
            'admin/index.html',
            categories=categories,
            menu=menu,
            meta_form = form
        )

    @expose('/meta_info/store', methods=['POST'])
    def store_meta_info(self):
        form = MetaDataForm(request.form or None)
        if form and form.validate():
            g_m = GeneralMeta.update(meta_d = "".join(form.meta_d.raw_data), meta_k = "".join(form.meta_k.raw_data)).where(id=1)
            g_m.execute()
            flash(u'Мета інформація обновлена успішно')
        else:
            flash(u'Помилка під час валідації даних')
        return redirect(url_for('.index'))

    @expose('/content_structure')
    def content_structure(self):
    	children = []
    	categories = Category.filter(is_visible=True)
    	for category in categories:
    		articles = category.article_set
    		if articles.count() > 0:
    			children.append({
    				'title':category.title,
                    'href':category.get_link(),
                    'key': category.slug,
    				'isFolder': 'true',
    				'children':self.get_children(articles)
    				})
    		else:	
    			children.append({
                    'title':category.title,
                    'href':category.get_link(),
                    'key':category.slug
                    })
        for article in Article.filter(is_visible=True).where(category__is=None):
            children.append({
                'title':article.title,
                'href':article.get_link(),
                'key':article.slug
            })
    	return json.dumps(children)

    @expose('/new_menu_item', methods=('POST','GET'))
    def new_menu_item(self):
        form = request.form
        itemTitle = form.get('itemTitle', None)
        itemUrl = form.get('itemUrl', None)
        itemTemplate = form.get('itemTemplate', None)
        itemUtilityTemplate = form.get('itemUtilityTemplate', None)
        itemSlug = form.get('itemSlug', None)
        menu = Menu()
        menu.title = itemTitle
        menu.url = itemUrl
        menu.template = itemTemplate
        menu.utility_template = itemUtilityTemplate
        menu.slug = itemSlug
        status = None
        try:
            status = menu.utility_template
            menu.save()
        except Exception, e:
            status = u'Помилка під час зберігання'
        return Response(status)

    @expose('/menu/<int:menu_id>/settings', methods=('GET', 'POST',))
    def menu_settings(self, menu_id=0):
        if request.method == 'GET':
            itemTmpl = ''
            try:
                itemTmpl = Menu.get(id=menu_id).template
            except Menu.DoesNotExist, e:
                print 'Error while loading item template, %s' % e
            return itemTmpl
        elif request.method == 'POST':
            form = request.form
            itemTitle = form.get('itemTitle', None)
            itemTemplate = form.get('itemTemplate', None)
            if itemTitle and itemTemplate:
                menu = Menu.update(title=itemTitle,template=itemTemplate).where(id=menu_id)
                menu.execute()
                flash(u'Зміни внесені успішно')
            else:
                flash(u'Під час збереження сталась помилка')
            return redirect(url_for('.index'))

    @expose('/menu/remove_menu_item/<int:menu_id>', methods=('GET',))
    def remove_menu_item(self, menu_id):
        try:
            Menu.get(id=menu_id).delete_instance()
            flash(u'Пункт меню видалений успішно')
        except Menu.DoesNotExist, e:
            print "Error while deleting menu item, %s" % e
        return redirect(url_for('.index'))

    def get_children(self, children_set):
    	result = []
    	for child in children_set:
            result.append({
                    'title':child.title,
                    'href':child.get_link(),
                    'key':child.get_config_link()
                })
        return result

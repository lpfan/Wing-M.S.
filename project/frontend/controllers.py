# -*- coding: utf-8 -*-
import pdb

from flask import Response, request, url_for, redirect, flash, render_template, abort

from project import app
from project.admin.models import Article, Menu

template_path = 'frontend/'


@app.route('/')
def index(title=u"головна сторінка"):
    main_content = ''
    menu = Menu.select()
    try:
        main_content = Article.get(is_index=True).text
    except Article.DoesNotExist, e:
        print "error while getting the index page, %s" % e
    return render_template(template_path+'index.html',
        title=title,
        content=main_content,
        menu=menu
    )

@app.route('/<string:slug>')
def show_alone_article(slug):
    obj = None
    menu = Menu.select()
    try:
        obj = Article.get(slug=slug)
    except Article.DoesNotExist, e:
        print "Error while geting article, %s" % e
        abort(404)
    return render_template(template_path+'index.html',
        title=obj.title,
        content=obj.text if obj else 'Empty content',
        menu=menu
    )
@app.route('/categories/<string:cat_slug>')
def show_category(cat_slug):
    pass

@app.route('/images/<string:filename>')
def send_static_file(filename):
    path = 'images/' + filename
    return app.send_static_file(path)

@app.errorhandler(404)
def page_not_found(e):
    return render_template(template_path + '404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template(template_path + '500.html'), 500

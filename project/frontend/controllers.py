# -*- coding: utf-8 -*-
import pdb

from flask import Response, request, url_for, redirect, flash, render_template, abort

from project import app
from project.admin.models import Article, Menu, Category, Album

template_path = 'frontend/'

@app.route('/')
def index(title=u"головна сторінка"):
    main_content = ''
    try:
        main_content = Article.get(is_index=True)
    except Article.DoesNotExist, e:
        print "error while getting the index page, %s" % e
    return render_template(template_path+'index.html',
        title=main_content.title,
        article=main_content
    )

@app.route('/<string:slug>')
def show_alone_article(slug, tmpl=template_path+'show_article.html'):
    article = None
    try:
        article = Article.get(slug=slug)
        if article.is_index: tmpl = template_path+'index.html'
    except Article.DoesNotExist, e:
        print "Error while geting article, %s" % e
        abort(404)
    return render_template(tmpl,
        title=article.title,
        article=article
    )
@app.route('/categories/<string:cat_slug>')
def show_category(cat_slug):
    category = Category.get(slug=cat_slug)
    articles = category.article_set
    return render_template(template_path+'show_category.html', category = category, articles=articles)

@app.route('/categories/<int:cat_id>/articles/<string:article_slug>')
def shot_cat_article(cat_id, article_slug=''):
    article = Article.filter(slug=article_slug).join(Category).where(Category.id==cat_id).get()
    return render_template(template_path+'show_article.html', article=article, title=article.title)

@app.route('/albums/<string:album_slug>')
def show_album(album_slug=''):
    album = ''
    try:
        album = Album.get(slug=album_slug)
    except Album.DoesNotExist, e:
        print "Album does not exists, %s" % e
    return render_template(template_path+'show_album.html', album=album, title=album)

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

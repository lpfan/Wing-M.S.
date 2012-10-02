# -*- coding: utf-8 -*-
import pdb

from flask import Response, request, url_for, redirect, flash, render_template

from project import app
from project.admin.models import Article

template_path = 'frontend/'

@app.route('/')
def index(title=u"головна сторінка"):
    main_content = ''
    try:
        main_content = Article.get(is_index=True).text
    except Article.DoesNotExist, e:
        print "error while getting the index page, %s" % e
    return render_template(template_path+'index.html', title=title, content=main_content)

@app.route('/images/<string:filename>')
def send_static_file(filename):
    path = 'images/' + filename
    return app.send_static_file(path)


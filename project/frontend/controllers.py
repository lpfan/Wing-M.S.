from flask import Response, request, url_for, redirect, flash, render_template

from project import app

template_path = 'frontend/'

@app.route('/')
def index():
    return render_template(template_path+'index.html')


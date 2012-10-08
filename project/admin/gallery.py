# -*- coding: utf-8 -*-

import pdb, json

from flask import request, redirect, url_for, flash
from flask.ext.admin import BaseView, expose
from peewee import DoesNotExist
from forms import NewAlbumForm
from models import Album, Photo
from utils import GalleryManager
from flask.ext import login

class GalleryView(BaseView):

	gal_man = GalleryManager()

	def is_accessible(self):
		if not login.current_user.is_anonymous(): return True

	@expose('/')
	def index(self):
		albums = Album.select()
		return self.render('admin/gallery.html', albums=albums)

	@expose('/new_album/', methods=('GET', 'POST'))
	def new_album(self):
		form = NewAlbumForm(request.form or None)
		if request.method == 'POST' and form.validate():
			album = Album()
			album_title = request.form['title']
			album_description = request.form['description']
			album_path, album_thumb = self.gal_man.create_album(album_title)
			album.title = album_title
			album.description = album_description
			album.album_path = album_path
			album.thumb_path = album_thumb
			album.save()
			return redirect(url_for('.show_album', album_id=album.id))
		return self.render('admin/new_album.html', form=form)

	@expose('/show_album/<int:album_id>/', methods=('GET',))
	def show_album(self, album_id=''):
		album=None
		try:
			album = Album.get(id=album_id)
		except DoesNotExist:
			print 'album does not exists'
		return self.render('admin/show_album.html', album=album)

	@expose('/show_album/<int:album_id>/add_photo/', methods=('GET', 'POST',))
	def add_photo(self, album_id=''):
		if request.method == 'POST':
			album = Album.get(id=album_id)
			photo = Photo()
			photo.album = album
			file = request.files['files']
			photo_title, size, photo_path, photo_url, thumb_url, thumb_path = self.gal_man.add_photo(album, file)
			result = []
			result.append({
				'name':photo_title,
				'size':size,
				'url':photo_url,
				'thumbnail_url':thumb_path,
				"delete_type":"POST",
			})
			photo.title = photo_title
			photo.photo_path = photo_path
			photo.thumb_path = thumb_path
			photo.photo_url = photo_url
			photo.thumb_url = thumb_url
			photo.size = size
			photo.save()
			return json.dumps(result)
		else:
			return 'response'

	@expose('/show_album/<int:album_id>/remove_photo/', methods=('POST','GET',))
	def remove_photo(self, album_id=''):
		if request.method == 'POST':
			form = request.form
			for v in form.itervalues():
				try:
					photo = Photo.get(id=v)
					photo.delete_instance()
				except DoesNotExist, e:
					print '%s' % e
		return redirect(url_for('.show_album', album_id=album_id))

	@expose('/show_album/<int:album_id>/remove_photo/<int:photo_id>', methods=('POST','GET',))
	def remove_current_photo(self, album_id='', photo_id=''):
		if request.method == 'GET':
			if photo_id:
				try:
					photo = Photo.get(id=photo_id)
					photo.delete_instance()
					flash(u"Фотографія %s успішно видалина." % photo.title)
				except DoesNotExist, e:
					print '%s' % e
		return redirect(url_for('.show_album', album_id=album_id))
	@expose('/show_album/<int:album_id>/delete', methods=('GET',))
	def remove_album(self, album_id=''):
		try:
			album = Album.get(id=album_id)
			album.delete_instance()
			flash(u"Альбом %s видалено успішно" % album.title)
			return redirect(url_for('.index'))
		except DoesNotExist:
			print "album does not exist"
		flash(u"Такого альбому не існує")
		return redirect(url_for('.index'))
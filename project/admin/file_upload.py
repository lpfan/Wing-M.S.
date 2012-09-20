# -*- coding: utf-8 -*-

import project, Image, os, pdb, json

from project import app
from flask import request, Response, send_file
from utils import ConfigManager, GalleryManager
from project.config import PICT_FOLDER,THUMB_FOLDER


@app.route('/admin/file_upload/', methods=['POST', 'GET'])
def file_upload():
	if request.method == 'POST':
		file = request.files['file']
		print file

@app.route('/admin/uploaded_files/', methods=['GET'])
def uploaded_files():
	__uploaded_files = []
	__files = []
	__pict_folder = '/' + '/'.join(PICT_FOLDER.split('/')[-2:]) + '/'
	__thumb_folder = '/' + '/'.join(THUMB_FOLDER.split('/')[-2:]) +'/'
	for dirpath, dirname, filenames in os.walk(PICT_FOLDER):
		#pdb.set_trace()
		__files.extend(filenames)
	for file in __files:
		__uploaded_files.append({'image':os.path.join(__pict_folder, file), 'thumb':os.path.join(__thumb_folder ,file)})
	resp = Response(json.dumps(__uploaded_files), status=200, mimetype='application/json')
	return resp

@app.route('/admin/image_upload/', methods=['POST', 'GET'])
def image_upload():
	image = request.files['file']
	if image and allowed_file(image.filename):
		__pict_folder = '/' + '/'.join(PICT_FOLDER.split('/')[-2:]) + '/'
		image = GalleryManager().save_as_png(image)
		img_filename = os.path.basename(image.filename) 
		response = {'filelink':os.path.join(__pict_folder, img_filename)}
		return json.dumps(response)


@app.route('/uploads/thumb/<string:file_name>')
def get_image_thumb(file_name):
	__thumb = THUMB_FOLDER + '/' + file_name
	try:
		return send_file(__thumb, 'image/png')
	except IOError:
		print 'file was removed by someone'

@app.route('/uploads/pict/<string:file_name>')
def get_image_pict(file_name):
	__pict = PICT_FOLDER + '/' + file_name
	try:
		return send_file(__pict, 'image/png')
	except IOError:
		print 'file was removed by someone'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in project.ALLOWED_EXTENSIONS
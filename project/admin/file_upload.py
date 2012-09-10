import project, Image, os, pdb, json

from project import app
from flask import request, Response, send_file

__UPLOAD_FOLDER = project.UPLOAD_FOLDER 
__PICT_FOLDER = os.path.join(__UPLOAD_FOLDER, 'pict')
__THUMB_FOLDER = os.path.join(__UPLOAD_FOLDER, 'thumb')

@app.route('/admin/file_upload/', methods=['POST', 'GET'])
def file_upload():
	if request.method == 'POST':
		file = request.files['file']
		print file

@app.route('/admin/uploaded_files/', methods=['GET'])
def uploaded_files():
	__uploaded_dict = {}
	files = []
	__pict_folder = '/' + '/'.join(__PICT_FOLDER.split('/')[-2:]) + '/'
	__thumb_folder = '/' + '/'.join(__THUMB_FOLDER.split('/')[-2:]) +'/'
	for (dirpath, dirname, filenames) in os.walk(__PICT_FOLDER):
		files.extend(filenames)
	for file in files:
		__uploaded_dict.update({'image':os.path.join(__pict_folder, file), 'thumb':os.path.join(__thumb_folder ,file)})
	resp = Response(json.dumps([__uploaded_dict]), status=200, mimetype='application/json')
	return resp

@app.route('/admin/image_upload/', methods=['POST', 'GET'])
def image_upload():
	pass

@app.route('/uploads/thumb/<string:file_name>')
def get_image_thumb(file_name):
	__thumb = __THUMB_FOLDER + '/' + file_name
	return send_file(__thumb, 'image/png')

@app.route('/uploads/pict/<string:file_name>')
def get_image_thumb(file_name):
	__pict = __PICT_FOLDER + '/' + file_name
	return send_file(__pict, 'image/png')

def create_thumbnail(target_path):
	pass
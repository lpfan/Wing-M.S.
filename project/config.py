import os

def rel(*x):
	return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

UPLOAD_FOLDER = os.path.join(rel('static'), 'uploads')
PICT_FOLDER = os.path.join(UPLOAD_FOLDER, 'pict')
THUMB_FOLDER = os.path.join(UPLOAD_FOLDER, 'thumb')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SETTINGS_PATH = rel('settings.cfg')
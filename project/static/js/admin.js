$(document).ready(function(){
	$('#text').redactor({
		fileUpload: '/admin/file_upload/',
		imageGetJson: '/admin/uploaded_files/',
		imageUpload: '/admin/image_upload/',
	});
	$('#description').redactor({
		fileUpload: '/admin/file_upload/',
		imageGetJson: '/admin/uploaded_files/',
		imageUpload: '/admin/image_upload/',
	});
	return false;
})
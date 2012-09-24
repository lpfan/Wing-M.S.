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

	$('#js_add_new_photo').bind('click', function(e){
		e.preventDefault();
		$('#multiupload_holder').slideDown('slow');
		$('#js_end_loading').removeClass('js_hidden');
		return false;
	})
	return false;
})
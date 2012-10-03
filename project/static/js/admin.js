$(document).ready(function(){

	$('#js_add_new_photo').bind('click', function(e){
		e.preventDefault();
		$('#multiupload_holder').slideDown('slow');
		$('#js_end_loading').removeClass('js_hidden');
		return false;
	})
	return false;
})
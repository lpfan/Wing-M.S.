$(document).ready(function(){
	
	var redactor_js_allowed = [
			"code", "span", "div", "label", "a", "br", "p", "b", "i", "del", "strike", "u",
			"img", "video", "audio", "iframe", "object", "embed", "param", "blockquote", 
			"mark", "cite", "small", "ul", "ol", "li", "hr", "dl", "dt", "dd", "sup", "sub", 
			"big", "pre", "code", "figure", "figcaption", "strong", "em", "table", "tr", "td", 
			"th", "tbody", "thead", "tfoot", "h1", "h2", "h3", "h4", "h5", "h6", "script"];

	$('#text').redactor({
		fileUpload: '/admin/file_upload/',
		imageGetJson: '/admin/uploaded_files/',
		imageUpload: '/admin/image_upload/',
		allowedTags: [
			"code", "span", "div", "label", "a", "br", "p", "b", "i", "del", "strike", "u",
			"img", "video", "audio", "iframe", "object", "embed", "param", "blockquote", 
			"mark", "cite", "small", "ul", "ol", "li", "hr", "dl", "dt", "dd", "sup", "sub", 
			"big", "pre", "code", "figure", "figcaption", "strong", "em", "table", "tr", "td", 
			"th", "tbody", "thead", "tfoot", "h1", "h2", "h3", "h4", "h5", "h6", "script"],
		cleanup: false
	});
	$('#description').redactor({
		fileUpload: '/admin/file_upload/',
		imageGetJson: '/admin/uploaded_files/',
		imageUpload: '/admin/image_upload/',
		allowedTags: redactor_js_allowed
	});

	$('#js_add_new_photo').bind('click', function(e){
		e.preventDefault();
		$('#multiupload_holder').slideDown('slow');
		$('#js_end_loading').removeClass('js_hidden');
		return false;
	})
	return false;
})
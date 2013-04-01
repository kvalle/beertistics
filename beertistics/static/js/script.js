$('.note-form .save-note').click(function(e){
    e.preventDefault(); // Stall form submit
    $('.note-form #target_state').val($(this).data('target-state'));
    $(this).parents('form:first').submit(); // Submit form
});

$('input[id=actual-file-field]').change(function() {
	$('#fake-file-field').val($(this).val());
});

$(".new-file-button").click(function () {
	$(".new-file-form").toggle("slow");
}); 

$("#fake-file-button").click(function () { 
	$('input[id=actual-file-field]').click();
});

$("#fake-file-field").click(function () { 
	$('input[id=actual-file-field]').click();
}); 

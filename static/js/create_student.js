$('#create_student .one-talent .add-talent').on('click', function(){
	$(this).parents('.one-talent').next('.one-talent').css('display', 'block');
	$(this).css('display', 'none');
})
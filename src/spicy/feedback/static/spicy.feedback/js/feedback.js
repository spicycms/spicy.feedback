var spicy = spicy || {};

var feedback = function(form_id, popup_id, callback){        
    
    var form = $('#' + form_id);
    var validator = form.data("validator");            


    if(validator.checkValidity()){
	$.post(form.attr('action'), form.serialize(), function(data){
		if(data.status == 'success'){
		    if (callback != undefined){
			return callback();
		    } else {
			$('#' + popup_id).html('<p>Спасибо! С вами свяжутся в кратчайший срок.</p>');
		    }

		    return true;
		    // Redirect on submit:                                                                                                                                                  
		    //window.location = 'http://www.example.com/somePage.html';                                                                                                             
		}
		else {
		    validator.invalidate(data.errors);
		    $('#' + popup_id).append(data.errors);
		    return false;
		}		
		
	    }, "json");
    } else {
	console.log('jquery.uniform.js validator plugin required');
    }
    return false;
};

spicy.feedback = feedback;

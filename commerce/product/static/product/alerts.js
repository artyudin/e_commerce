function showFlashMessage(message){
		var template = "<div class='container-alert-flash'><div class='alert alert-success alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>"+ message "</div></div>"
			$("body").append(template);
			$(".container-alert-flash").fadeIn();
			setTimeout(function(){
				$(".container-alert-flash").fadeOut();
			}, 2500);


	}
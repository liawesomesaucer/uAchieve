// various javascript settings for uAchieve application

// user clicks sign in; shows the sign in box
	function signin() {
	    $( '.body' ).fadeTo(400, 0.5);
		$( '.popup_signin' ).fadeIn();
	}

	// hides the sign in box
	function hide_signin() { 
		$( '.body' ).fadeTo(400, 1);
		$( '.popup_signin' ).fadeOut(400);
	}

	// user clicks register; shows the registration box
	function register() {
	    $( '.body' ).fadeTo(400, 0.5);
	    $( '.popup_register' ).fadeIn();
	}

	// hides the registration box
	function hide_register() {
		$( '.body' ).fadeTo(400, 1);
		$( '.popup_register' ).fadeOut(400);
	}

	// if the person presses escape
	$(document).keyup(function(e) {
  		if (e.keyCode == 27) {
  			hide_signin();	// hide all the stuff
  			hide_register();
  			}   
	});
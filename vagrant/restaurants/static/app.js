

window.onload = () => {

	(function restaurants_html(){
		// Show a restaurant's action buttons only when hovering it
		function toggleActions(){ $(this).find('a:not(.btn-default)').toggleClass('hidden'); };
		$('#restaurant-list .btn-group').hover(toggleActions, toggleActions);
	console.log('ad');
	})();
	
};
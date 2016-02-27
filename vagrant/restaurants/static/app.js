

window.onload = () => {

	(function restaurants_html(){
		// Show a restaurant's action buttons only when hovering it
		function toggleActions(){ $(this).find('a:not(.btn-default)').toggleClass('hidden'); };
		$('#restaurant-list .btn-group').hover(toggleActions, toggleActions);
	})();

	(function showmenu_html(){
		// Adjust all menu item boxes to have the same height
		var maxHeight = 0;
		const thumbs = $('.thumbnail');
		thumbs.each(function(){
			var h = $(this).height();
			if(h > maxHeight) maxHeight = h;
		});
		thumbs.height(maxHeight);
	})();
	
};
function selectSkin(id) {
	$(".skin").removeClass("enabled");
	$("#" + id).addClass("enabled");
}
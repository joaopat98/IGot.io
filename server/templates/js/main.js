function selectSkin(id) {
	$(".skin").removeClass("enabled");
	$("#" + id).addClass("enabled");
}

let input = {};

let submit = () => {
    Request.post("api/join", input).then(response => {
        if (response.status !== 200) {
            response.json().then(errors => {

            });
        } else {
            response.json().then(data => {
                window.location.assign(window.location.origin + "/play");
            });
        }
    });
};

window.onload = () => {
	document.getElementById("username_box").onchange = ev => {
		input["name"] = ev.currentTarget.value;
	};
};
function selectSkin(id) {
    $(".skin").removeClass("enabled");
    $("#" + id).addClass("enabled");
}

let input = {};

let submit = () => {
    console.log(input);
    Request.post("api/join", input).then(response => {
        if (response.status !== 200) {
            response.json().then(errors => {

            });
        } else {
            window.location.assign(window.location.origin + "/play");
        }
    });
};

window.addEventListener("load", () => {
    document.getElementById("username_box").onchange = ev => {
        input["name"] = ev.currentTarget.value;
    };
});
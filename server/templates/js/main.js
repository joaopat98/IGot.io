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

window.onload = () => {
    // handler for fixing suspended audio context in Chrome
    try {
        if (createjs.WebAudioPlugin.context.state === "suspended") {
            createjs.WebAudioPlugin.context.resume();
            // Should only need to fire once
            window.removeEventListener("click", playMenuSong);
        }
    } catch (e) {
        // SoundJS context or web audio plugin may not exist
        console.error("There was an error while trying to resume the SoundJS Web Audio context...");
        console.error(e);
    }
    window.addEventListener("click", playMenuSong);
    document.body.click();

	document.getElementById("username_box").onchange = ev => {
		input["name"] = ev.currentTarget.value;
	};
};

function loadMusic(){
    /*Music/Sound Stuff*/
    createjs.Sound.alternateExtensions = ["mp3"];
    createjs.Sound.on("fileload", playMenuSong);
    createjs.Sound.registerSound("static/res/background_music.mp3", "menuMusic", 1);
    //createjs.Sound.registerSound("../Resources/Audio/gameMusic.mp3", "gameMusic", 2);

}

function playMenuSong(){
    var instance = createjs.Sound.play("menuMusic");
    instance.on("complete", playMenuSong);
}


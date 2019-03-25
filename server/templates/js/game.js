"use strict";

var queue, stage, arena, time, player, score, leaderboard, numberPlayers;
var mapWidth = 3000, mapHeight = 3000;
let ws;

function loadImages(data, onComplete) {
    queue = new createjs.LoadQueue(false, null, true);
    queue.on("complete", onComplete, this);
    queue.loadFile({src: "static/res/tile.png", crossOrigin: true, id: "tile"});
    queue.loadFile({src: "static/res/laser.png", crossOrigin: true, id: "laser"});
    for (let skin in data) {
        console.log("static/res/skins/" + data[skin]);
        queue.loadFile({src: "static/res/skins/" + data[skin], crossOrigin: true, id: skin});
    }
}

function init() {
    Request.post("api/load", {}).then(response => {
        response.json().then(data => {
            loadImages(data.skins, () => {
                stage = new createjs.Stage("canvas");
                player = new Character(data.playerX, data.playerY, queue.getResult(data.playerSkin), data.charSize, queue.getResult("laser"), 595, 64, data.fov, true, data.mapWidth, data.mapHeight, data.id, data.speed);
                arena = new Arena(queue.getResult("tile"), player, time, data.mapWidth, data.mapHeight);
                arena.x = window.innerWidth / 2;
                arena.y = window.innerHeight / 2;
                stage.addChild(arena);
                leaderboard = new LeaderBoard(300, 10);
                leaderboard.x = window.innerWidth - 300;
                createScore();
                createNumberP();
                stage.addChild(leaderboard);
                stage.addChild(score);
                stage.addChild(numberPlayers);
                config();
                window.addEventListener("keydown", keyHandler);
                window.addEventListener("keyup", keyHandler);
                ws = new WebSocket("wss://" + window.location.host + "/ws/group");
                ws.onmessage = message => {
                    let newData = JSON.parse(message.data);
                    newData.chars.forEach(char => {
                        if (arena.chars.hasOwnProperty(char.id)) {
                            if (char.id === player.id) {
                                player.score = char.score;
                                scoreUpdate();
                                arena.player.x = char.x;
                                arena.player.y = char.y;
                            } else {
                                let b = arena.chars[char.id];
                                b.x = char.x;
                                b.y = char.y;
                            }
                        } else {
                            let c = new Character(char.x, char.y, queue.getResult(char.skin), data.charSize, undefined, undefined, undefined, 0, false, data.mapWidth, data.mapHeight, char.id, data.speed);
                            arena.chars[char.id] = c;
                            arena.addChild(c);
                        }
                    });
                    console.log(newData.chars);
                    console.log(arena.chars);

                    leaderboard.update(newData.leaderboard);
                    numberPUpdate(newData.number_players);

                    for (let char in arena.chars) {
                        if (newData.chars.find(c => c.id == char) === undefined) {
                            arena.removeChild(arena.chars[char]);
                            delete arena.chars[char]
                        }
                    }
                }
            });
        });
    });

}

function resize() {
    stage.canvas.width = window.innerWidth;
    stage.canvas.height = window.innerHeight;
}

function display(ev) {
    resize();
    player.move(ev.delta, ws);

    arena.regX = Math.min(Math.max(-mapWidth / 2 + stage.canvas.width / 2, player.x), mapWidth / 2 - stage.canvas.width / 2);
    arena.regY = Math.min(Math.max(-mapHeight / 2 + stage.canvas.height / 2, player.y), mapHeight / 2 - stage.canvas.height / 2);

    /*
    if(player.sprite.x > - mapWidth/2 + stage.canvas.width/2 && player.sprite.x < mapWidth/2 - stage.canvas.width/2)
        arena.regX = player.sprite.x;

    if(player.sprite.y > - mapHeight/2 + stage.canvas.height/2 && player.sprite.y < mapHeight/2 - stage.canvas.height/2)
        arena.regY = player.sprite.y;
    */

    stage.update();
}

function config() {
    time = createjs.Ticker.getTime(true);
    createjs.Ticker.addEventListener("tick", display);
    createjs.Ticker.framerate = 60;
}

function keyHandler(ev) {
    arena.player.keys[ev.keyCode] = (ev.type === "keydown");
    if (player.shootOnce == false && ev.type === "keyup" && ev.keyCode == 32) {
        arena.player.shootOnce = true;
    }
}


function createScore() {
    score = new createjs.Text("Own score: " + player.score, "20px Arial", "#000000");
    console.log(score.getBounds().width);
    score.x = window.innerWidth - score.getBounds().width - 10;
    score.y = leaderboard.getBounds().height + 5;
}

function scoreUpdate() {
    score.text = "Own score:" + player.score;
    score.x = window.innerWidth - score.getBounds().width - 10;
}

function createNumberP() {
    numberPlayers = new createjs.Text("Number of players: " + 0, "20px Arial", "#000000");
    console.log(numberPlayers.getBounds().width);
    numberPlayers.x = window.innerWidth / 2 - numberPlayers.getBounds().width / 2;
    numberPlayers.y = numberPlayers.getBounds().height / 2;
}

function numberPUpdate(number) {
    numberPlayers.text = "Number of players: " + number;
}

function notif(msg) {
    let text = new createjs.Text(msg, "33px Arial", "#000000");
    text.x = window.innerWidth / 2 - text.getBounds().width / 2;
    text.y = 30;
    stage.addChild(text);
    window.setInterval(() => stage.removeChild(text), 1);
}
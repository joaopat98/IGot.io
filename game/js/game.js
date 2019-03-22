"use strict";

var queue, stage, arena, time, player;
var mapWidth = 3000, mapHeight = 3000;

function loadImages() {
	queue = new createjs.LoadQueue(false, null, true);
	queue.on("complete", init, this);
	queue.loadFile({src:"res/tile.png", crossOrigin:true, id:"tile"});
	queue.loadFile({src:"res/skin_warrior.png", crossOrigin:true, id:"warrior"});
	queue.loadFile({src:"res/laser.png", crossOrigin:true, id:"laser"});
}

function init() {
	stage = new createjs.Stage("canvas");
	player = new Character(0, 0, queue.getResult("warrior"), 726, 543, queue.getResult("laser"), 595, 64, true, mapWidth, mapHeight);
	arena = new Arena(queue.getResult("tile"), player, time, mapWidth, mapHeight);
	arena.x = window.innerWidth / 2;
	arena.y = window.innerHeight / 2;
	stage.addChild(arena);
	config();
	window.addEventListener("keydown", keyHandler);
	window.addEventListener("keyup", keyHandler);
}

function resize() {
	stage.canvas.width = window.innerWidth;
	stage.canvas.height = window.innerHeight;
}

function display(ev) {
	resize();
	player.move(ev.delta);
	
	arena.regX = Math.min(Math.max(- mapWidth/2 + stage.canvas.width/2, player.sprite.x), mapWidth/2 - stage.canvas.width/2);
	arena.regY = Math.min(Math.max(- mapHeight/2 + stage.canvas.height/2, player.sprite.y), mapHeight/2 - stage.canvas.height/2);
	
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
	if(player.shootOnce == false && ev.type === "keyup" && ev.keyCode == 32) {
		arena.player.shootOnce = true;
	}
}
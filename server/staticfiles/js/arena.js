"use strict";

class Arena extends createjs.Container {
	constructor(img, player, gameTime, width, height) {
		super();
		var worldShape = new createjs.Shape();
		worldShape.graphics.beginBitmapFill(img).drawRect(0, 0, width, height);       
		worldShape.x = -width/2;
		worldShape.y = -height/2;
		this.addChild(worldShape);
		this.player = player;
		this.chars = {};
		this.chars[player.id] = player;
		this.objects = new Array();
		this.gameTime = gameTime;
		this.addChild(player);
	}
}
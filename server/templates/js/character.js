"use strict";

class Character extends createjs.Container {
	constructor(x, y, sprite, spriteWidth, spriteHeight, laserSprite, laserWidth, laserHeight, isPlayer, mapWidth, mapHeight) {
		super();
		this.shootOnce = true;
		this.moveSpeed = 500;
		this.turnSpeed = 250;
		this.mapWidth = mapWidth;
		this.mapHeight = mapHeight;
		this.keys = new Array();
		this.isPlayer = isPlayer;
		var spritesheet = new createjs.SpriteSheet({
			images: [sprite],
			frames: {"width": spriteWidth, "height": spriteHeight, "regX": spriteWidth/2, "regY": spriteHeight/2},
		});
		this.sprite = new createjs.Sprite(spritesheet);
		this.sprite.scale = 0.15;
		this.width = 0.15 * spriteWidth;
		this.height = 0.15 * spriteHeight;
		this.sprite.x = x;
		this.sprite.y = y;
		this.sprite.rotation = 0;
		var laserSpriteSheet = new createjs.SpriteSheet({
			images: [laserSprite],
			frames: {"width": laserWidth, "height": laserHeight, "regX": -this.height, "regY": laserHeight/2},
			animations: {
				"idle":{
					frames: [0],
					next: "idle",
				},
				"shoot": {
					frames: [1, 2, 3, 4, 3, 2, 1],
					next: "idle",
					speed: .75,
				},
			}
		});
		this.laserSprite = new createjs.Sprite(laserSpriteSheet, "idle");
		this.laserSprite.scale = 0.50;
		this.laserSprite.x = this.sprite.x;
		this.laserSprite.y = this.sprite.y;
		this.laserSprite.rotation = 90;
	}

	move(delta) {
		let right = 68, left = 65, up = 87, down = 83, laserRight = 75, laserLeft = 74, spacebar = 32;
		let tx = 0, ty = 0;
		if(this.keys[right] || this.keys[left] || this.keys[up] || this.keys[down]) {
			//let r = this.sprite.rotation * (Math.PI / 180);
			//let cos = Math.cos(r), sin = Math.sin(r);
			if(this.keys[right]) {
				tx += 1;
			}
			if(this.keys[left]) {
				tx -= 1;
			}
			if(this.keys[down]) {
				ty += 1;
			}
			if(this.keys[up]) {
				ty -= 1;
			}

			let m = Math.sqrt(tx * tx + ty * ty);
			if(m > 1) {
				tx /= m;
				ty /= m;
			}
			if(tx != 0 || ty != 0) {
				let movementX = tx * this.moveSpeed * (delta/1000);
				let movementY = ty * this.moveSpeed * (delta/1000);
				if(this.sprite.x + movementX > - mapWidth/2 + this.width/2
				&& this.sprite.x + movementX < mapWidth/2 - this.width/2
				&& this.sprite.y + movementY > -mapHeight/2 + this.height/2
				&& this.sprite.y + movementY < mapHeight/2 - this.height/2) {
					this.sprite.x += movementX;
					this.sprite.y += movementY;
					this.laserSprite.x += movementX;
					this.laserSprite.y += movementY;
				}
				
				//this.sprite.x += (cos * tx + sin * ty) * this.moveSpeed * (delta / 1000);
				//this.sprite.y += (sin * tx - cos * ty) * this.moveSpeed * (delta / 1000);
			}
			
		}
		
		if(this.keys[laserLeft] || this.keys[laserRight]) {
			let tr = (this.keys[laserLeft] ? 1 : 0) + (this.keys[laserRight] ? -1 : 0);
			if(tr != 0) {
				this.sprite.rotation -= tr * this.turnSpeed * (delta / 1000);
				this.laserSprite.rotation -= tr * this.turnSpeed * (delta / 1000);
			}
		}
		
		if(this.keys[spacebar] && this.shootOnce) {
			this.shootOnce = false;
			this.laserSprite.gotoAndPlay("shoot");
		}
	}
}
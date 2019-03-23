"use strict";

class Character extends createjs.Container {
    constructor(x, y, sprite, charSize, laserSprite, laserWidth, laserHeight, isPlayer, mapWidth, mapHeight, id, speed) {
        super();
        this.id = id;
        this.player = 0;
        this.lives = 5;
        this.shootOnce = true;
        this.moveSpeed = speed;
        this.turnSpeed = 250;
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.keys = new Array();
        this.isPlayer = isPlayer;
        let scale = charSize / 512;
        let spritesheet = new createjs.SpriteSheet({
            images: [sprite],
            frames: {
                "width": sprite.width,
                "height": sprite.height,
                "regX": sprite.width / 2,
                "regY": sprite.height / 2
            },
        });
        this.sprite = new createjs.Sprite(spritesheet);
        this.addChild(this.sprite);
        this.sprite.scale = scale;
        this.width = scale * sprite.width;
        this.height = scale * sprite.height;
        this.x = x;
        this.y = y;
        this.rotation = 90;
        if (isPlayer) {
            let laserSpriteSheet = new createjs.SpriteSheet({
                images: [laserSprite],
                frames: {"width": laserWidth, "height": laserHeight, "regX": -this.height, "regY": laserHeight / 2},
                animations: {
                    "idle": {
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
            this.addChild(this.laserSprite);
        }
    }

    move(delta, ws) {
        let right = 68, left = 65, up = 87, down = 83, laserRight = 75, laserLeft = 74, spacebar = 32;
        let tx = 0, ty = 0;
        if (this.keys[right] || this.keys[left] || this.keys[up] || this.keys[down]) {
            //let r = this.sprite.rotation * (Math.PI / 180);
            //let cos = Math.cos(r), sin = Math.sin(r);
            if (this.keys[right]) {
                tx += 1;
            }
            if (this.keys[left]) {
                tx -= 1;
            }
            if (this.keys[down]) {
                ty += 1;
            }
            if (this.keys[up]) {
                ty -= 1;
            }

            let m = Math.sqrt(tx * tx + ty * ty);
            if (m > 1) {
                tx /= m;
                ty /= m;
            }
            if (tx != 0 || ty != 0) {
                let movementX = tx * this.moveSpeed * (delta / 1000);
                let movementY = ty * this.moveSpeed * (delta / 1000);
                ws.send(JSON.stringify({
                    action: "move",
                    deltaX: movementX,
                    deltaY: movementY
                }));

                //this.sprite.x += (cos * tx + sin * ty) * this.moveSpeed * (delta / 1000);
                //this.sprite.y += (sin * tx - cos * ty) * this.moveSpeed * (delta / 1000);
            }

        }

        if (this.keys[laserLeft] || this.keys[laserRight]) {
            let tr = (this.keys[laserLeft] ? 1 : 0) + (this.keys[laserRight] ? -1 : 0);
            if (tr != 0) {
                this.rotation -= tr * this.turnSpeed * (delta / 1000);
            }
        }

        if (this.keys[spacebar] && this.shootOnce) {
            this.shootOnce = false;
            this.laserSprite.gotoAndPlay("shoot");
            ws.send(JSON.stringify({
                action: "fire",
                rotation: this.rotation
            }));
        }
    }
}
class LeaderBoard extends createjs.Container {
    constructor(width, deltaY){
        super();
        let title = new createjs.Text("LeaderBoard", "33px Arial", "#000000");
        title.x = width / 2 - title.getBounds().width / 2;

        this.addChild(title);

        this.entries = [];
        let y = title.y + title.getBounds().height + deltaY;
        for (let i = 0; i < 10; i++) {
            let text = new createjs.Text(" ","26px Arial","#000000");
            text.y = y;
            y += text.getBounds().height + deltaY;
            this.entries.push(text);
            this.addChild(text);
        }
    }

    update(data){
        let i;
        for (i = 0; i < data.length; i++) {
            this.entries[i].text = (i+1) + ". " + data[i].name + " - " + data[i].score;
        }
        for (; i < 10; i++) {
            this.entries[i].text = "";
        }
    }
}
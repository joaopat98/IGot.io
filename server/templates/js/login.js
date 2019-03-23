window.onload = () => {
    let inputs = document.getElementsByTagName("input");
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].onchange = textChange;
    }
};

input = {};

let textChange = ev => {
    let trg = ev.currentTarget;
    input[trg.name] = trg.value;
};

let submit = () => {
    Request.post("api/login", input).then(response => {
        if (response.status !== 200) {
            response.json().then(errors => {

            });
        } else {
            window.location.assign(window.location.origin);
        }
    });
};

let main = () => {

};
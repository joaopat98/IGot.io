window.onload = () => {
    let inputs = document.getElementsByTagName("input");
    inputs.forEach(input => input.onchange = textChange);
};

input = {};

let textChange = ev => {
    let trg = ev.currentTarget;
    input[trg.name] = trg.value;
};

let submit = () => {
    console.log(input);
};

let main = () => {

};
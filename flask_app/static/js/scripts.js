// Calls all functions that need to be called onload.
// Calls this function onload on the body.
function loadFunction() {
    changeNumValue();
}

function changeNumValue() {
    range = document.getElementById('sentences');
    num = document.getElementById('num-display');
    num.value = range.value;
}
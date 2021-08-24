// Calls all functions that need to be called onload.
// Calls this function onload on the body.
function loadFunction() {
    subForm();
}

function subForm() {
    var myForm = document.getElementById('inp-form');
    var myButt = document.getElementById('tldr-butt');
    var myLoader = document.getElementById('loader');
    myForm.onsubmit = function(e) {
        e.preventDefault();
        myButt.style.display = 'none'
        myLoader.style.display = 'block'
        var form = new FormData(myForm);
        fetch('http://localhost:5000/summarize', {method: 'POST', body: form})
            .then(response => response.json())
            .then(data => showSummary(data))

    }
}

function showSummary(data) {
    var ul = document.getElementById('output-ul');
    while (ul.firstChild) {
        ul.removeChild(ul.firstChild);
    }
    h2 = document.createElement('h2');
    h2.innerHTML = 'Notes';
    ul.appendChild(h2);
    for (var i = 0; i < data.length; i++) {
        for (var j = 0; j < data[i].length; j++) {
            if (data[i][j].length >= 10) {
                li = document.createElement('li');
            li.innerHTML = data[i][j];
            ul.appendChild(li);
            }
        }
    }
    document.getElementById('tldr-butt').style.display = 'block';
    document.getElementById('loader').style.display = 'none';
}
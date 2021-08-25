// Calls all functions that need to be called onload.
// Calls this function onload on the body.
function loadFunction() {
    subForm();
    saveNotebook();
    deleteNotebook();
    saveToNotebook();
}

function subForm() {
    var myForm = document.getElementById('inp-form');
    var myButt = document.getElementById('tldr-butt');
    var myLoader = document.getElementById('loader');
    myForm.onsubmit = function(e) {
        e.preventDefault();
        myButt.style.display = 'none';
        myLoader.style.display = 'block';
        var form = new FormData(myForm);
        fetch('http://localhost:5000/summarize', {method: 'POST', body: form})
            .then(response => response.json())
            .then(data => showSummary(data))

    }
}

function saveToNotebook() {
    var myForm = document.getElementById('save-to-notebook');
    myForm.onsubmit = function(e) {
        e.preventDefault();
        getAllBullets();
    }
}

function showSummary(data) {
    var ul = document.getElementById('output-ul');
    while (ul.firstChild) {
        ul.removeChild(ul.firstChild);
    }
    var h2 = document.createElement('h2');
    h2.innerHTML = 'Notes';
    ul.appendChild(h2);
    for (var i = 0; i < data.length; i++) {
        for (var j = 0; j < data[i].length; j++) {
            if (data[i][j].length >= 10) {
                var li = document.createElement('li');
            li.innerHTML = data[i][j];
            ul.appendChild(li);
            }
        }
    }
    document.getElementById('tldr-butt').style.display = 'block';
    document.getElementById('loader').style.display = 'none';
}

function getAllBullets() {
    var ul = document.getElementById('output-ul');
    var bullets = [];
    for (var i = 1; i < ul.children.length; i++) {
        bullets.push(ul.children[i].innerHTML);
    }
    select = document.getElementById('notebook-select');
    jsonToPost = JSON.stringify([{'bullets': bullets, 'notebook_name': select[select.selectedIndex].value}]);
    fetch('http://localhost:5000/notebooks/save', {method: 'POST', body: jsonToPost})
        .then(response => response.json())
        .then(data => data == 'success' ? showSnackbar() : console.log('Error Saving')) // Change the console log to give user a more helpful error messsage.
}

function showSnackbar() {
    console.log('here')
    var snackbar = document.getElementById('snackbar');
    snackbar.className = 'show';
    setTimeout(function() { snackbar.className = snackbar.className.replace('show', '');}, 3000);
}

function registerButton() {
    localStorage.setItem('whichOne', 'register');
}

function loginButton() {
    localStorage.setItem('whichOne', 'login');
}

function showSave() {
    var saveDiv = document.getElementById('notebook-pop');
    saveDiv.style.display = 'block';
}

function closeSave() {
    var saveDiv = document.getElementById('notebook-pop');
    saveDiv.style.display = 'none';
}

function saveNotebook() {
    var myForm = document.getElementById('save-form');
    myForm.onsubmit = function(e) {
        e.preventDefault();
        var form = new FormData(myForm);
        fetch('http://localhost:5000/notebooks/add', {method: 'POST', body: form})
            .then(response => response.json())
            .then(data => addToSelect(data))
    }
}

function deleteNotebook() {
    var myForm = document.getElementById('delete-form');
    var mySelect = document.getElementById('notebook-select');
    myForm.onsubmit = function(e) {
        if (!confirm('Delete ' + mySelect.options[mySelect.selectedIndex].text + '?\n\nThis action is irreversible.')) {
            return;
        } else {
            var form = new FormData(myForm);
            fetch('http://localhost:5000/notebooks/delete', {method: 'POST', body: form})
                .then(response => response.json())
                .then(data => addToSelect(data))
        }
    }
}


function addToSelect(data) {
    var mySelect = document.getElementById('notebook-select');
    while (mySelect.firstChild) {
        mySelect.removeChild(mySelect.firstChild);
    }
    
    for (var i = 0; i < data.length; i++) {
        var option = document.createElement('option');
        option.value = data[i];
        option.innerHTML = data[i];
        mySelect.appendChild(option);
    }
    mySelect.selectedIndex = data.length-1;
}
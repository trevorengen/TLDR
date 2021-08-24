function showRegistration() {
    loginForm = document.getElementById('login-form');
    loginForm.setAttribute('style', 'display: none;');
    registerForm = document.getElementById('register-form');
    registerForm.setAttribute('style', 'display: block;');
    localStorage.setItem('whichOne', 'register');
}

function showLogin() {
    loginForm = document.getElementById('login-form');
    loginForm.setAttribute('style', 'display: block;');
    registerForm = document.getElementById('register-form');
    registerForm.setAttribute('style', 'display: none;');
    localStorage.setItem('whichOne', 'login');
}

function whichToShow() {
    if (localStorage.getItem('whichOne') == 'register') {
        showRegistration();
    } else {
        showLogin();
    }
}

function onLoad() {
    let loginForm = document.getElementById('login-form');
    loginForm.onsubmit = function(e) {
        e.preventDefault();
        var form = new FormData(loginForm)
        // little test
        fetch('https://trevorengen.com/login', {method: 'POST', body: form})
            .then(response => response.json())
            .then(data => (data != 'connect') ? applyLoginFlash(data) : location.reload())
    }

    let registerForm = document.getElementById('register-form');
    registerForm.onsubmit = function(e) {
        e.preventDefault();
        var form = new FormData(registerForm);
        fetch('https://trevorengen.com/register', {method: 'POST', body: form})
            .then(response => response.json())
            .then(data => (data != 'connect') ? applyRegisterFlash(data) : location.reload())
    }
}

function hideToast() {
    toast = document.getElementById("this-toast")
    toast.setAttribute('style', 'display: none;')
}

/*  
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    VALIDATION STILL HAPPENS ON THE BACK END THIS
    IS JUST SO THAT THE FORM IS RESPONSIVE AND
    IT IS EASIER TO USE!!!
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

function activeRegister(elem) {
    if (elem.name == 'first_name') {
        if (elem.value.length < 3) {
            elem.className = 'form-control my-1 is-invalid';
        } else {
            elem.className = 'form-control my-1 is-valid';
            if (document.getElementById('last-name').className == 'form-control my-1 is-valid') {
                flash = document.getElementById('register-head-flash');
                flash.setAttribute('style', 'display: none;');
            }
        }
    } else if (elem.name == 'last_name') {
        if (elem.value.length < 3) {
            elem.className = 'form-control my-1 is-invalid';
        } else {
            elem.className = 'form-control my-1 is-valid';
            elem.className = 'form-control my-1 is-valid';
            if (document.getElementById('first-name').className == 'form-control my-1 is-valid') {
                flash = document.getElementById('register-head-flash');
                flash.setAttribute('style', 'display: none;');
            }
        }
    } else if (elem.name == 'email') {
        let re = new RegExp('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)');
        if (!re.test(elem.value)) {
            elem.className = 'form-control my-2 is-invalid';
        } else {
            elem.className = 'form-control my-2 is-valid';
            flash = document.getElementById('register-email-flash');
            flash.setAttribute('style', 'display: none;');
        }
    } else if (elem.name == 'password') {
        let caps = new RegExp('[A-Z]');
        let nums = new RegExp('[0-9]');
        if (elem.value.length < 6 || !caps.test(elem.value) || !nums.test(elem.value)) {
            elem.className = 'form-control my-2 is-invalid';
            if (elem.value.length < 6) {
                flash = document.getElementById('register-password-flash');
                flash.setAttribute('style', 'display: block;');
                flash.innerHTML = 'Password must be at least 6 characters.';
                flash.setAttribute('style', 'margin: 0;');
            } else {
                flash = document.getElementById('register-password-flash');
                flash.setAttribute('style', 'display: block;');
                flash.innerHTML = 'Password must contain at least one capital letter AND one number.';
                flash.setAttribute('style', 'margin: 0;');
            }
        } else {
            elem.className = 'form-control my-2 is-valid';
            flash = document.getElementById('register-password-flash');
            flash.setAttribute('style', 'display: none;');
        }
    } else if (elem.name == 'confirm-password') {
        if (elem.value != document.getElementById('password').value) {
            elem.className = 'form-control my-2 is-invalid';
            flash = document.getElementById('register-confirm-password-flash');
            flash.setAttribute('style', 'display: block;');
            flash.innerHTML = 'Passwords don\'t match.';
            flash.setAttribute('style', 'margin: 0;');
        } else {
            elem.className = 'form-control my-2 is-valid';
            flash = document.getElementById('register-confirm-password-flash');
            flash.setAttribute('style', 'display: none;');
        }
    }
}

function applyRegisterFlash(data) {
    if (data.includes('First and last name must be at least 3 characters.')) {
        flash = document.getElementById('register-head-flash');
        flash.setAttribute('style', 'display: block;');
        flash.innerHTML = 'First and last name must be at least 3 characters.';
        flash.setAttribute('style', 'margin: 0;');
        if (document.getElementById('first-name').value.length < 3) {
            document.getElementById('first-name').className += ' is-invalid';
        }
        if (document.getElementById('last-name').value.length < 3) {
            document.getElementById('last-name').className += ' is-invalid';
        }
    } else {
        flash = document.getElementById('register-head-flash');
        flash.setAttribute('style', 'display: none;');
        document.getElementById('first-name').className = 'form-control my-1 is-valid';
        document.getElementById('last-name').className = 'form-control my-1 is-valid';
    }
    
    if (data.includes('Invalid email address.')) {
        flash = document.getElementById('register-email-flash');
        flash.setAttribute('style', 'display: block;');
        flash.innerHTML = 'Invalid email address.';
        flash.setAttribute('style', 'margin: 0;');
        emailInput = document.getElementById('email');
        emailInput.className += ' is-invalid';

        emailInput.setAttribute('style', 'margin-top: 0;');
    } else if (data.includes('Email already exists, please login.'))  {
        flash = document.getElementById('register-email-flash');
        flash.setAttribute('style', 'display: block;');
        flash.innerHTML = 'Email already exists, please login.';
        flash.setAttribute('style', 'margin: 0;');
        emailInput = document.getElementById('email');
        emailInput.className += ' is-invalid';
        emailInput.setAttribute('style', 'margin-top: 0;');
    } else {
        flash = document.getElementById('register-email-flash');
        flash.setAttribute('style', 'display: none;');
        document.getElementById('email').className = 'form-control my-2 is-valid';
    }
    
    if (data.includes('Password must be at least 6 characters.')) {
        flash = document.getElementById('register-password-flash');
        flash.setAttribute('style', 'display: block;');
        flash.innerHTML = 'Password must be at least 6 characters.';
        flash.setAttribute('style', 'margin: 0;');
        password = document.getElementById('password');
        password.className += ' is-invalid';
        password.setAttribute('style', 'margin-top: 0;');
        password = document.getElementById('confirm-password');
        password.className += ' is-invalid';
        password.setAttribute('style', 'margin-top: 0;');
        flash = document.getElementById('register-confirm-password-flash');
        flash.setAttribute('style', 'display: none;');
    } else if (data.includes('Password must contain at least one capital letter AND one number.')) {
        flash = document.getElementById('register-password-flash');
        flash.setAttribute('style', 'display: block;');
        flash.innerHTML = 'Password must contain at least one capital letter AND one number.';
        flash.setAttribute('style', 'margin: 0;');
        password = document.getElementById('password');
        password.className += ' is-invalid';
        password.setAttribute('style', 'margin-top: 0;');
        password = document.getElementById('confirm-password');
        password.className += ' is-invalid';
        password.setAttribute('style', 'margin-top: 0;');
        flash = document.getElementById('register-confirm-password-flash');
        flash.setAttribute('style', 'display: none;');
    } else if (data.includes('Passwords don\'t match.')) {
        flash = document.getElementById('register-confirm-password-flash');
        flash.setAttribute('style', 'display: block;');
        flash.innerHTML = 'Passwords don\'t match.';
        flash.setAttribute('style', 'margin: 0;');
        password.setAttribute('style', 'margin-top: 0;');
        password = document.getElementById('confirm-password');
        password.className += ' is-invalid';
        flash = document.getElementById('register-password-flash');
        flash.setAttribute('style', 'display: none;');
        document.getElementById('password').className = 'form-control my-2 is-valid';
    } else {
        flash = document.getElementById('register-password-flash');
        flash.setAttribute('style', 'display: none;');
        document.getElementById('password').className = 'form-control my-2 is-valid';
        flash = document.getElementById('register-confirm-password-flash');
        flash.setAttribute('style', 'display: none;');
        document.getElementById('confirm-password').className = 'form-control my-2 is-valid';
    }
    
}

function applyLoginFlash(data) {
    console.log(data);
    if (data.length > 0) {
        emailInput = document.getElementById('login-email');
        passwordInput = document.getElementById('login-password');
        flashP = document.getElementById('login-flash');
        header = document.getElementById('title-login');
        emailInput.className += ' is-invalid';
        passwordInput.className += ' is-invalid';
        flashP.innerHTML = '';
        flashP.setAttribute('style', 'display: block;');
        for (var i = 0; i < data.length; i++) {
            flashP.innerHTML += data[i];
        }
        flashP.setAttribute('style', 'margin-bottom: 0;');
    }
}
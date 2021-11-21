function register_handler() {
    var username_validation_result = username_validation(document.getElementById('username').value);
    var email_validation_result = email_validation(document.getElementById('email').value);
    var password_validation_result = password_validation(document.getElementById('password').value);
    var cfm_password_validation_result = confirm_password_validation(document.getElementById('password').value, document.getElementById('cfm_password').value);
    var recaptcha_validation_result = recaptcha_validation();

    const form = document.getElementById('register_form')
    const error = document.getElementById('error-alert')

    if (username_validation_result && email_validation_result && password_validation_result && cfm_password_validation_result && recaptcha_validation_result) {
        form.submit();
    }
    else {
        if (error.classList.contains("alert-danger")) {
            error.classList.remove("alert-danger");
        }
        if (error.classList.contains("alert-success")) {
            error.classList.remove("alert-success");
        }
        error.innerHTML = "";
        error.classList.add("alert-danger");
        error.style.display = null;
    }

    if (!username_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure that username is not more than 45 characters and no special character is allowed</b>";
        error.append(p);
    }

    if (!email_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure that email is in the correct format</b>";
        error.append(p);
    }

    if (!password_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure that password is in the correct format</b> <br/> 1) Password must have a minimum length of 8 <br /> 2) Password must contain 1 upper case <br /> 3) Password must contain 1 special character";
        error.append(p);
    }

    if (!cfm_password_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Confirm password does not match with password</b>";
        error.append(p);
    }

    if (!recaptcha_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure that recaptcha have been checked</b>";
        error.append(p);
    }
}
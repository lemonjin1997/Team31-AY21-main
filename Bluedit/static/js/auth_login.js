function login_handler() {
    var email_validation_result = email_validation(document.getElementById('email').value);
    var password_validation_result = auth_password_validation(document.getElementById('password').value);

    const error = document.getElementById('error-alert');
    const form = document.getElementById('login_form');

    if (email_validation_result && password_validation_result) {
        form.submit();
    } else {
        if (error.classList.contains("alert-danger")) {
            error.classList.remove("alert-danger");
        }
        if (error.classList.contains("alert-success")) {
            error.classList.remove("alert-success");
        }
        error.style.display = null;
        error.classList.add("alert-danger");
        error.innerHTML = "Authentication error";
    }
}
function forget_handler() {
    var recaptcha_validation_result = recaptcha_validation();
    var email_validation_result = email_validation(document.getElementById('email').value);

    const form = document.getElementById('forget_form');
    const error = document.getElementById('error-alert');

    if (recaptcha_validation_result && email_validation_result) {
        form.submit();
    } else {
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

    if (!email_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure that email is in the correct format</b>";
        error.append(p);
    }

    if (!recaptcha_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure that recaptcha have been checked</b>";
        error.append(p);
    }
}
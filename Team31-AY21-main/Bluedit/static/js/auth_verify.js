function verify_handler() {
    var recaptcha_validation_result = recaptcha_validation();

    const form = document.getElementById('verify_form');
    const error = document.getElementById('error-alert')

    if (recaptcha_validation_result) {
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
        error.innerHTML = "- <b>Please ensure that recaptcha have been checked</b>";
    }
}
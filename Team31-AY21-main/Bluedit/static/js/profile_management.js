function change_username_handler() {
    var username_validation_result = username_validation(document.getElementById('username').value);

    const form = document.getElementById('username_change_form');
    const error = document.getElementById('error-alert');

    if (username_validation_result) {
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

        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure that username is not more than 45 characters and no special character is allowed</b>";
        error.append(p);
    }
}

function change_email_handler() {
    var old_email_validation_result = email_validation(document.getElementById('current-email').value);
    var new_email_validation_result = email_validation(document.getElementById('new-email').value);

    const form = document.getElementById('email_change_form');
    const error = document.getElementById('error-alert');

    if (old_email_validation_result && new_email_validation_result) {
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

    if (!old_email_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Current email not in the correct format. Please verify it</b>";
        error.append(p);
    }

    if (!new_email_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>New email not in the correct format. Please verify it</b>";
        error.append(p);
    }
}

function change_password_handler() {
    var cur_password_validation_result = auth_password_validation(document.getElementById('current-pw').value);
    var new_password_validation_result = password_validation(document.getElementById('new-password').value);
    var cfm_password_validation_result = confirm_password_validation(document.getElementById('new-password').value, document.getElementById('cfm-password').value);

    const form = document.getElementById('password_change_form');
    const error = document.getElementById('error-alert');

    if (cur_password_validation_result && new_password_validation_result && cfm_password_validation_result) {
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

    if (!cur_password_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please enter your current password or ensure that it is below 255 in length</b>";
        error.append(p);
    }

    if (!new_password_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>New password does not meet the accepted requirements</b>";
        error.append(p);
    }

    if (!cfm_password_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Confirm password does not match your new password</b>";
        error.append(p);
    }
}

function delete_handler() {
    var input = document.getElementById('delete-txt').value;
    const challenge = "I wish to delete my account now";

    const form = document.getElementById('delete_form');
    const error = document.getElementById('error-alert');

    if (input != challenge) {
        if (error.classList.contains("alert-danger")) {
            error.classList.remove("alert-danger");
        }
        if (error.classList.contains("alert-success")) {
            error.classList.remove("alert-success");
        }
        error.innerHTML = "";
        error.classList.add("alert-danger");
        error.style.display = null;

        let p = document.createElement("p");
        p.innerHTML = "- <b>Delete failed as input text does not match the challenge text</b>";
        error.append(p);
    }
    else {
        form.submit();
    }
}

function toggle_handler() {
    if (tfa == 1) {
        tfa = 0;
    } else {
        tfa = 1;
    }

    target = document.getElementById('tfa');
    target.value = tfa;
    console.log(target.value);
    $('#tfa_modal').modal({backdrop: 'static', keyboard: false});
}

function refresh_page() {
    window.location.reload();
}
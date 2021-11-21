function comment_form_handler() {
    var comment_validation_result = post_content_validation(document.getElementById('content').value);

    const form = document.getElementById('comment_form');
    const error = document.getElementById('error-alert');

    if (comment_validation_result) {
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
        p.innerHTML = "- <b>Validation failed. Please input something into the comment before submitting</b>";
        error.append(p);
    }
}
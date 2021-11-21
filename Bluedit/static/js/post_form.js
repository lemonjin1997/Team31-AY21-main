var input = document.getElementById( 'image' );
var infoArea = document.getElementById( 'image_label' );

input.addEventListener( 'change', showFileName );
function showFileName( event ) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}

function post_form_handler() {
    var category_validation_result = category_validation(document.getElementById('categories').value);
    var post_title_validation_result = post_title_validation(document.getElementById('title').value);
    var post_content_validation_result = post_content_validation(document.getElementById('content').value);

    const error = document.getElementById("error-alert");
    const form = document.getElementById("post_form");

    if (category_validation_result && post_title_validation_result && post_content_validation_result) {
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

    if (!post_title_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure post title is not empty and does not contain any special characters</b>";
        error.append(p);
    }

    if (!post_content_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure post content is not empty</b>";
        error.append(p);
    }

    if (!category_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = '- <b>Please ensure category contains no special character other than " " and "&#59;"</b>';
        error.append(p);
    }
}

function edit_post_handler() {
    var post_title_validation_result = post_title_validation(document.getElementById('title').value);
    var post_content_validation_result = post_content_validation(document.getElementById('content').value);

    const error = document.getElementById("error-alert");
    const form = document.getElementById("edit_post_form");

    if (post_title_validation_result && post_content_validation_result) {
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

    if (!post_title_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure post title is not empty and does not contain any special characters</b>";
        error.append(p);
    }

    if (!post_content_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure post content is not empty</b>";
        error.append(p);
    }
}

function edit_reply_handler() {
    var post_content_validation_result = post_content_validation(document.getElementById('content').value);

    const error = document.getElementById("error-alert");
    const form = document.getElementById("edit_reply_form");

    if (post_content_validation_result) {
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

    if (!post_content_validation_result) {
        let p = document.createElement("p");
        p.innerHTML = "- <b>Please ensure reply content is not empty</b>";
        error.append(p);
    }
}
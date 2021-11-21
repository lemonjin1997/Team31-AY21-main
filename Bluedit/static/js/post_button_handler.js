function like(target_elem, id, token) {
    const arr = target_elem.innerHTML.split(" ");
    var val = parseInt(arr[1], 10);

    $.ajax({
        url: "/post_like/" + id,
        type: 'POST',
        headers: {
                        'X-CSRFToken': token
                   },
        dataType: 'json', // added data type
        success: function(res) {
            if (res == 1) {
                if (target_elem.classList.contains("badge-secondary")) {
                    target_elem.classList.remove("badge-secondary");
                    target_elem.classList.add("badge-success");
                    target_elem.innerHTML = "Likes: " + (val + 1);
                } else {
                    target_elem.classList.remove("badge-success");
                    target_elem.classList.add("badge-secondary");
                    target_elem.innerHTML = "Likes: " + (val - 1);
                }
            }
            else if (res == -2) {
                window.location.replace("/auth/login");
            }
            else if (res == -3) {
                console.log("validation error");
            }
            else {
                console.log("internal service error");
            }
        },
        error: function(res) {
            console.log(res);
        }
    });
}

function save(target_elem, id, token) {
    const arr = target_elem.innerHTML.split(" ");
    var val = parseInt(arr[1], 10);

    $.ajax({
        url: "/post_save/" + id,
        type: 'POST',
        headers: {
                        'X-CSRFToken': token
                   },
        dataType: 'json', // added data type
        success: function(res) {
            if (res == 1) {
                if (target_elem.classList.contains("badge-secondary")) {
                    target_elem.classList.remove("badge-secondary");
                    target_elem.classList.add("badge-success");
                    target_elem.innerHTML = "Saves: " + (val + 1);
                } else {
                    target_elem.classList.remove("badge-success");
                    target_elem.classList.add("badge-secondary");
                    target_elem.innerHTML = "Saves: " + (val - 1);
                }
            }
            else if (res == -2) {
                window.location.replace("/auth/login");
            }
            else if (res == -3) {
                console.log("validation error");
            }
            else {
                console.log("internal service error");
            }
        },
        error: function(res) {
            console.log(res);
        }
    });
}

function reply_like(target_elem, id, token) {
    const arr = target_elem.innerHTML.split(" ");
    var val = parseInt(arr[1], 10);

    $.ajax({
        url: "/reply_like/" + id,
        type: 'POST',
        headers: {
                        'X-CSRFToken': token
                   },
        dataType: 'json', // added data type
        success: function(res) {
            if (res == 1) {
                if (target_elem.classList.contains("badge-secondary")) {
                    target_elem.classList.remove("badge-secondary");
                    target_elem.classList.add("badge-success");
                    target_elem.innerHTML = "Likes: " + (val + 1);
                } else {
                    target_elem.classList.remove("badge-success");
                    target_elem.classList.add("badge-secondary");
                    target_elem.innerHTML = "Likes: " + (val - 1);
                }
            }
            else if (res == -2) {
                window.location.replace("/auth/login");
            }
            else if (res == -3) {
                console.log("validation error");
            }
            else {
                console.log("internal service error");
            }
        },
        error: function(res) {
            console.log(res);
        }
    });
}

function report_post_handler(id) {
    const form = document.getElementById('report_post_' + id);
    form.submit();
}

function report_reply_handler(id) {
    const form = document.getElementById('report_reply_' + id);
    form.submit();
}


function delete_post(id) {
    const form = document.getElementById('delete_form_' + id);
    form.submit();
}

function delete_reply(id) {
    const form = document.getElementById('delete_form_reply_' + id);
    form.submit();
}

function edit_post(id) {
    window.location.href = "/post_edit/" + id;
}

function edit_reply(id) {
    window.location.href = "/reply_edit/" + id;
}

function post_view(id) {
    window.location.href = "/post/" + id;
}
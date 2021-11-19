function promote_handler(id) {
    const form = document.getElementById('promote_form_' + id);

    form.submit();
}

function delete_handler(id) {
    const form = document.getElementById('delete_form_' + id);

    form.submit();
}

function delete_reply_handler(id) {
    const form = document.getElementById('delete_reply_form_' + id);

    form.submit();
}

function ban_handler(id) {
    const form = document.getElementById('ban_form_' + id);

    form.submit();
}

function lock_handler(id) {
    const form = document.getElementById('lock_form_' + id);

    form.submit();
}
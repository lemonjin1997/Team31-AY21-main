var sentinel = document.querySelector('#sentinel');
var counter = 0;
var old_value = 0;

function target_handler(value, text) {
    document.getElementById('drop_down_btn').innerHTML = text;
    document.getElementById('drop_down_btn').value = value;
    document.getElementById('category').value = value;
}

function sort_handler() {
    target = document.getElementById('sort');
    form = document.getElementById('sort_form');

    form.submit();
}



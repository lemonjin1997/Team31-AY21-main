function email_validation(email) {
    const regex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    if (regex.test(email) && email.length <= 255 && email.length >= 1) {
        return true;
    } else {
        return false;
    }
}

function password_validation(password) {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&.]{8,}$/;

    if (regex.test(password) && password.length >=8 && password.length <= 255) {
        return true;
    } else {
        return false;
    }
}

function auth_password_validation(password) {
    if (password.length >=0 && password.length <= 255) {
        return true;
    } else {
        return false;
    }
}

function confirm_password_validation(main_pw, sub_pw) {
    if (main_pw.length >= 8 && main_pw.length <= 255 && sub_pw.length >= 8 && sub_pw.length <= 255) {
        if (main_pw == sub_pw) {
            return true;
        }

        return false;
    } else {
        return false;
    }
}

function username_validation(username) {
    const regex = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;

    if (!regex.test(username) && username.length >= 1 && username.length <= 45) {
        return true;
    } else {
        return false;
    }
}

function recaptcha_validation() {
    var response = grecaptcha.getResponse();

    if(response.length != 0){
        return true;
    } else{
        return false
    }
}

function category_validation(category) {
    const regex = /[`!@#$%^&*()_+\-=\[\]{}':"\\|,.<>\/?~]/;

    if (category.length >= 1) {
        if (!regex.test(category) && category.length >= 1 && category.length <= 255) {
            return true;
        } else {
            return false;
        }
    } else {
        return true;
    }
}

function post_title_validation(postTitle) {
    const regex = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;

    if (!regex.test(postTitle) && postTitle.length >= 1 && postTitle.length <= 255) {
        return true;
    } else {
        return false;
    }
}

function post_content_validation(postContent) {
    if (postContent.length >= 1) {
        return true;
    } else {
        return false;
    }
}
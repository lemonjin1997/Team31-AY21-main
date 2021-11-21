import re

from config import Config


class Sanitizer(object):
    # check string for any special character
    def validate_input_NoSpecialCharacters(self, inputs):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:\';]')

        if 0 < len(inputs) <= 45:
            if regex.search(inputs) is None:
                return True
            else:
                return False
        else:
            return False

    # check string for match against the email format
    def validate_email_MatchFormat(self, inputs):
        regex = re.compile(
            '^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')

        if 0 < len(inputs) <= 255:
            if re.match(regex, str(inputs)):
                return True
            else:
                return False
        else:
            return False

    # check password for match against regex
    def validate_password_MatchFormat(self, inputs):
        regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&.]{8,}$')

        if 8 <= len(inputs) <= 255:
            if re.match(regex, str(inputs)):
                return True
            else:
                return False
        else:
            return False

    def validate_text_replaceSymbol(self, inputs):
        translation = {
            "!": "&#33;",
            "\"": "&#34;",
            "#": "&#35;",
            "$": "&#36;",
            "%": "&#37;",
            "&": "&#38;",
            "\'": "&#39;",
            "(": "&#40;",
            ")": "&#41;",
            "*": "&#42;",
            "+": "&#43;",
            ",": "&#44;",
            "-": "&#45;",
            ".": "&#46;",
            "/": "&#47;",
            ":": "&#58;",
            ";": "&#59;",
            "<": "&#60;",
            "=": "&#61;",
            ">": "&#62;",
            "?": "&#63;",
            "[": "&#91;",
            "\\": "&#92;",
            "]": "&#93;",
            "^": "&#94;",
            "_": "&#95;",
            "`": "&#96;",
            "{": "&#123;",
            "|": "&#124;",
            "}": "&#125;",
            "~": "&#126;"
        }

        table = inputs.maketrans(translation)
        return inputs.translate(table)

    # check string for any special character
    def validate_post_title(self, inputs):
        # allow spacing
        regex = re.compile('[`!@#$%^&*()_+\-=\[\]{};\':\"\\|,.<>\/?~]')

        if 0 < len(inputs) <= 255:
            if regex.search(inputs) is None:
                return True
            else:
                return False
        else:
            return False

    # check string for any special character
    def validate_post_category(self, inputs):
        # allow spacing and ;
        regex = re.compile('[`!@#$%^&*()_+\-=\[\]{}\':\"\\|,.<>\/?~]')

        if 0 < len(inputs) <= 255:
            if regex.search(inputs) is None:
                return True
            else:
                return False
        else:
            return False

    def validate_filename_not_empty(self, filename):
        if filename == "" or len(filename) <= 0:
            return False

        return True

    def validate_filename_valid(self, filename):
        if not "." in filename:
            return False
        elif len(filename) > 150:
            return False

        return True

    def validate_file_extension(self, filename):
        # Split the extension from the filename
        ext = filename.rsplit(".", 1)[1]

        if ext.upper() in Config.ALLOWED_IMAGE_EXTENSIONS:
            return True
        else:
            return False

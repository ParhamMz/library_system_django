function toggleVisibility() {
    var x = document.getElementById("id_password");
    var y = document.getElementById("id_confirm_password");
    if (x.type === "password") {
        x.type = "text";
        y.type = "text";
    } else {
        x.type = "password";
        y.type = "password";
    }
}

if (document.getElementById("id_password")) {
    $('#id_password, #id_confirm_password').on('keyup', function () {
        if ($('#id_password').val().length < 8) {
            $('#id_password').css('borderColor', '#dc3545');
            $('#id_password').css('borderWidth', '2px');
        }
        else if ($('#id_password').val() === $('#id_confirm_password').val()) {
            $('#id_confirm_password').css('borderColor', '#198754');
            $('#id_confirm_password').css('borderWidth', '2px');
        } else {
            $('#id_confirm_password').css('borderColor', '#dc3545');
            $('#id_confirm_password').css('borderWidth', '2px');
        }
        if ($('#id_password').val().length >= 8) {
            $('#id_password').css('borderColor', '#ced4da');
            $('#id_password').css('borderWidth', '1px');
        }
    });
}
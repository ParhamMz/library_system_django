
if (document.getElementById("id_birth_date")) {
    var my_date = document.getElementById("id_birth_date");
    my_date.setAttribute("placeholder", "1401-01-01");
    my_date.style.textAlign = 'center'
}

$(document).ready(function () {
    $(".only-number-input").keydown(function (event) {
        // Allow: backspace, delete, tab, escape, and enter
        if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
            // Allow: Ctrl+A
            (event.keyCode == 65 && event.ctrlKey === true) ||
            // Allow: home, end, left, right
            (event.keyCode >= 35 && event.keyCode <= 39)) {
            // let it happen, don't do anything
            return;
        } else {
            // Ensure that it is a number and stop the keypress
            if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105)) {
                swal({
                    title: ".فقط وارد کردن اعداد مجاز است",
                    button: "بستن",
                });
                event.preventDefault();
            }
        }
    });
});

$(".only-english").keypress(function (event) {
    var ew = event.which;
    console.log(ew);
    if (48 <= ew && ew <= 57)
        return true;
    if (65 <= ew && ew <= 90)
        return true;
    if (97 <= ew && ew <= 122)
        return true;
    if (ew === 95 || ew === 46)
        return true;
    swal({
        title: "فقط وارد کردن حروف انگلیسی، اعداد، '_' و '.' مجاز است",
        button: "بستن",
    });
    return false;
});


$(document).ready(function () {
    $(".only-persian").keydown(function (event) {
        var p = /^[\u0600-\u06FF\s]+$/;

        // Allow: backspace, delete, tab, escape, and enter
        if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
            // Allow: Ctrl+A
            (event.keyCode == 65 && event.ctrlKey === true) ||
            // Allow: home, end, left, right
            (event.keyCode >= 35 && event.keyCode <= 39) || p.test(event.key)) {
            // let it happen, don't do anything
            return;
        } else {
            // Ensure that it is a number and stop the keypress
            swal({
                title: ".فقط وارد کردن حروف فارسی مجاز است",
                button: "بستن",
            });
            event.preventDefault();

        }
    });
});


function toggleVisibility() {
    var x = document.getElementById("id_password1");
    var y = document.getElementById("id_password2");
    if (x.type === "password") {
        x.type = "text";
        y.type = "text";
    } else {
        x.type = "password";
        y.type = "password";
    }
}

if (document.getElementById("id_password1")) {
    $('#id_password1, #id_password2').on('keyup', function () {
        if ($('#id_password1').val() === $('#id_password2').val()) {
            $('#id_password2').css('borderColor', '#198754');
            $('#id_password2').css('borderWidth', '2px');
        } else
            $('#id_password2').css('borderColor', '#dc3545');
            $('#id_password2').css('borderWidth', '2px');
    });
}


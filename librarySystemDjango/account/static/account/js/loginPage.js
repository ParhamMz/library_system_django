function toggleVisibility() {
    var x = document.getElementById("login-pass-inp");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
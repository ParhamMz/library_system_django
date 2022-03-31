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
                event.preventDefault();
            }
        }
    });
});

// function startTimer(e) {
//     e.preventDefault();
//     if (document.getElementById("card-num-inp").value.length === 16) {
//         theBTN = document.getElementById('payBTN');
//         theBTN.type = 'submit';
//         theBTN.onclick = "";
//         var count = 10;
//         var counter = setInterval(timer, 1000);
//         function timer() {
//             count = count - 1
//             if (count <= 0) {
//                 clearInterval(counter);
//                 window.location.href = "/accounts/myprofile/";
//             }
//             document.getElementById("redirectTimer").innerHTML = " در حال انتقال به پروفایل در " + count + " ثانیه...";


//         }
//     }
// }

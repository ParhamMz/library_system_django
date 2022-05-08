/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    var mybtn = document.querySelector('.side-navbar-btn');
    mybtn.setAttribute('onclick', 'closeNav()');
    var is_phone = window.matchMedia("(max-width: 600px)");
    if(is_phone.matches){
        document.getElementById("mySidenav").style.width = "200px";
    }
    document.getElementById("mySidenav").style.width = "300px";
    if (!is_phone.matches) {
        document.getElementById("user-profile-sidenav").style.marginRight = "300px";
    }
    document.getElementById("btn-container").style.display = "none";
    if (document.getElementById('search-form-of-users')){
        document.getElementById('search-form-of-users').style.width = "71%";
    }
    if (document.getElementById('my-countdown-box')){
        document.getElementById('my-countdown-box').style.marginRight = "8%";
        document.getElementById('my-countdown-box').style.fontSize = "40px";
    }
    if (document.getElementsByClassName('subscription-card')){
        document.getElementById('golden-subscription-card').style.width = "31%";
        document.getElementById('silver-subscription-card').style.width = "31%";
        document.getElementById('bronze-subscription-card').style.width = "31%";
    }
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    var mybtn = document.querySelector('.side-navbar-btn');
    mybtn.setAttribute('onclick', 'openNav()');
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("user-profile-sidenav").style.marginRight = "0";
    document.getElementById("btn-container").style.display = "block";
    if (document.getElementById('search-form-of-users')){
        document.getElementById('search-form-of-users').style.width = "79%";
    }
    if (document.getElementById('my-countdown-box')){
        document.getElementById('my-countdown-box').style.marginRight = "25%";
        document.getElementById('my-countdown-box').style.fontSize = "50px";
    }
    if (document.getElementsByClassName('subscription-card')){
        document.getElementById('golden-subscription-card').style.width = "31.5%";
        document.getElementById('silver-subscription-card').style.width = "31.5%";
        document.getElementById('bronze-subscription-card').style.width = "31.5%";
    }
}

if (document.querySelector(".edit-pass-container")){
document.querySelector(".edit-pass-container").style.textAlign = "right";
}


function successMessage(){
    alert('گذرواژه با موفقیت تغییر یافت.')
}

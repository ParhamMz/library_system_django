function showFilter(){
    var filter_box = document.querySelector(".search-filters-box");
    filter_box.style.display = "block";
    var is_phone = window.matchMedia("(max-width: 600px)");
    if(is_phone.matches){
        document.getElementById('change-filter').setAttribute('onclick', 'hideFilter()')
    }
}

function hideFilter(){
    var filter_box = document.querySelector(".search-filters-box");
    filter_box.style.display = "none";
}
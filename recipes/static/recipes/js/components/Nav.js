const currentLocation = window.location.pathname;
const class_to_add = 'nav__item_active';

var nav_location = new Map();
nav_location.set("/", "index");
nav_location.set("/subscriptions/", "subscriptions");
nav_location.set("/new/", "new");
nav_location.set("/favorites/", "favorites");
nav_location.set("/basket/", "basket");


const nav_id = nav_location.get(currentLocation);
const nav_for_active = document.getElementById(nav_id);
if (nav_for_active !== null) {
    nav_for_active.classList.add(class_to_add);
}
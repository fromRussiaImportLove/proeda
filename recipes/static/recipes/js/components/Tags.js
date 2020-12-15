const tag_in_url = new URLSearchParams(window.location.search).getAll('tag');
const class_to_add_to_tag = 'tags__active';

var tag_location = new Map();

tag_location.set("?tag=breakfast", "breakfast");
tag_location.set("?tag=lunch", "lunch");
tag_location.set("?tag=dinner", "dinner");


// var url_string = "http://www.example.com/t.html?a=1&b=3&c=m2-m3-m4-m5"; //window.location.href
// var url = new URL(url_string);
// var c = url.searchParams.get("c");
// console.log(c);


const allcheckbox = document.querySelectorAll('.tags__checkbox');
for (var i = 0; i < allcheckbox.length; i++) {
  if (tag_in_url.indexOf(allcheckbox[i].id) > -1) {
  allcheckbox[i].classList.add("tags__checkbox_active");
  }
}

// console.log(tag_in_url.get('tag'))

// const tag_id = tag_location.get(tag_in_url);

// const tag_for_active = document.getElementById(tag_id);
// if (tag_for_active !== null) {
//   tag_for_active.classList.add(class_to_add_to_tag);
//   tag_for_active.href=".";
//   const allcheckbox = document.querySelectorAll('.tags__checkbox');
//   for (var i = 0; i < allcheckbox.length; i++) {
//     if (allcheckbox[i].href.indexOf(tag_in_url) > -1) {
//     allcheckbox[i].href=".";
//     } else {
//     allcheckbox[i].classList.remove("tags__checkbox_active");
//     }
//   }
// }
//

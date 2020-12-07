const tag_in_url = window.location.search;


const class_to_add_to_tag = 'tags__active';

var tag_location = new Map();

tag_location.set("?tag=breakfast", "breakfast");
tag_location.set("?tag=lunch", "lunch");
tag_location.set("?tag=dinner", "dinner");

const tag_id = tag_location.get(tag_in_url);
const tag_for_active = document.getElementById(tag_id);
if (tag_for_active !== null) {
  tag_for_active.classList.add(class_to_add_to_tag);
  console.log(tag_in_url)
  tag_for_active.href=".";
  const allcheckbox = document.querySelectorAll('.tags__checkbox');
  for (var i = 0; i < allcheckbox.length; i++) {
    if (allcheckbox[i].href.indexOf(tag_in_url) > -1) {
    allcheckbox[i].href=".";
    } else {
    allcheckbox[i].classList.remove("tags__checkbox_active");
    }
  }
}


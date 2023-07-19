document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMloaded');

/* Menu shows active page */
const navItems = document.querySelectorAll('nav li a').forEach(link => {
    if (!(link.className == 'dropdown-item' || link.className == 'nav-link active dropdown-toggle' || link.className == 'navbar-brand' || link.className == 'page-link' )) {
    if(link.href == window.location.href) {
    link.classList.add('active');
    }
    }
})


/* Edit post */
document.querySelectorAll('[id^="edit_post_"]').forEach(link => {


    link.onclick = function() {
    name_post = link.id.split('edit_')[1];
    edit_div = document.querySelector('#' + name_post);
    original_text = edit_div.innerText;

    /* press button to edit post */
    if (link.getAttribute("class") == 'fa-regular fa-pen-to-square') {
        link.className = "fa-solid fa-xmark";
        edit_div.innerHTML=`
        <form id='form_${name_post}'>
        <textarea class="form-control" rows='5' style="white-space: pre-wrap" id=textarea_${name_post}>${original_text}</textarea>
        <button type="button" onclick='sendEdit("textarea_" + name_post)' value='put' id='button' class="btn btn-success mt-3">Save</button>
        </form>
    `;

    /* undo editing of the post, return to previous state */
    } else if (link.getAttribute("class") == 'fa-solid fa-xmark')  {
        let id = link.id.split('edit_post_')[1];
        fetch(`/edit/${id}`)
    .then(response => response.json())
    .then(post => {

       const ps = post['content'].split("\n");
  let formattedText = '';
  for (let i = 0; i < ps.length; i++) {
    if (i == ps.length - 1) {
    formattedText += `${ps[i]}`;
    } else {
    formattedText += `${ps[i]}<br>`;
    }
  }
    var my_p = '<p>' + `${formattedText}` + '</p>';
    edit_div.innerHTML=my_p;
    let editButton = document.getElementById("edit_post_" + id);
    editButton.className = 'fa-regular fa-pen-to-square';
    });
    }
}
});

/* Like a post! */
document.querySelectorAll('[id^="like_post_"]').forEach(like => {
    like.onclick = function() {
    post_id = like.id.split('like_post_')[1];
    console.log(post_id);

    fetch(`/like/${post_id}`, {
        method: "PUT",
        headers: {"Content-type": "application/json", "X-CSRFToken": getTokenFromCookie('csrftoken')},
        body: JSON.stringify({
            set_like: true,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result['like_count']);
        let likeCounter = document.getElementById("like_count_post_" + post_id);
        if (result['set_like'] == false) {
            like.style.removeProperty('color');
            like.className = 'fa-regular fa-heart';
            likeCounter.innerHTML= `${result['like_count']}`;
        } else {
        like.style.color = '#a21515';
        like.className = 'fa-solid fa-heart';
        likeCounter.innerHTML= `${result['like_count']}`;
        }
    });
    }
})
})


function getTokenFromCookie(token) {
    const cookie = `; ${document.cookie}`;
    const components = cookie.split(`; ${token}=`);
    if (components.length == 2) return components.pop().split(';').shift();
}


/* Send request to edit post, then change the post itself */
function sendEdit(name_textarea) {
    let editTextareaText = document.getElementById(name_textarea).value;
    let id = name_textarea.split('textarea_post_')[1];
    fetch(`/edit/${id}`, {
        method: "PUT",
        headers: {"Content-type": "application/json", "X-CSRFToken": getTokenFromCookie('csrftoken')},
        body: JSON.stringify({
            content: editTextareaText,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });


   const ps = editTextareaText.split("\n");
  let formattedText = '';
  for (let i = 0; i < ps.length; i++) {
    if (i == ps.length - 1) {
    formattedText += `${ps[i]}`;
    } else {
    formattedText += `${ps[i]}<br>`;
    }
  }

    var my_p = '<p>' + `${formattedText}` + '</p>';
    edit_div.innerHTML=my_p;
    let editButton = document.getElementById("edit_post_" + id);
    editButton.className = 'fa-regular fa-pen-to-square';
}
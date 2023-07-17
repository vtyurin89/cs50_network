document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMloaded');

/* Edit post */
document.querySelectorAll('[id^="edit_post_"]').forEach(link => {

    link.onclick = function() {
    name_post = link.id.split('edit_')[1];
    edit_div = document.querySelector('#' + name_post);
    let original_text = edit_div.innerText;
    if (link.getAttribute("class") == 'fa-regular fa-pen-to-square') {
        link.className = "fa-solid fa-xmark";
        edit_div.innerHTML=`
        <form id='form_${name_post}'>
        <textarea class="form-control" rows='5' style="white-space: pre-wrap" id=textarea_${name_post}>${original_text}</textarea>
        <button type="button" onclick='sendEdit("textarea_" + name_post)' value='put' id='button' class="btn btn-primary mt-3">Save</button>
        </form>
    `;
    } else  {
        original_text = original_text.replace(/\r?\n/g, '<br />');
        edit_div.innerHTML=`${original_text}`;
        link.className = 'fa-regular fa-pen-to-square';
    }

    /* send query */
//    document.querySelector(`#form_${name}`).onsubmit = () => {
//    const editedPost = document.querySelector(`#input_${name}`).value;
//    window.alert(editedPost);
//    }
}
})
})

function getTokenFromCookie(token) {
    const cookie = `; ${document.cookie}`;
    const components = cookie.split(`; ${token}=`);
    if (components.length == 2) return components.pop().split(';').shift();
}

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
    edit_div.innerHTML=editTextareaText;
}
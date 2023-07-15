document.addEventListener('DOMContentLoaded', function() {


/* Edit post */
document.querySelectorAll('[id^="edit_post_"]').forEach(link => {
    link.onclick = function() {
    name = link.id.split('edit_')[1]
    edit_div = document.querySelector('#' + name);
    edit_div.innerHTML=`
            <form id='form_${name}'>
            <textarea class="form-control" rows='5' style="white-space: pre-wrap" id=input_${name}>${edit_div.textContent}</textarea>
            <button type="submit" class="btn btn-primary mt-3">Save</button>
            </form>
    `;
    document.querySelector(`#form_${name}`).onsubmit = () => {
    const editedPost = document.querySelector(`#input_${name}`).value;
    window.alert(editedPost);
    }
}
})


})
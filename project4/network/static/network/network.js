document.addEventListener('DOMContentLoaded', function() {


document.querySelectorAll('[id^="edit_post_"]').forEach(link => {
    link.onclick = function() {
    window.alert('time to edit!');
    }
})
})
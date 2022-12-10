let initialContent
let disabled = false
// Disable warning if submitting a valid form
function onSubmitClicked() {
  if (document.querySelector('.entry-form').checkValidity()) {
    disabled = true;
  }
}

addEventListener('DOMContentLoaded', () => {
  // Save original content to compare to later
  initialContent = document.querySelector('#id_content').value
  // If the server returned an error, assume content is changed as the initial value can no longer be retrieved
  submitFailed = document.querySelector('.errorlist.nonfield')
})

window.addEventListener('beforeunload', function (event) {
  // Warn user before leaving page if any changes were made to the content (edit or new page)
  if ((document.querySelector('#id_content').value != initialContent || submitFailed) && !disabled) {
    event.preventDefault();
  }
});

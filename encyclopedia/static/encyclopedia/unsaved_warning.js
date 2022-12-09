let initialContent

addEventListener('DOMContentLoaded', () => {
  // Save original content to compare to
  initialContent = document.querySelector('#id_content').value
})

window.addEventListener('beforeunload', function (event) {
  // Warn user before leaving page if any changes were made to the content (edit or new page)
  if (content = document.querySelector('#id_content').value != initialContent) {
    event.preventDefault();
  }
});

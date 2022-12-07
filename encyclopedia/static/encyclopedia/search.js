let timeoutID

function search() {
  let searchField = document.querySelector('#dropdown-search')
  let dropdown = document.querySelector('.dropdown-menu')
  // Only send requests if there has been no input for 150
  clearTimeout(timeoutID)
  timeoutID = setTimeout(() => {
    if (searchField.value == '') {
      dropdown.innerHTML = ''
      return
    }
    fetch(`/api/search?q=${searchField.value}`)
    .then((response) => response.json())
    .then((data) => {
      dropdown.innerHTML = ''
      data['results'].slice(0, 5).forEach((entryTitle) => {
        let li = document.createElement('li')
        let link = document.createElement('a')
        // TODO: check if entryTitle can be capitalized and if links with diff capitalization work
        link.setAttribute('href', `/wiki/${entryTitle}`)
        link.classList.add('dropdown-item')
        // Used to help modify bolded parts
        link.setAttribute('data-original', entryTitle)
        li.appendChild(link)
        dropdown.appendChild(li)
        // Update bolded text after changing results
        boldDropdown()
      })
    })
  }, 150)
  // Update bolded text after the query is changed
  boldDropdown()
}

// Adds bold tags to the autocomplete dropdown where the text matches the query
function boldDropdown() {
  document.querySelectorAll('.dropdown-item').forEach((link) => {
    searchField = document.querySelector('.dropdown-toggle')
    link.innerHTML = boldFragment(link.getAttribute('data-original'), searchField.value)
  })
}

// Escape an entire string
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions#escaping
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Adds bold tags wrapping all appearances of fragment in text (case-insensitive)
function boldFragment(text, fragment) {
  reg = new RegExp(escapeRegExp(fragment), 'gi')
  // TODO: change in-line function
  final_str = text.replace(reg, function(str) {return '<b>'+str+'</b>'})
  return final_str
}

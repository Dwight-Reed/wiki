let searchField
let timeoutID
let dropdown

document.addEventListener('DOMContentLoaded', function () {
  searchField = document.querySelector('#myInput')
  dropdown = document.querySelector('.dropdown-menu')
})

function search() {
  // Only send requests if there has been no input for 300ms
  clearTimeout(timeoutID)
  timeoutID = setTimeout(() => {
    console.log(searchField.value)
    if (searchField.value == '') {
      dropdown.innerHTML = ''
      return
    }
    fetch(`/search?q=${searchField.value}`)
    .then((response) => response.json())
    .then((data) => {
      dropdown.innerHTML = ''
      data['results'].slice(0, 5).forEach((entryTitle) => {
        let li = document.createElement('li')
        let link = document.createElement('a')
        // TODO: check if entryTitle can be capitalized and if links with diff capitalization work
        link.setAttribute('href', `/wiki/${entryTitle}`)
        link.classList.add('dropdown-item')
        link.innerHTML = entryTitle
        li.appendChild(link)
        dropdown.appendChild(li)
      })
    })
  }, 300)
}

function focus() {

}

function focusOut() {

}

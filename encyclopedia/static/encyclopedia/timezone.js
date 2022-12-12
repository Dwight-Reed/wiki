addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.date').forEach((element) => {
    let date = new Date(element.innerHTML);
    element.innerHTML = date.toLocaleString();
  });
});

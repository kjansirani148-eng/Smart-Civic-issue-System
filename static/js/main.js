document.addEventListener('DOMContentLoaded', function () {
  const forms = document.querySelectorAll('form');
  forms.forEach((form) => {
    form.noValidate = true;
  });
});

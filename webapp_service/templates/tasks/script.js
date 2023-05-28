function showForm() {
  var form = document.createElement("form");
  form.setAttribute("method", "post");
  form.setAttribute("action", "/server");

  var input = document.createElement("input");
  input.setAttribute("type", "text");
  input.setAttribute("name", "data");
  form.appendChild(input);

  var submit = document.createElement("input");
  submit.setAttribute("type", "submit");
  submit.setAttribute("value", "Отправить");
  form.appendChild(submit);

  var form_container = document.getElementById('form-container');
  form_container.appendChild(form);
}

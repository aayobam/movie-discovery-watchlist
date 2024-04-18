const form = document.getElementById("change-password");
const newPassword = document.getElementById("new-password");
const password = document.getElementById("old-password");
const confirmPassword = document.getElementById("confirm-new-password");

form.addEventListener("submit", (e) => {
  checkInput();
});

function checkInput() {
  // get the values from the inputs
  const passwordValue = password.value.trim();
  const confirmPasswordValue = confirmPassword.value.trim();
  const newPasswordValue = newPassword.value.trim();

  if (passwordValue === "") {
    // show error border color
    setErrorFor(password, "Password cannot be blank");
  } else if (passwordValue.length < 8) {
    setErrorFor(password, "Password must be up to eight characters !");
  } else {
    setSuccessFor(password);
  }

  if (newPasswordValue === "") {
    // show error border color
    setErrorFor(newPassword, "Password cannot be blank");
  } else if (newPasswordValue.length < 8) {
    setErrorFor(newPassword, "Password must be up to eight characters !");
  } else {
    setSuccessFor(newPassword);
  }

  if (confirmPasswordValue === "") {
    // show error border color
    setErrorFor(confirmPassword, "Input cannot be blank");
  } else if (confirmPasswordValue !== newPasswordValue) {
    setErrorFor(confirmPassword, "Password doesn't match");
  } else {
    setSuccessFor(confirmPassword);
  }
}

function setErrorFor(input, message) {
  const formControl = input.parentElement;
  const small = formControl.querySelector("small");
  small.textContent = message;
  small.classList.remove("d-none");
  // add error class
  formControl.classList.add("error");
}
function setSuccessFor(input) {
  const formControl = input.parentElement;
  const small = formControl.querySelector("small");
  small.classList.add("d-none");

  // remove error class
  formControl.classList.remove("error");
  // add success class
  formControl.classList.add("success");
}

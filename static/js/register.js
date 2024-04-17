/* Form vaildation */

const form = document.getElementById("reForm");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm-password");
// const form = document.getElementByid("form");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  checkInput();
});

function checkInput() {
  // get the values from the inputs
  const emailValue = email.value.trim();
  const passwordValue = password.value.trim();
  const confirmPasswordValue = confirmPassword.value.trim();

  if (emailValue === "") {
    setErrorFor(email, "Email cannot be blank");
  } else if (!isEmail(emailValue)) {
    setErrorFor(email, "Email is not valid");
  } else {
    setSuccessFor(email);
  }
  if (passwordValue === "") {
    // show error border color
    setErrorFor(password, "Password cannot be blank");
  } else if (passwordValue.length !== 8) {
    setErrorFor(password, "Password must be up to eight characters !");
  } else {
    setSuccessFor(password);
  }
  if (confirmPasswordValue === "") {
    // show error border color
    setErrorFor(confirmPassword, "Input cannot be blank");
  } else if (confirmPasswordValue !== passwordValue) {
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
function isEmail(email) {
  return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email);
}

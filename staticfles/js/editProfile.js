const form = document.getElementById("edit-profile");
const email = document.getElementById("email");
// const form = document.getElementByid("form");

form.addEventListener("submit", (e) => {
  checkInput();
});

function checkInput() {
  // get the values from the inputs
  const emailValue = email.value.trim();

  if (emailValue === "") {
    setErrorFor(email, "Email cannot be blank");
  } else if (!isEmail(emailValue)) {
    setErrorFor(email, "Email is not valid");
  } else {
    setSuccessFor(email);
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

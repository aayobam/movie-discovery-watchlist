const fav = document.querySelectorAll(".fav");
let isClicked = false;
fav.forEach(function (element) {
  element.addEventListener("click", function () {
    const heart = element.querySelector("i");
    isClicked = !isClicked;
    console.log(isClicked);
    if (isClicked) {
      heart.classList.remove("text-white");
      heart.classList.add("text-danger");
    } else {
      heart.classList.remove("text-danger");
      heart.classList.add("text-white");
    }
  });
});
// console.log(fav);

/* Swiper initialization  */
var swiper = new Swiper(".mySwiper", {
  slidesPerView: 1,
  spaceBetween: 30,
  freeMode: true,
  loop: true,
  autoplay: {
    delay: 4000,
    disableOnInteraction: false,
  },
  breakpoints: {
    500: {
      slidesPerView: 2,
    },
    700: {
      slidesPerView: 3,
    },
    1200: {
      slidesPerView: 4,
    },
  },
});

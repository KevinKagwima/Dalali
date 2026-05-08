const burger = document.querySelector(".burger");
const close_mobile = document.querySelector(".fa-x");
const mobile_nav = document.querySelector(".mobile-navigation");

burger.addEventListener("click", () => {
  mobile_nav.classList.add("show-mobile-navigation");
});

close_mobile.addEventListener("click", () => {
  mobile_nav.classList.remove("show-mobile-navigation");
});

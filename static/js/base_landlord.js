const burger = document.querySelector(".burger");
const close = document.getElementById("close");
const sidebar = document.querySelector(".sidebar");

burger.addEventListener("click", () => {
  sidebar.style.width = "100%";
});

close.addEventListener("click", () => {
  sidebar.style.width = "0";
});

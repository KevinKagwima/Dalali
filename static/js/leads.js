const lead_btn = document.getElementById("lead_btn");
const close_lead_btn = document.querySelector(".fa-x");
const lead_modal = document.getElementById("lead-modal");

lead_btn.addEventListener("click", () => {
  lead_modal.classList.add("active");
});

close_lead_btn.addEventListener("click", () => {
  lead_modal.classList.remove("active");
});

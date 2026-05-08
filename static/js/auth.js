const btn = document.querySelector(".btn");
const inputs = document.querySelectorAll(".name");

btn.addEventListener("click", () => {
  let allInputsFilled = true;

  inputs.forEach((input) => {
    if (!input.value) {
      allInputsFilled = false;
    }
  });

  if (allInputsFilled) {
    btn.disabled = true;
    btn.form.submit();
    // btn.classList.toggle("btn--loading");
  }
});

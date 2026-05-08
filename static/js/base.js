document.addEventListener("DOMContentLoaded", function () {
  // Close button functionality
  document.querySelectorAll(".flash-close").forEach((button) => {
    button.addEventListener("click", function () {
      const message = this.closest(".flash-message");
      message.style.transform = "translateX(100%)";
      message.style.opacity = "0";
      setTimeout(() => message.remove(), 300);
    });
  });

  // Auto-dismiss after 5 seconds
  document.querySelectorAll(".flash-message").forEach((message) => {
    setTimeout(() => {
      message.style.transform = "translateX(100%)";
      message.style.opacity = "0";
      setTimeout(() => message.remove(), 300);
    }, 10000);
  });
});

let slideIndex = 1;

// Initialize the slideshow
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides((slideIndex += n));
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides((slideIndex = n));
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");

  // Handle cycling from last to first and vice versa
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }

  // Hide all slides
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
    slides[i].classList.remove("active");
  }

  // Show the current slide and set active thumbnail
  slides[slideIndex - 1].style.display = "block";
  slides[slideIndex - 1].classList.add("active");
}

document.addEventListener("DOMContentLoaded", function () {
  // Modal elements
  const subscribeModal = document.getElementById("subscribe-modal");
  const paymentModal = document.getElementById("payment-modal");
  const successModal = document.getElementById("success-modal");
  const contactModal = document.getElementById("contact-modal");
  const ratingModal = document.getElementById("rating-modal");
  const bookingModal = document.getElementById("booking-modal");

  // Show subscribe modal when any contact button is clicked
  const subscribeButtons = [document.getElementById("show-subscribe-modal")];

  subscribeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      contactModal.classList.add("active");
    });
  });

  document
    .getElementById("show-rating-modal")
    .addEventListener("click", function () {
      ratingModal.classList.add("active");
    });

  // document
  //   .getElementById("show-visit-modal")
  //   .addEventListener("click", function () {
  //     bookingModal.classList.add("active");
  //   });

  // Close subscribe modal
  document
    .getElementById("close-subscribe-modal")
    .addEventListener("click", function () {
      subscribeModal.classList.remove("active");
    });

  // Process payment button
  document
    .getElementById("process-payment")
    .addEventListener("click", function () {
      subscribeModal.classList.remove("active");
      paymentModal.classList.add("active");

      // Simulate payment processing
      setTimeout(function () {
        paymentModal.classList.remove("active");
        successModal.classList.add("active");
      }, 3000);
    });

  // View contact details button
  document
    .getElementById("view-contact-details")
    .addEventListener("click", function () {
      successModal.classList.remove("active");
      contactModal.classList.add("active");
    });

  // Close contact modal
  document
    .getElementById("close-contact-modal")
    .addEventListener("click", function () {
      contactModal.classList.remove("active");
    });

  // Close modals when clicking outside
  const modals = document.querySelectorAll(".modal-overlay");
  modals.forEach((modal) => {
    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        modal.classList.remove("active");
      }
    });
  });
});

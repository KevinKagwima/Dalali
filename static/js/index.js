document.addEventListener("DOMContentLoaded", function () {
  const navItems = document.querySelectorAll(".user-nav-item");
  const sections = document.querySelectorAll(".user-section");

  // Function to update active nav item
  function updateActiveNav() {
    let currentSection = "";

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;

      if (
        window.scrollY >= sectionTop - 200 &&
        window.scrollY < sectionTop + sectionHeight - 200
      ) {
        currentSection = section.getAttribute("id");
      }
    });

    navItems.forEach((item) => {
      item.classList.remove("active");
      if (item.getAttribute("data-target") === currentSection) {
        item.classList.add("active");
      }
    });
  }

  // Initial call
  updateActiveNav();

  // Update on scroll
  window.addEventListener("scroll", updateActiveNav);

  // Click event for nav items
  navItems.forEach((item) => {
    item.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target");
      const targetSection = document.getElementById(targetId);

      if (targetSection) {
        window.scrollTo({
          top: targetSection.offsetTop - 100,
          behavior: "smooth",
        });
      }
    });
  });
});

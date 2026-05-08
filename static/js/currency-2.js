// Currency conversion setup
const exchangeRate = 2475;

// Get currency selector
const currencySelector = document.getElementById("currencySelector");

// Function to format currency values
function formatCurrency(value, currency) {
  if (currency === "USD") {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(value);
  } else {
    return new Intl.NumberFormat("en-TZ", {
      style: "currency",
      currency: "TZS",
      maximumFractionDigits: 0,
    }).format(value);
  }
}

// Function to convert and update all property prices
function updateAllPrices(selectedCurrency) {
  const priceElements = document.querySelectorAll(".property-price");

  priceElements.forEach((element) => {
    const tshValue = parseFloat(element.getAttribute("data-tsh"));

    if (selectedCurrency === "USD") {
      const usdValue = tshValue / exchangeRate;
      element.textContent = formatCurrency(usdValue, "USD");
    } else {
      element.textContent = formatCurrency(tshValue, "Tsh");
    }
  });

  // Save to localStorage
  localStorage.setItem("preferredCurrency", selectedCurrency);
}

// Initialize currency based on saved preference or default
function initCurrency() {
  const savedCurrency = localStorage.getItem("preferredCurrency");
  if (savedCurrency) {
    currencySelector.value = savedCurrency;
    updateAllPrices(savedCurrency);
  } else {
    // Default to TSH
    updateAllPrices("Tsh");
  }
}

// Event listener for currency change
currencySelector.addEventListener("change", function () {
  updateAllPrices(this.value);
});

// Initialize currency on page load
document.addEventListener("DOMContentLoaded", initCurrency);

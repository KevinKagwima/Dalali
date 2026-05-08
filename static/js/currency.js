// Currency conversion setup
const exchangeRate = 2475; // 1 USD = 2300 TSH

// Elements with currency values
const currencyElements = [
  { element: document.getElementById("mainPrice"), isPrice: true },
];

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

// Function to convert and update currencies
function updateCurrencies(selectedCurrency) {
  currencyElements.forEach((item) => {
    const tshValue = parseFloat(item.element.getAttribute("data-tsh"));

    if (selectedCurrency === "USD") {
      const usdValue = tshValue / exchangeRate;
      item.element.textContent = item.isPrice
        ? formatCurrency(usdValue, "USD")
        : `${formatCurrency(usdValue, "USD")}/year`;
    } else {
      item.element.textContent = item.isPrice
        ? formatCurrency(tshValue, "TSH")
        : `${formatCurrency(tshValue, "TSH")}/year`;
    }
  });

  // Update the exchange rate text
  document.getElementById(
    "exchangeRate"
  ).textContent = `1 USD = ${exchangeRate.toLocaleString()} TSH`;

  // Save to localStorage
  localStorage.setItem("preferredCurrency", selectedCurrency);
}

// Initialize currency based on saved preference or default
function initCurrency() {
  const savedCurrency = localStorage.getItem("preferredCurrency");
  if (savedCurrency) {
    currencySelector.value = savedCurrency;
    updateCurrencies(savedCurrency);
  } else {
    // Default to TSH
    updateCurrencies("TSH");
  }
}

// Event listener for currency change
currencySelector.addEventListener("change", function () {
  updateCurrencies(this.value);
});

// Initialize currency on page load
document.addEventListener("DOMContentLoaded", initCurrency);

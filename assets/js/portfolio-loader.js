document.addEventListener("DOMContentLoaded", function () {
  const container = document.querySelector(".isotope-container");

  if (!container) return;

  // Helper: format price
  function formatPrice(price) {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0
    }).format(price);
  }

  // Helper: check NEW badge
  function isNew(product) {
    if (product.is_new) return true;
    if (!product.date) return false;

    const published = new Date(product.date);
    const today = new Date();
    const diffDays = (today - published) / (1000 * 60 * 60 * 24);
    return diffDays <= 7;
  }

  function renderProduct(product) {
    return `
      <div class="col-lg-4 col-md-6 portfolio-item isotope-item">
        <div class="position-relative">
          <img src="${product.image}" class="img-fluid" alt="${product.name}">
          ${isNew(product) ? `<span class="new-badge">NEW</span>` : ""}
        </div>

        <div class="portfolio-info">
          <h4>${product.name}</h4>
          <p class="price">${formatPrice(product.price)}</p>
          ${product.description ? `<p>${product.description}</p>` : ""}
        </div>
      </div>
    `;
  }

  fetch("/data/products.json")
    .then(res => res.json())
    .then(products => {
      products.forEach(product => {
        container.insertAdjacentHTML("beforeend", renderProduct(product));
      });

      // Init Isotope AFTER products load
      if (window.Isotope) {
        new Isotope(container, {
          itemSelector: ".isotope-item",
          layoutMode: "masonry"
        });
      }
    })
    .catch(err => {
      console.error("Failed to load products:", err);
      container.innerHTML = "<p>Unable to load products.</p>";
    });
});

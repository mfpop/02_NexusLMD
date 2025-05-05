document.addEventListener('DOMContentLoaded', () => {
  const addressContainer = document.getElementById('address-container');
  if (!addressContainer) return;

  const form = addressContainer.querySelector('form');
  const mapIframe = addressContainer.querySelector('iframe');
  const showMapButton = addressContainer.querySelector('button[type="button"]');
  const validationMessage = addressContainer.querySelector('#validation-message');
  const errorMessage = addressContainer.querySelector('#error-message');
  const successMessage = document.createElement('div');
  successMessage.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg transform transition-all duration-300 opacity-0 translate-y-[-100%]';
  successMessage.innerHTML = `
    <div class="flex items-center">
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      <span>Address saved successfully!</span>
    </div>
  `;
  document.body.appendChild(successMessage);

  function showSuccessMessage() {
    successMessage.classList.remove('opacity-0', 'translate-y-[-100%]');
    setTimeout(() => {
      successMessage.classList.add('opacity-0', 'translate-y-[-100%]');
    }, 4000);
  }

  function checkMinimumAddress() {
    const address = form.querySelector('[name="address"]').value.trim();
    const city = form.querySelector('[name="city"]').value.trim();
    const country = form.querySelector('[name="country"]').value.trim();
    return address && city && country;
  }

  function constructFullAddress() {
    const address = form.querySelector('[name="address"]').value.trim();
    const city = form.querySelector('[name="city"]').value.trim();
    const state = form.querySelector('[name="state"]').value.trim();
    const postalCode = form.querySelector('[name="postal_code"]').value.trim();
    const country = form.querySelector('[name="country"]').value.trim();

    let fullAddress = address;
    if (city) fullAddress += `, ${city}`;
    if (state) fullAddress += `, ${state}`;
    if (postalCode) fullAddress += ` ${postalCode}`;
    if (country) fullAddress += `, ${country}`;

    return encodeURIComponent(fullAddress);
  }

  function updateMap() {
    if (!checkMinimumAddress()) {
      if (validationMessage) {
        validationMessage.classList.remove('hidden');
        setTimeout(() => {
          validationMessage.classList.add('hidden');
        }, 3000);
      }
      return;
    }

    const fullAddress = constructFullAddress();
    mapIframe.src = `https://www.openstreetmap.org/export/embed.html?bbox=-180,-90,180,90&amp;layer=mapnik&amp;q=${fullAddress}`;

    // Handle iframe load error
    mapIframe.onerror = () => {
      if (errorMessage) {
        errorMessage.classList.remove('hidden');
        setTimeout(() => {
          errorMessage.classList.add('hidden');
        }, 3000);
      }
    };
  }

  // Handle "Show on Map" button click
  if (showMapButton) {
    showMapButton.addEventListener('click', (e) => {
      e.preventDefault();
      updateMap();
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
      const formData = new FormData(form);
      const response = await fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value
        }
      });

      if (response.ok) {
        showSuccessMessage();
      } else {
        console.error('Failed to save address');
      }
    } catch (error) {
      console.error('Error saving address:', error);
    }
  });

  // Update map when address changes
  form.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', () => {
      // Only update map if the "Show on Map" button was clicked before
      if (mapIframe.src && mapIframe.src !== 'https://www.openstreetmap.org/export/embed.html?bbox=-180,-90,180,90&amp;layer=mapnik') {
        updateMap();
      }
    });
  });
}); 
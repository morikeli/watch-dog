const card = document.querySelector('#map-info-card');
const mapContainer = document.querySelector('.map-container');

// Calculate the adjusted height of the card
const cardHeight = card.offsetHeight; // Get the height of the card
const cardPadding = parseInt(window.getComputedStyle(card).paddingTop) + parseInt(window.getComputedStyle(card).paddingBottom); // Get the padding of the card
const adjustedCardHeight = cardHeight - cardPadding; // Subtract padding from the height

// Set the height of the map container to match the adjusted height of the card
mapContainer.style.height = adjustedCardHeight + 'px';
// Jumbotron slideshow
let slideIndex = 0;
const slides = document.querySelectorAll('#jumbotron-slides img');
const totalSlides = slides.length;

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.toggle('hidden', i !== index);
    });
}

function nextSlide() {
    slideIndex = (slideIndex + 1) % totalSlides;
    showSlide(slideIndex);
}

setInterval(nextSlide, 5000); // Change slide every 5 seconds

// Initialize first slide
showSlide(slideIndex);

// Cart functionality
llet cart = [];

function addToCart(productId, productName, productPrice) {
    const productInCart = cart.find(product => product.id === productId);
    if (productInCart) {
        productInCart.count++;
    } else {
        cart.push({ id: productId, name: productName, price: productPrice, count: 1 });
    }
    updateCartCount();
    updateCartDetails();
}

function updateCartCount() {
    const cartCountElement = document.getElementById('cart-count');
    const totalItems = cart.reduce((sum, product) => sum + product.count, 0);
    cartCountElement.textContent = totalItems;
}

function updateCartDetails() {
    const cartDetailsElement = document.getElementById('cart-details');
    cartDetailsElement.innerHTML = '';
    let totalAmount = 0;

    cart.forEach(product => {
        const productTotal = product.price * product.count;
        totalAmount += productTotal;

        const productElement = document.createElement('div');
        productElement.classList.add('flex', 'justify-between', 'mb-2');
        productElement.innerHTML = `
            <span>${product.name} x ${product.count}</span>
            <span>Rp ${productTotal}</span>
        `;
        cartDetailsElement.appendChild(productElement);
    });

    document.getElementById('total-amount').textContent = totalAmount;
}

function toggleCartModal() {
    const cartModal = document.getElementById('cart-modal');
    cartModal.style.display = (cartModal.style.display === 'none' || cartModal.style.display === '') ? 'block' : 'none';
}

// Initial setup
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('cart-modal').style.display = 'none';
    updateCartCount();
    updateCartDetails();
});

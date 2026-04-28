let cart = [];
let products = [];

// Load products on page load
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    updateCart();
});

// Search products
document.getElementById('searchProducts').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    displayProducts(products.filter(p => 
        p.name.toLowerCase().includes(searchTerm) || 
        p.category.toLowerCase().includes(searchTerm)
    ));
});

// Load products from API
function loadProducts() {
    fetch('/api/products')
        .then(r => r.json())
        .then(data => {
            products = data;
            displayProducts(products);
        });
}

// Display products in UI
function displayProducts(productsToShow) {
    const productsList = document.getElementById('productsList');
    productsList.innerHTML = '';
    
    productsToShow.forEach(product => {
        const div = document.createElement('div');
        div.className = 'product-item';
        div.innerHTML = `
            <div class="product-info">
                <div class="product-name">${product.name}</div>
                <div class="product-category" style="font-size: 12px; color: #999;">${product.category}</div>
                <div class="product-price">₱${product.price.toFixed(2)}</div>
                <div class="product-stock">Stock: ${product.quantity}</div>
            </div>
            <button class="product-btn" ${product.quantity <= 0 ? 'disabled' : ''} onclick="addToCart(${product.id}, '${product.name}', ${product.price})">
                ${product.quantity > 0 ? 'Add' : 'Out of Stock'}
            </button>
        `;
        productsList.appendChild(div);
    });
}

// Add item to cart
function addToCart(productId, productName, price) {
    const existingItem = cart.find(item => item.product_id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            product_id: productId,
            name: productName,
            price: price,
            quantity: 1
        });
    }
    
    updateCart();
}

// Update cart display
function updateCart() {
    const cartItems = document.getElementById('cartItems');
    const itemsCount = document.getElementById('itemsCount');
    const subtotal = document.getElementById('subtotal');
    const total = document.getElementById('total');
    
    cartItems.innerHTML = '';
    
    let totalItems = 0;
    let totalAmount = 0;
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p style="color: #999; text-align: center;">Cart is empty</p>';
    } else {
        cart.forEach((item, index) => {
            const itemTotal = item.price * item.quantity;
            totalItems += item.quantity;
            totalAmount += itemTotal;
            
            const div = document.createElement('div');
            div.className = 'cart-item';
            div.innerHTML = `
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-qty">Qty: 
                        <button style="width: 25px; padding: 2px;" onclick="changeQty(${index}, -1)">-</button>
                        <span style="margin: 0 5px;">${item.quantity}</span>
                        <button style="width: 25px; padding: 2px;" onclick="changeQty(${index}, 1)">+</button>
                    </div>
                </div>
                <div>
                    <div class="cart-item-price">₱${itemTotal.toFixed(2)}</div>
                    <button class="cart-item-remove" onclick="removeFromCart(${index})">Remove</button>
                </div>
            `;
            cartItems.appendChild(div);
        });
    }
    
    itemsCount.textContent = totalItems;
    subtotal.textContent = '₱' + totalAmount.toFixed(2);
    total.textContent = '₱' + totalAmount.toFixed(2);
}

// Change item quantity
function changeQty(index, change) {
    cart[index].quantity += change;
    if (cart[index].quantity <= 0) {
        cart.splice(index, 1);
    }
    updateCart();
}

// Remove item from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
}

// Clear cart
function clearCart() {
    if (confirm('Are you sure you want to clear the cart?')) {
        cart = [];
        updateCart();
    }
}

// Checkout
function checkout() {
    if (cart.length === 0) {
        alert('Cart is empty!');
        return;
    }
    
    const checkoutBtn = document.getElementById('checkoutBtn');
    checkoutBtn.disabled = true;
    checkoutBtn.textContent = 'Processing...';
    
    fetch('/api/checkout', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ items: cart })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert(`Sale completed!\nSale ID: ${data.sale_id}\nTotal: ₱${data.total_amount.toFixed(2)}`);
            cart = [];
            updateCart();
            loadProducts(); // Reload products to update stock
        } else {
            alert('Error: ' + data.error);
        }
        checkoutBtn.disabled = false;
        checkoutBtn.textContent = 'Checkout';
    })
    .catch(err => {
        alert('Error: ' + err);
        checkoutBtn.disabled = false;
        checkoutBtn.textContent = 'Checkout';
    });
}

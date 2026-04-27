const API_URL = 'http://localhost:5000';

// State Management
let state = {
    token: localStorage.getItem('token') || null,
    user: null,
    products: [],
    stock: [],
    cart: []
};

// DOM Elements
const sections = document.querySelectorAll('.view-section');
const navLinks = document.querySelectorAll('.nav-link');
const authBtn = document.getElementById('auth-btn');
const logoutBtn = document.getElementById('logout-btn');
const themeToggle = document.getElementById('theme-toggle');
const adminOnlyElems = document.querySelectorAll('.admin-only');

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    updateAuthUI();
    setupEventListeners();
    setupImageUpload();
    fetchProducts();
    fetchStock();
    fetchInvoices();
});

function setupEventListeners() {
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(e.target.dataset.target);
        });
    });

    document.getElementById('cart-btn').addEventListener('click', () => {
        navigateTo('cart-section');
    });

    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        themeToggle.innerHTML = isDark ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    });

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        state.token = null;
        state.user = null;
        updateAuthUI();
        showToast('Logged out successfully');
        navigateTo('home-section');
    });

    document.getElementById('add-product-form').addEventListener('submit', handleAddProduct);
    document.getElementById('update-stock-form').addEventListener('submit', handleUpdateStock);
    document.getElementById('checkout-btn').addEventListener('click', handleCheckout);
}

function navigateTo(targetId) {
    sections.forEach(sec => sec.classList.add('hidden'));
    document.getElementById(targetId).classList.remove('hidden');

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.dataset.target === targetId) {
            link.classList.add('active');
        }
    });

    if (targetId === 'products-section') {
        console.log('Loading products...');
        fetchProducts();
    }
    if (targetId === 'cart-section') renderCart();
    if (targetId === 'admin-section') {
        fetchProducts();
        fetchStock();
        fetchInvoices();
    }
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.remove('dark-mode');
        themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
    } else {
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
    }
}

function updateAuthUI() {
    if (state.token) {
        authBtn.classList.add('hidden');
        logoutBtn.classList.remove('hidden');
        adminOnlyElems.forEach(el => el.style.display = 'block');
    } else {
        authBtn.classList.remove('hidden');
        logoutBtn.classList.add('hidden');
        adminOnlyElems.forEach(el => el.style.display = 'none');
    }
}

function showToast(message, isError = false) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    if (isError) toast.style.borderLeftColor = '#ff7675';
    toast.innerText = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function openAuthModal() { window.location.href = '/login'; }
function closeAuthModal() {
    const modal = document.getElementById('auth-fullscreen');
    if (modal) modal.classList.add('hidden');
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errBox = document.getElementById('login-error');
    errBox.innerText = '';

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();

        if (!res.ok) throw new Error(data.error || 'Login failed');

        state.token = data.access_token;
        localStorage.setItem('token', data.access_token);
        updateAuthUI();
        closeAuthModal();
        showToast('Successfully logged in');
        document.getElementById('login-form').reset();
    } catch (err) {
        errBox.innerText = err.message;
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const email = document.getElementById('reg-email').value;
    const phone = document.getElementById('reg-phone').value;
    const password = document.getElementById('reg-password').value;
    const errBox = document.getElementById('reg-error');
    errBox.innerText = '';

    try {
        const res = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, phone, password })
        });
        const data = await res.json();

        if (!res.ok) throw new Error(data.error || 'Registration failed');

        showToast('Registration successful! Please login.');
        document.querySelector('[data-form="login-form"]').click();
        document.getElementById('register-form').reset();
    } catch (err) {
        errBox.innerText = err.message;
    }
}

async function apiFetch(endpoint, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (state.token) headers['Authorization'] = `Bearer ${state.token}`;

    const url = endpoint.startsWith('http') ? endpoint : `${API_URL}${endpoint}`;
    const res = await fetch(url, { ...options, headers });
    return res;
}

async function fetchProducts() {
    try {
        console.log('Fetching products...');
        const res = await apiFetch('/products');
        const data = await res.json();
        console.log('Products received:', data);

        if (res.ok && data.data) {
            state.products = data.data;
            console.log('State products updated:', state.products.length);
            renderProducts();
            populateAdminProductSelects();
            renderAdminProducts();
        } else {
            console.error('Failed to fetch products:', data);
        }
    } catch (err) {
        console.error('Failed to load products', err);
        showToast('Failed to load products: ' + err.message, true);
    }
}

async function fetchStock() {
    try {
        const res = await apiFetch('/stock');
        const data = await res.json();
        if (res.ok && data.data) {
            state.stock = data.data;
            renderProducts();
            renderAdminStock();
        }
    } catch (err) { console.error('Failed to load stock', err); }
}

function getProductStock(productId) {
    const s = state.stock.find(st => st.product_id === productId);
    return s ? s.quantity : 0;
}

function renderProducts() {
    const grid = document.getElementById('products-grid');
    if (!grid) return;

    if (state.products.length === 0) {
        grid.innerHTML = '<p class="text-muted">No products found.</p>';
        return;
    }

    grid.innerHTML = '';

    state.products.forEach(p => {
        const stockAmt = getProductStock(p.id);
        grid.innerHTML += `
            <div class="product-card glass-panel">
                ${p.image_url && p.image_url.includes('/static/') ?
                `<img src="${p.image_url}" class="product-image" onerror="this.src='https://placehold.co/400x400?text=No+Image'">` :
                `<div class="product-image" style="background: linear-gradient(135deg, var(--primary), var(--accent)); display: flex; align-items: center; justify-content: center; height: 200px; border-radius: 12px;">
                        <i class="fa-solid fa-image" style="font-size: 3rem; opacity: 0.5;"></i>
                    </div>`
            }
                <div class="category-badge">${p.category || 'Uncategorized'}</div>
                <h3>${p.name}</h3>
                ${p.description ? `<p class="text-muted">${p.description.substring(0, 80)}</p>` : ''}
                <p class="stock">Stock: ${stockAmt}</p>
                <p class="price">$${parseFloat(p.price).toFixed(2)}</p>
                <button class="btn primary-btn" onclick="addToCart(${p.id}, '${p.name}', ${p.price}, ${stockAmt})">
                    Add to Cart
                </button>
            </div>
        `;
    });
}
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function (m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

function populateAdminProductSelects() {
    const select = document.getElementById('stock-product-select');
    if (!select) return;
    select.innerHTML = '<option value="" disabled selected>Select Product</option>';
    state.products.forEach(p => {
        select.innerHTML += `<option value="${p.id}">${p.id} - ${escapeHtml(p.name)}</option>`;
    });
}

async function handleAddProduct(e) {
    e.preventDefault();

    const name = document.getElementById('new-product-name')?.value;
    const price = document.getElementById('new-product-price')?.value;
    const category = document.getElementById('new-product-category')?.value;
    const description = document.getElementById('new-product-description')?.value;
    const imageUrl = document.getElementById('product-image-url')?.value;

    if (!name || !price) {
        showToast('Name and price are required', true);
        return;
    }

    try {
        const res = await apiFetch('/products', {
            method: 'POST',
            body: JSON.stringify({
                name,
                price,
                category: category || 'Uncategorized',
                description: description || '',
                image_url: imageUrl || null
            })
        });

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Failed to add product');
        }

        showToast('Product added successfully!');
        document.getElementById('add-product-form')?.reset();
        document.getElementById('image-preview-container').innerHTML = '';
        document.getElementById('product-image-url').value = '';
        fetchProducts();
        fetchStock();
    } catch (err) {
        showToast(err.message, true);
    }
}

async function handleUpdateStock(e) {
    e.preventDefault();
    const product_id = document.getElementById('stock-product-select')?.value;
    const quantity = document.getElementById('stock-quantity')?.value;

    if (!product_id) {
        showToast('Please select a product', true);
        return;
    }

    try {
        const res = await apiFetch('/stock', {
            method: 'POST',
            body: JSON.stringify({ product_id, quantity })
        });
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.error || 'Failed to update stock');
        }

        showToast('Stock updated successfully!');
        document.getElementById('update-stock-form')?.reset();
        fetchStock();
    } catch (err) {
        showToast(err.message, true);
    }
}

function renderAdminProducts() {
    const list = document.getElementById('admin-product-list');
    if (!list) return;
    list.innerHTML = '';
    state.products.forEach(p => {
        list.innerHTML += `
            <div class="list-item">
                <div>
                    <strong>ID: ${p.id}</strong> - ${escapeHtml(p.name)}
                    <div class="text-muted">Price: $${p.price} | Category: ${escapeHtml(p.category || 'Uncategorized')}</div>
                </div>
            </div>
        `;
    });
}

function renderAdminStock() {
    const list = document.getElementById('admin-stock-list');
    if (!list) return;
    list.innerHTML = '';
    state.stock.forEach(s => {
        list.innerHTML += `
            <div class="list-item">
                <div>
                    <strong>Product ID: ${s.product_id} (${escapeHtml(s.product_name)})</strong>
                    <div class="text-muted">Quantity: ${s.quantity}</div>
                </div>
            </div>
        `;
    });
}

async function uploadProductImage(file) {
    const formData = new FormData();
    formData.append('image', file);

    try {
        const res = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await res.json();
        if (res.ok) {
            return data.image_url;
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    } catch (err) {
        showToast('Image upload failed: ' + err.message, true);
        return null;
    }
}

function setupImageUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('product-image-input');

    if (!uploadArea) return;

    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (ev) {
            const previewContainer = document.getElementById('image-preview-container');
            if (previewContainer) {
                previewContainer.innerHTML = `
                    <div style="position: relative; display: inline-block;">
                        <img src="${ev.target.result}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px; margin-top: 10px;">
                        <button type="button" onclick="removeImage()" style="position: absolute; top: -8px; right: -8px; background: red; color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer;">×</button>
                    </div>
                `;
            }
        };
        reader.readAsDataURL(file);

        showToast('Uploading image...');
        const imageUrl = await uploadProductImage(file);
        if (imageUrl) {
            document.getElementById('product-image-url').value = imageUrl;
            showToast('Image uploaded successfully!');
        }
    });
}

window.removeImage = function () {
    document.getElementById('image-preview-container').innerHTML = '';
    document.getElementById('product-image-url').value = '';
    document.getElementById('product-image-input').value = '';
};

function addToCart(id, name, price, maxStock) {
    const existing = state.cart.find(item => item.productId === id);
    if (existing) {
        if (existing.quantity >= maxStock) {
            showToast('Cannot add more than available stock', true);
            return;
        }
        existing.quantity += 1;
    } else {
        state.cart.push({ productId: id, name, price, quantity: 1, maxStock });
    }

    updateCartUI();
    showToast(`${name} added to cart`);
}

function updateCartUI() {
    const totalItems = state.cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCount = document.getElementById('cart-count');
    if (cartCount) cartCount.innerText = totalItems;

    const cartSection = document.getElementById('cart-section');
    if (cartSection && !cartSection.classList.contains('hidden')) {
        renderCart();
    }
}

function renderCart() {
    const list = document.getElementById('cart-items');
    if (!list) return;
    list.innerHTML = '';

    if (state.cart.length === 0) {
        list.innerHTML = '<p class="empty-state">Your cart is empty.</p>';
        document.getElementById('summary-items').innerText = '0';
        document.getElementById('summary-total').innerText = '$0.00';
        document.getElementById('checkout-btn').disabled = true;
        return;
    }

    document.getElementById('checkout-btn').disabled = false;

    let totals = 0;
    let counts = 0;

    state.cart.forEach(item => {
        counts += item.quantity;
        totals += (item.price * item.quantity);

        const el = document.createElement('div');
        el.className = 'cart-item glass-panel';
        el.innerHTML = `
            <div class="cart-item-details">
                <h4>${escapeHtml(item.name)}</h4>
                <p class="text-muted">$${parseFloat(item.price).toFixed(2)} each</p>
            </div>
            <div class="cart-controls">
                <span>Qty: ${item.quantity}</span>
                <button class="icon-btn" onclick="removeFromCart(${item.productId})"><i class="fa-solid fa-trash"></i></button>
            </div>
        `;
        list.appendChild(el);
    });

    document.getElementById('summary-items').innerText = counts;
    document.getElementById('summary-total').innerText = '$' + totals.toFixed(2);
}

window.removeFromCart = function (id) {
    state.cart = state.cart.filter(item => item.productId !== id);
    updateCartUI();
};

async function handleCheckout() {
    const customerInfo = document.getElementById('customer-info')?.value.trim();
    if (!customerInfo) {
        showToast('Please enter shipping/customer information', true);
        return;
    }

    for (const item of state.cart) {
        try {
            const res = await apiFetch(`/invoice`, {
                method: 'POST',
                body: JSON.stringify({
                    product_id: item.productId,
                    quantity: item.quantity,
                    customer_info: customerInfo
                })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Failed to checkout');
            showToast(`Purchased ${item.name}!`);
        } catch (err) {
            showToast(err.message, true);
        }
    }

    state.cart = [];
    document.getElementById('customer-info').value = '';
    updateCartUI();
    fetchStock();
    fetchInvoices();
}

async function fetchInvoices() {
    try {
        const res = await apiFetch('/invoice');
        const data = await res.json();
        if (res.ok && data.data) {
            renderAdminInvoices(data.data);
        }
    } catch (err) { console.error('Failed to load invoices', err); }
}

function renderAdminInvoices(invoices) {
    const list = document.getElementById('admin-invoice-list');
    if (!list) return;
    list.innerHTML = '';
    invoices.forEach(inv => {
        list.innerHTML += `
            <div class="list-item">
                <div>
                    <strong>Invoice #${inv.id}</strong>
                    <div>Customer: ${escapeHtml(inv.customer_info)}</div>
                    <div class="text-muted">Product: ${escapeHtml(inv.product_name)} | Qty: ${inv.quantity}</div>
                </div>
                <div style="text-align: right">
                    <strong>$${parseFloat(inv.total_amount).toFixed(2)}</strong>
                </div>
            </div>
        `;
    });
}
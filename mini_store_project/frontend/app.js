const API_URL = 'http://localhost:5000';

// State Management
let state = {
    token: localStorage.getItem('token') || null,
    user: null, // we will decode or fetch user later
    products: [],
    stock: [],
    cart: [] // { productId, name, price, quantity }
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
    fetchProducts();
    fetchStock();
    fetchInvoices(); // Admin
});

function setupEventListeners() {
    // Navigation
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(e.target.dataset.target);
        });
    });

    document.getElementById('cart-btn').addEventListener('click', () => {
        navigateTo('cart-section');
    });

    // Theme Toggle
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        themeToggle.innerHTML = isDark ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    });

    // Logout
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        state.token = null;
        state.user = null;
        updateAuthUI();
        showToast('Logged out successfully');
        navigateTo('home-section');
    });

    // Auth Modal
    const closeModalBtn = document.querySelector('.back-link');
    if (closeModalBtn) closeModalBtn.addEventListener('click', closeAuthModal);
    
    // Toggle Password Visibility
    document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.innerHTML = '<i class="fa-regular fa-eye-slash"></i>';
            } else {
                input.type = 'password';
                this.innerHTML = '<i class="fa-regular fa-eye"></i>';
            }
        });
    });
    
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            document.querySelectorAll('.auth-form').forEach(f => f.classList.add('hidden'));
            const formTarget = document.getElementById(e.target.dataset.form);
            if(formTarget) formTarget.classList.remove('hidden');
        });
    });

    // Forms
    const loginForm = document.getElementById('login-form');
    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    
    const registerForm = document.getElementById('register-form');
    if (registerForm) registerForm.addEventListener('submit', handleRegister);
    
    // Admin Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');
            document.getElementById(`tab-${e.target.dataset.tab}`).classList.add('active');
        });
    });

    // Admin Action Forms
    document.getElementById('add-product-form').addEventListener('submit', handleAddProduct);
    document.getElementById('update-stock-form').addEventListener('submit', handleUpdateStock);
    
    // Checkout
    document.getElementById('checkout-btn').addEventListener('click', handleCheckout);
}

// ---- Navigation & UI Update ----
function navigateTo(targetId) {
    sections.forEach(sec => sec.classList.add('hidden'));
    document.getElementById(targetId).classList.remove('hidden');

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.dataset.target === targetId) {
            link.classList.add('active');
        }
    });

    if (targetId === 'products-section') fetchProducts();
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
        adminOnlyElems.forEach(el => el.style.display = 'block'); // Assuming generic user is admin for this dashboard
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
    if (isError) toast.style.borderLeftColor = 'var(--danger)';
    toast.innerText = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function openAuthModal() { window.location.href = 'login.html'; }
function closeAuthModal() { 
    const modal = document.getElementById('auth-fullscreen');
    if(modal) modal.classList.add('hidden'); 
}


// ---- Auth API ----
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
        document.querySelector('[data-form="login-form"]').click(); // switch to login
        document.getElementById('register-form').reset();
    } catch (err) {
        errBox.innerText = err.message;
    }
}

// ==== Helper to safely fetch ====
async function apiFetch(endpoint, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (state.token) headers['Authorization'] = `Bearer ${state.token}`;
    
    // We pass the full URL directly here
    const url = endpoint.startsWith('http') ? endpoint : `${API_URL}${endpoint}`;

    const res = await fetch(url, { ...options, headers });
    return res;
}


// ---- Products & Stock ----
async function fetchProducts() {
    try {
        const res = await apiFetch('/products');
        const data = await res.json();
        if (res.ok && data.data) {
            state.products = data.data;
            renderProducts();
            populateAdminProductSelects();
            renderAdminProducts();
        }
    } catch (err) { console.error('Failed to load products', err); }
}

async function fetchStock() {
    try {
        const res = await apiFetch('/stock');
        const data = await res.json();
        if (res.ok && data.data) {
            state.stock = data.data;
            renderProducts(); // Re-render to show updated stock
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
    grid.innerHTML = '';
    
    if (state.products.length === 0) {
        grid.innerHTML = '<p class="text-muted">No products found.</p>';
        return;
    }

    state.products.forEach(p => {
        const stockAmt = getProductStock(p.id);
        const card = document.createElement('div');
        card.className = 'product-card glass-panel';
        card.innerHTML = `
            <div>
                <h3>${p.name}</h3>
                <p class="stock">Stock Available: ${stockAmt}</p>
                <p class="price">$${parseFloat(p.price).toFixed(2)}</p>
            </div>
            <button class="btn primary-btn ${stockAmt === 0 ? 'outline-btn' : ''}" 
                    onclick="addToCart(${p.id}, '${p.name}', ${p.price}, ${stockAmt})"
                    ${stockAmt === 0 ? 'disabled' : ''}>
                ${stockAmt === 0 ? 'Out of Stock' : 'Add to Cart'}
            </button>
        `;
        grid.appendChild(card);
    });
}

function populateAdminProductSelects() {
    const select = document.getElementById('stock-product-select');
    select.innerHTML = '<option value="" disabled selected>Select Product</option>';
    state.products.forEach(p => {
        select.innerHTML += `<option value="${p.id}">${p.id} - ${p.name}</option>`;
    });
}

async function handleAddProduct(e) {
    e.preventDefault();
    const name = document.getElementById('new-product-name').value;
    const price = document.getElementById('new-product-price').value;

    try {
        const res = await apiFetch('/products', {
            method: 'POST',
            body: JSON.stringify({ name, price })
        });
        if (!res.ok) throw new Error('Failed to add product');
        
        showToast('Product added successfully!');
        document.getElementById('add-product-form').reset();
        fetchProducts(); // refresh
    } catch(err) {
        showToast(err.message, true);
    }
}

async function handleUpdateStock(e) {
    e.preventDefault();
    const product_id = document.getElementById('stock-product-select').value;
    const quantity = document.getElementById('stock-quantity').value;

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
        document.getElementById('update-stock-form').reset();
        fetchStock(); // refresh
    } catch(err) {
        showToast(err.message, true);
    }
}

function renderAdminProducts() {
    const list = document.getElementById('admin-product-list');
    list.innerHTML = '';
    state.products.forEach(p => {
        list.innerHTML += `
            <div class="list-item">
                <div>
                    <strong>ID: ${p.id}</strong> - ${p.name}
                    <div class="text-muted">Price: $${p.price}</div>
                </div>
            </div>
        `;
    });
}

function renderAdminStock() {
    const list = document.getElementById('admin-stock-list');
    list.innerHTML = '';
    state.stock.forEach(s => {
        list.innerHTML += `
            <div class="list-item">
                <div>
                    <strong>Product ID: ${s.product_id} (${s.product_name})</strong>
                    <div class="text-muted">Quantity: ${s.quantity} | Updated at: ${new Date(s.updated_at).toLocaleString()}</div>
                </div>
            </div>
        `;
    });
}


// ---- Cart & Invoice API ----
function addToCart(id, name, price, maxStock) {
    if (!state.token && !confirm("You might need to login to complete checkout. Proceed?")) {
        openAuthModal();
        return;
    }

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
    // Update badge
    const totalItems = state.cart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cart-count').innerText = totalItems;
    if(document.getElementById('cart-section').classList.contains('hidden') === false) {
        renderCart();
    }
}

function renderCart() {
    const list = document.getElementById('cart-items');
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
                <h4>${item.name}</h4>
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

function removeFromCart(id) {
    state.cart = state.cart.filter(item => item.productId !== id);
    updateCartUI();
}

async function handleCheckout() {
    const customerInfo = document.getElementById('customer-info').value.trim();
    if (!customerInfo) {
        showToast('Please enter shipping/customer information', true);
        return;
    }

    if (state.cart.length > 1) {
        // Backend API only accepts one product per invoice currently!
        // We will loop and create multiple invoices or warn them.
        showToast('Processing multiple items as separate invoices...', false);
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
            if(!res.ok) throw new Error(data.error || 'Failed to checkout item ' + item.name);
            
            showToast(`Purchased ${item.name}!`);
        } catch(err) {
            showToast(err.message, true);
        }
    }

    // Clear cart and refresh
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
    } catch(err) { console.error('Failed to load invoices', err); }
}

function renderAdminInvoices(invoices) {
    const list = document.getElementById('admin-invoice-list');
    list.innerHTML = '';
    invoices.forEach(inv => {
        list.innerHTML += `
            <div class="list-item">
                <div>
                    <strong>Invoice #${inv.id}</strong>
                    <div>Customer: ${inv.customer_info}</div>
                    <div class="text-muted">Product ID: ${inv.product_id} (${inv.product_name}) | Qty: ${inv.quantity}</div>
                </div>
                <div style="text-align: right">
                    <strong>$${parseFloat(inv.total_amount).toFixed(2)}</strong>
                    <div class="text-muted" style="font-size: 0.8rem">${new Date(inv.created_at).toLocaleString()}</div>
                </div>
            </div>
        `;
    });
}

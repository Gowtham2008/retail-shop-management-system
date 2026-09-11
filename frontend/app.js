const API = "http://127.0.0.1:8000";


// =============================
// DASHBOARD
// =============================

async function loadDashboard() {

    const productCount = document.getElementById("productCount");

    if (!productCount) {
        return;
    }

    const products = await fetch(`${API}/products`);
    const productData = await products.json();

    const customers = await fetch(`${API}/customers/`);
    const customerData = await customers.json();

    const orders = await fetch(`${API}/orders/`);
    const orderData = await orders.json();

    productCount.textContent = productData.length;

document.getElementById("customerCount").textContent =
    customerData.length;

document.getElementById("orderCount").textContent =
    orderData.length;


let totalSales = 0;

orderData.forEach(order => {

    if (order.status !== "Cancelled") {
        totalSales += order.total_amount;
    }

});

document.getElementById("totalSales").textContent =
    `₹${totalSales.toFixed(2)}`;
}


// =============================
// SHOW PRODUCTS
// =============================

async function loadProducts() {

    const table = document.getElementById("productTable");

    if (!table) {
        return;
    }

    const response = await fetch(`${API}/products`);

    const products = await response.json();

    table.innerHTML = "";

    products.forEach(product => {

        table.innerHTML += `
            <tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>₹${product.price}</td>
                <td>${product.stock_quantity}</td>
                <td>

        <button onclick="editProduct(${product.id})">
            ✏️ Edit
        </button>

        <button
            onclick="addStock(${product.id})"
            style="background:#16a34a; margin-left:8px;">
            ➕ Stock
        </button>

        <button
            onclick="deleteProduct(${product.id})"
            style="background:#dc2626; margin-left:8px;">
            🗑️ Delete
        </button>

    </td>
            </tr>
        `;
    });
}


// =============================
// ADD PRODUCT
// =============================

const productForm = document.getElementById("productForm");

if (productForm) {

    productForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const name = document
            .getElementById("productName")
            .value
            .trim();

        const price = Number(
            document.getElementById("productPrice").value
        );

        if (name.length < 2) {

            alert("Product name must have at least 2 characters.");

            return;
        }

        if (!Number.isFinite(price) || price <= 0) {

            alert("Price must be greater than 0.");

            return;
        }

        const response = await fetch(`${API}/products`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                price: price
            })
        });

        if (response.ok) {

            alert("Product added successfully!");

            productForm.reset();

            loadProducts();

        } else {

            const error = await response.json();

            alert(error.detail || "Failed to add product.");
        }

    });
}


// =============================
// EDIT PRODUCT
// =============================

async function editProduct(id) {

    const name = prompt("Enter new product name:");

    if (name === null) {
        return;
    }

    if (name.trim().length < 2) {

        alert("Name must have at least 2 characters.");

        return;
    }

    const priceInput = prompt("Enter new price:");

    if (priceInput === null) {
        return;
    }

    const price = Number(priceInput);

    if (!Number.isFinite(price) || price <= 0) {

        alert("Price must be greater than 0.");

        return;
    }

    const response = await fetch(`${API}/products/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name: name.trim(),
            price: price
        })
    });

    if (response.ok) {

        alert("Product updated successfully!");

        loadProducts();

    } else {

        alert("Failed to update product.");
    }
}


// =============================
// DELETE PRODUCT
// =============================

async function deleteProduct(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this product?"
    );

    if (!confirmDelete) {
        return;
    }

    const response = await fetch(`${API}/products/${id}`, {

        method: "DELETE"

    });

    if (response.ok) {

        alert("Product deleted successfully!");

        loadProducts();

    } else {

        alert("Failed to delete product.");
    }
}

async function addStock(id) {

    const input = prompt("Enter stock quantity to add:");

    if (input === null) {
        return;
    }

    const quantity = Number(input);

    if (!Number.isInteger(quantity) || quantity <= 0) {

        alert("Stock must be a positive whole number.");

        return;
    }

    const response = await fetch(
        `${API}/products/${id}/stock?quantity=${quantity}`,
        {
            method: "PATCH"
        }
    );

    if (response.ok) {

        const result = await response.json();

        alert(
            `Stock added successfully!\nNew stock: ${result.stock_quantity}`
        );

        loadProducts();

    } else {

        const error = await response.json();

        alert(error.detail || "Failed to add stock.");
    }
}


// =============================
// RUN
// =============================

loadDashboard();

loadProducts();

// =============================
// CUSTOMERS
// =============================

async function loadCustomers() {

    const table = document.getElementById("customerTable");

    if (!table) {
        return;
    }

    const response = await fetch(`${API}/customers/`);

    const customers = await response.json();

    table.innerHTML = "";

    customers.forEach(customer => {

        table.innerHTML += `
            <tr>
                <td>${customer.id}</td>
                <td>${customer.name}</td>
                <td>${customer.phone}</td>
                <td>${customer.email || "-"}</td>
                <td>${customer.address || "-"}</td>
            </tr>
        `;

    });
}


const customerForm = document.getElementById("customerForm");

if (customerForm) {

    customerForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const name =
            document.getElementById("customerName").value.trim();

        const phone =
            document.getElementById("customerPhone").value.trim();

        const email =
            document.getElementById("customerEmail").value.trim();

        const address =
            document.getElementById("customerAddress").value.trim();


        // Name validation

        if (name.length < 2) {

            alert("Name must have at least 2 characters.");

            return;
        }


        // Phone validation

        if (!/^[0-9]{10,15}$/.test(phone)) {

            alert("Phone must contain only 10 to 15 digits.");

            return;
        }


        const response = await fetch(`${API}/customers/`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                name: name,
                phone: phone,
                email: email || null,
                address: address || null

            })
        });


        if (response.ok) {

            alert("Customer added successfully!");

            customerForm.reset();

            loadCustomers();

        } else {

            const error = await response.json();

            alert(error.detail || "Failed to add customer.");

        }

    });
}


loadCustomers();

// =============================
// ORDERS + CART
// =============================

let cart = [];

let allProducts = [];


// Load customers and products
async function loadOrderData() {

    const customerSelect = document.getElementById("customerSelect");
    const productSelect = document.getElementById("productSelect");

    if (!customerSelect || !productSelect) {
        return;
    }


    // Get customers
    const customerResponse = await fetch(`${API}/customers/`);
    const customers = await customerResponse.json();


    customers.forEach(customer => {

        customerSelect.innerHTML += `
            <option value="${customer.id}">
                ${customer.name}
            </option>
        `;

    });


    // Get products
    const productResponse = await fetch(`${API}/products`);
    allProducts = await productResponse.json();


    allProducts.forEach(product => {

        productSelect.innerHTML += `
            <option value="${product.id}">
                ${product.name} - ₹${product.price}
            </option>
        `;

    });
}


// Add product to cart
function addToCart() {

    const productId =
        Number(document.getElementById("productSelect").value);

    const quantity =
        Number(document.getElementById("quantity").value);


    // Validation
    if (!productId) {

        alert("Please select a product.");

        return;
    }


    if (!Number.isInteger(quantity) || quantity <= 0) {

        alert("Quantity must be a positive whole number.");

        return;
    }


    const product = allProducts.find(
        p => p.id === productId
    );


    if (!product) {

        alert("Product not found.");

        return;
    }


    // Check if product already exists in cart
    const existingItem = cart.find(
        item => item.product_id === productId
    );


    if (existingItem) {

        existingItem.quantity += quantity;

    } else {

        cart.push({

            product_id: product.id,

            name: product.name,

            price: product.price,

            quantity: quantity

        });

    }


    displayCart();
}


// Display cart
function displayCart() {

    const table =
        document.getElementById("cartTable");

    const totalElement =
        document.getElementById("cartTotal");


    table.innerHTML = "";

    let total = 0;


    cart.forEach(item => {

        const subtotal =
            item.price * item.quantity;

        total += subtotal;


        table.innerHTML += `
            <tr>

                <td>${item.name}</td>

                <td>${item.quantity}</td>

                <td>₹${item.price}</td>

                <td>₹${subtotal}</td>

            </tr>
        `;

    });


    totalElement.textContent = total.toFixed(2);
}


// Create order
async function createOrder() {

    const customerId =
        Number(document.getElementById("customerSelect").value);


    if (!customerId) {

        alert("Please select a customer.");

        return;
    }


    if (cart.length === 0) {

        alert("Cart is empty.");

        return;
    }


    const orderData = {

        customer_id: customerId,

        items: cart.map(item => ({

            product_id: item.product_id,

            quantity: item.quantity

        }))

    };


    const response = await fetch(`${API}/orders/`, {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(orderData)

    });


    if (response.ok) {

        const order = await response.json();

        alert(
            `Order #${order.id} created successfully!`
        );


        // Empty cart
        cart = [];

        displayCart();

        document.getElementById("customerSelect").value = "";

        document.getElementById("productSelect").value = "";

        document.getElementById("quantity").value = 1;


    } else {

        const error = await response.json();

        alert(
            error.detail || "Failed to create order."
        );

    }

}


// Start order page
loadOrderData();

// =============================
// ORDER HISTORY
// =============================

async function loadOrders() {

    const table = document.getElementById("ordersTable");

    if (!table) {
        return;
    }

    const response = await fetch(`${API}/orders/`);

    const orders = await response.json();

    table.innerHTML = "";

    orders.forEach(order => {

        table.innerHTML += `
            <tr>
                <td>${order.id}</td>
                <td>${order.customer_id}</td>
                <td>${new Date(order.order_date).toLocaleDateString()}</td>
                <td>₹${order.total_amount}</td>
                <td>${order.status}</td>

<td>

    ${
        order.status === "Pending"
        ? `
            <button onclick="completeOrder(${order.id})">
                ✅ Complete
            </button>

            <button
                onclick="cancelOrder(${order.id})"
                style="background:#dc2626; margin-left:8px;">
                ❌ Cancel
            </button>
          `
        : "No Action"
    }

</td>
            </tr>
        `;

    });
}

loadOrders();

async function completeOrder(id) {

    const response = await fetch(
        `${API}/orders/${id}/status`,
        {
            method: "PATCH",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                status: "Completed"
            })
        }
    );

    if (response.ok) {

        alert("Order completed successfully!");

        loadOrders();

    } else {

        const error = await response.json();

        alert(error.detail || "Failed to complete order.");
    }
}
async function cancelOrder(id) {

    const confirmCancel = confirm(
        "Are you sure you want to cancel this order?"
    );

    if (!confirmCancel) {
        return;
    }

    const response = await fetch(
        `${API}/orders/${id}/status`,
        {
            method: "PATCH",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                status: "Cancelled"
            })
        }
    );

    if (response.ok) {

        alert("Order cancelled successfully!");

        loadOrders();

    } else {

        const error = await response.json();

        alert(error.detail || "Failed to cancel order.");
    }
}
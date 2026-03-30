# 🏪 Mini Store Project

A complete **Store Management REST API** built with **Flask + MySQL + SQLAlchemy**.
This project manages products, stock, and invoices for a mini store.

---

## 🚀 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Flask | Web Framework |
| SQLAlchemy | Database ORM / Connector |
| MySQL | Database |
| PyMySQL | MySQL Driver |
| Postman | API Testing |

---

## 📁 Project Structure

```
mini_store_project/
│
├── app.py                        # Main entry point — starts Flask server
│
├── database/
│   └── connection.py             # Creates database engine (connects to MySQL)
│
├── routes/
│   ├── product_route.py          # Product API routes (GET, POST, PUT, DELETE)
│   ├── stock_route.py            # Stock API routes (GET, POST)
│   └── invoice_route.py          # Invoice API routes (GET, POST)
│
├── Tables/
│   ├── product_table.py          # Creates product table in MySQL
│   ├── stock_table.py            # Creates stock table in MySQL
│   └── invoice_table.py          # Creates invoice table in MySQL
│
├── config.py                     # Database URL and configuration
└── README.md                     # Project documentation
```

---

## 🗄️ Database Tables & Relations

```
product                stock                  invoice
───────────────        ───────────────        ───────────────
id (PK)         ←───  product_id (FK)  ←───  product_id (FK)
name                   quantity               quantity
price                  updated_at             total_amount
created_at                                    customer_info
                                              created_at
```

### Relations:
- `stock.product_id` → references `product.id`
- `invoice.product_id` → references `product.id`
- You **cannot** add stock or invoice for a product that does not exist!

---

## ⚙️ Installation & Setup

### Step 1 — Clone the project
```bash
git clone <your-repo-url>
cd mini_store_project
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
```

### Step 3 — Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
pip install flask sqlalchemy pymysql flask-cors
```

### Step 5 — Setup database config
Create a `config.py` file:
```python
DATABASE_URL = "mysql+pymysql://username:password@localhost/mini_store"
```

### Step 6 — Run the server
```bash
python app.py
```

### Step 7 — Server is running!
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

---

## 📡 API Endpoints

### 🛍️ Products

| Method | URL | Description | Body |
|---|---|---|---|
| GET | `/products` | Get all products | None |
| POST | `/products` | Add new product | `{"name": "Apple", "price": 100}` |
| PUT | `/products/<id>` | Update product | `{"name": "Apple", "price": 120}` |
| DELETE | `/products/<id>` | Delete product | None |

### 📦 Stock

| Method | URL | Description | Body |
|---|---|---|---|
| GET | `/stock` | Get all stock | None |
| POST | `/stock` | Add/Update stock | `{"product_id": 1, "quantity": 50}` |

### 🧾 Invoice

| Method | URL | Description | Body |
|---|---|---|---|
| GET | `/invoice` | Get all invoices | None |
| POST | `/invoice` | Create invoice | `{"product_id": 1, "quantity": 10, "customer_info": "Ahmed, Karachi"}` |

### ❤️ Health Check

| Method | URL | Description |
|---|---|---|
| GET | `/health` | Check if server is running |

---

## 📬 Postman Examples

### Add a Product
```json
POST http://127.0.0.1:5000/products
Body (raw JSON):
{
    "name": "Apple",
    "price": 25000
}
```

### Add Stock
```json
POST http://127.0.0.1:5000/stock
Body (raw JSON):
{
    "product_id": 1,
    "quantity": 100
}
```

### Create Invoice
```json
POST http://127.0.0.1:5000/invoice
Body (raw JSON):
{
    "product_id": 1,
    "quantity": 10,
    "customer_info": "Ahmed, Karachi"
}
```

---

## 🔄 Project Flow

```
1. Add a Product    →  POST /products
        ↓
2. Add Stock        →  POST /stock
        ↓
3. Create Invoice   →  POST /invoice
        ↓
4. Stock reduces automatically!
        ↓
5. Invoice saved with total amount!
```

---

## 🧠 Invoice Logic

When a customer places an order:

```
Step 1 → Check product exists
Step 2 → Check stock exists
Step 3 → Check enough stock available
Step 4 → Calculate: total = price × quantity
Step 5 → Reduce stock: new_qty = available - ordered
Step 6 → Save invoice to database
Step 7 → Return success message
```

---

## 📊 Stock Smart Logic (Upsert)

```
POST /stock
    ↓
Does stock exist for this product?
    YES → UPDATE quantity
    NO  → INSERT new row
    ↓
{"message": "Stock Saved"} ✅
```

---

## 🛡️ Error Responses

| Status Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request (missing fields, not enough stock) |
| 404 | Not found (product/stock doesn't exist) |
| 500 | Server error |

---

## 🔮 Future Improvements

- [ ] Add JWT Authentication
- [ ] Add Login/Register routes
- [ ] Add middleware for token validation
- [ ] Add CORS support for frontend
- [ ] Add logging for every request
- [ ] Add pagination for large data
- [ ] Add search and filter for products

---

## 👨‍💻 Author

Built with 💪 and a lot of debugging! 😄

---

## 📝 Notes

- Always activate virtual environment before running
- Make sure MySQL is running before starting Flask
- Add a product first, then stock, then create invoice
- Use Postman to test all API endpoints
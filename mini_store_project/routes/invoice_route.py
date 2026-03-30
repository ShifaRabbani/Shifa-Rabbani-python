import sys
import os
import sqlalchemy as db
from flask import Blueprint , jsonify , request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_engine

invoice_bp = Blueprint("invoice_bp" , __name__, url_prefix='/invoice')

@invoice_bp.route("", methods =['GET'])
def list_invoice():
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(
                db.text(
                """
                SELECT i.id, i.product_id, p.name AS product_name, i.quantity,
                        i.total_amount, i.customer_info, i.created_at
                    FROM invoice i
                    JOIN product p ON p.id = i.product_id
                    ORDER BY i.id
    """
                )
            )
            data = [dict(row._mapping) for row in result]
        return jsonify({"data":data})

@invoice_bp.route("" , methods = ["POST"])
def create_invoice():
    payload = request.get_json(silent=True) or {}
    product_id = payload.get("product_id")
    quantity = payload.get("quantity")
    customer_info = payload.get("customer_info")
    if product_id is None:
        return jsonify({"error":"product_id is required"}), 400
    if quantity is None :
        return jsonify({"error":"quantity is required"}), 400
    
    try:
        order_qty = int(quantity)
    except (TypeError, ValueError):
        return jsonify({"error":"quantity must be integer"}), 400
    
    if order_qty <= 0:
        return jsonify({"error":"quantity must be positive"}), 400
    
    engine = get_engine()
    with engine.begin() as conn:
        # connect with product
        product = conn.execute(
            db.text("SELECT id, price FROM product WHERE id = :product_id"),
            {"product_id": product_id},
        ).first()

        if not product:
            return jsonify({"error":"product not found"}), 404
        # Connect with stock
        stock = conn.execute(
            db.text(
                "SELECT quantity FROM stock "
                "WHERE product_id = :product_id"
            ),
            {"product_id":product_id,}
        ).first()
        if not stock:
            return jsonify({"error":"stock not found for product"}), 404
        
        # now check the stock is available or not or we have less or more etc

        available_qty = int(stock.quantity)
        order_qty = int(quantity)

        if available_qty < order_qty:
            return jsonify({"error":"not enough stock"}), 400
        # count amount
        new_qty = available_qty - order_qty
        total_amount = float(product.price) * order_qty


        conn.execute(
            db.text(
                "UPDATE stock SET quantity = :quantity "
                "WHERE product_id = :product_id"
            ),
            {"quantity" : new_qty, "product_id":product_id},
        )
        
        conn.execute(
            db.text(
                """
                INSERT INTO invoice
                    (product_id, quantity, total_amount, customer_info)
                VALUES (:product_id, :quantity, :total_amount, :customer_info)
                """
            ),
            {
                "product_id": product_id,
                "quantity": order_qty,
                "total_amount": total_amount,
                "customer_info": customer_info
            },
        )

    return jsonify({"message": "Invoice created"}), 201

# postman input
# {
#     "product_id": 1,
#     "quantity": 10,
#     "customer_info": "Ahmed, Karachi"
# }








import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlalchemy as db
from flask import Blueprint , jsonify , request

from database.connection import get_engine

stck_bp = Blueprint("stock_bp" , __name__, url_prefix='/stock')

@stck_bp.route('', methods = ["GET"])
def list_stck():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            db.text(
                # s.id mean stock id ,p : product id is called Alies
                """
                SELECT s.id, s.product_id, p.name AS product_name,
                       s.quantity, s.updated_at
                FROM stock s
                JOIN product p ON p.id = s.product_id
                ORDER BY s.id
                """
                # inner join
            )
        )

        data = [dict(row._mapping) for row in result]
    return jsonify({"data":data})

@stck_bp.route("" , methods = ['POST'])
def add_stock():
    payload = request.get_json(silent=True) or {}   #returns None safely # ✅ Just return None quietly #  If JSON is missing or invalid — don't crash!                                     
    product_id = payload.get("product_id")  
    quantity = payload.get("quantity")

    if product_id is None:
        return jsonify({"error":"Product ID is required"}) , 400
    
    if quantity is None:
        return jsonify({"error":"Quantity is required"}), 400

    engine = get_engine()
    with engine.begin() as conn:
        product_exists = conn.execute(
            db.text("SELECT id FROM product WHERE id = :product_id"),
            {"product_id": product_id},
        ).first()
# first
    # It gets only the first row from the result!
        if not product_exists:
            return jsonify({"error":"Product not found"}), 400
    
        stock_row = conn.execute(
            db.text("SELECT id FROM stock WHERE product_id = :product_id"),
            {"product_id": product_id},
        ).first()
         
        if stock_row:
            conn.execute(
                db.text(
                    "UPDATE stock SET quantity = :quantity "
                    "WHERE product_id = :product_id"
                ),
                {"quantity":quantity, "product_id":product_id},
            )
        else:
            conn.execute(
                db.text(
                    "INSERT INTO stock (product_id, quantity) "
                    "VALUES (:product_id, :quantity)"
                ),
                {"product_id":product_id,"quantity":quantity},
            )

    return jsonify({"message":"Stock Saved"})
# For update the code
# POST {"product_id": 1, "quantity": 100}
# → stock exists → UPDATE ✅



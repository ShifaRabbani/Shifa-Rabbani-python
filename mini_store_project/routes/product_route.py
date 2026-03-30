import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlalchemy as db

from flask import Blueprint , jsonify , request

from database.connection import get_engine

product_bp = Blueprint("product_bp" , __name__ , url_prefix= "/products")
# blueprint is like an map

# url_prefix :means waht is first to show

@product_bp.route('', methods= ['GET'])
def list_produts():
    engine = get_engine()
    with engine.connect() as conn:
    # with = automatically opens and closes your database connection safely — even if an error happens! 
        result = conn.execute(
            db.text(
            "SELECT id, name, price, created_at "
                "FROM product ORDER BY id"
            )
        )
        data = [dict(row._mapping) for row in result]
    return jsonify({"data":data})
# row._mapping  (add column names)
# result` contains all rows from database
# Loop through each row one by one

@product_bp.route("",methods = ['POST'])
def add_product():
    payload = request. get_json(silent=True) or {}
    name = payload.get("name")
    price = payload.get("price")

    if not name:
        return jsonify({"erorr" : "Name is required"}) , 400
    
    if not price:
        return jsonify({"erorr":"price is required"}) , 400
    
    engine = get_engine()
    with engine.begin() as conn:
        # conn and begin are same
        conn.execute(
            db.text(
                "INSERT INTO product (name, price) "
                "VALUES (:name, :price)"
            ),
            {"name":name ,  "price":price}
        )
    return jsonify({"message": "Product added"}) , 201



@product_bp.route("/<int:id>", methods=["DELETE"])
def del_product(id):
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(
            db.text(
                "DELETE FROM product "
                "WHERE id = :id"
            ),
            {"id": id},
        )

    if result.rowcount == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product deleted"}), 200


@product_bp.route("/<int:id>", methods=['PUT'])
def update_product(id):
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    price = payload.get("price")

    if not name:
        return jsonify({"error": "name is required"}), 400

    if price is None:
        return jsonify({"error": "price is required"}), 400

    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(
            db.text(
                "UPDATE product "
                "SET name = :name, price = :price "
                "WHERE id = :id"
            ),
            {"name": name, "price": price, "id": id}
        )

    if result.rowcount == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product updated"}), 200


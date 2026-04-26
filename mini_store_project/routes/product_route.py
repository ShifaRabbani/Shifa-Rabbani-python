import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlalchemy as db
from flask import Blueprint, jsonify, request
from database.connection import get_engine

product_bp = Blueprint("product_bp", __name__, url_prefix="/products")

# Get all products (with images)
@product_bp.route('', methods=['GET'])
def list_products():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            db.text(
                "SELECT id, name, price, image_url, description, category, created_at "
                "FROM product ORDER BY id"
            )
        )
        data = [dict(row._mapping) for row in result]
    
    if not data:
        return jsonify({"data": []})  # Return empty array instead of 404
    
    return jsonify({"data": data})

# Get single product
@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            db.text(
                "SELECT id, name, price, image_url, description, category, created_at "
                "FROM product WHERE id = :id"
            ),
            {"id": id}
        )
        row = result.fetchone()
    
    if not row:
        return jsonify({"error": "Product not found"}), 404
    
    return jsonify(dict(row._mapping))

# Add product (with image support)
@product_bp.route("", methods=['POST'])
def add_product():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    price = payload.get("price")
    image_url = payload.get("image_url")  # New field
    description = payload.get("description", "")  # New field
    category = payload.get("category", "Uncategorized")  # New field

    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    if not price:
        return jsonify({"error": "Price is required"}), 400
    
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            db.text(
                "INSERT INTO product (name, price, image_url, description, category) "
                "VALUES (:name, :price, :image_url, :description, :category)"
            ),
            {
                "name": name, 
                "price": price,
                "image_url": image_url,
                "description": description,
                "category": category
            }
        )
    return jsonify({"message": "Product added"}), 201

# Delete product
@product_bp.route("/<int:id>", methods=["DELETE"])
def del_product(id):
    engine = get_engine()
    with engine.begin() as conn:
        result = conn.execute(
            db.text("DELETE FROM product WHERE id = :id"),
            {"id": id},
        )

    if result.rowcount == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product deleted"}), 200

# Update product (with image support)
@product_bp.route("/<int:id>", methods=['PUT'])
def update_product(id):
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    price = payload.get("price")
    image_url = payload.get("image_url")
    description = payload.get("description")
    category = payload.get("category")

    engine = get_engine()
    
    # Build dynamic update query
    updates = []
    params = {"id": id}
    
    if name is not None:
        updates.append("name = :name")
        params["name"] = name
    if price is not None:
        updates.append("price = :price")
        params["price"] = price
    if image_url is not None:
        updates.append("image_url = :image_url")
        params["image_url"] = image_url
    if description is not None:
        updates.append("description = :description")
        params["description"] = description
    if category is not None:
        updates.append("category = :category")
        params["category"] = category
    
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    
    query = f"UPDATE product SET {', '.join(updates)} WHERE id = :id"
    
    with engine.begin() as conn:
        result = conn.execute(db.text(query), params)

    if result.rowcount == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product updated"}), 200

# Get all categories (for filtering)
@product_bp.route("/categories", methods=['GET'])
def get_categories():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            db.text("SELECT DISTINCT category FROM product WHERE category IS NOT NULL ORDER BY category")
        )
        categories = [row[0] for row in result]
    
    return jsonify({"categories": categories})
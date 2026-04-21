import sqlalchemy as db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_engine

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    phone = payload.get("phone")
    password = payload.get("password")

    if not email:
        return jsonify({"error": "email is required"}), 400
    if not password:
        return jsonify({"error": "password is required"}), 400

    # Hash the password
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    engine = get_engine()
    
    with engine.begin() as conn:
        # Check if email already exists
        existing = conn.execute(
            db.text("SELECT id FROM users WHERE email = :email"), 
            {"email": email}
        ).first()
        
        if existing:
            return jsonify({"error": "email already registered"}), 400
        
        # Insert new user - decode bytes to string for database storage
        conn.execute(
            db.text("INSERT INTO users (email, phone, password) VALUES (:email, :phone, :password)"),
            {
                "email": email, 
                "phone": phone, 
                "password": hashed_pw.decode('utf-8')
            }
        )

    return jsonify({"message": "Registered successfully!"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    password = payload.get("password")

    if not email:
        return jsonify({"error": "email is required"}), 400
    if not password:
        return jsonify({"error": "password is required"}), 400

    engine = get_engine()
    
    with engine.connect() as conn:
        # Get user from database
        user = conn.execute(
            db.text("SELECT id, email, phone, password FROM users WHERE email = :email"),
            {"email": email}
        ).first()
        
        # Check if user exists
        if not user:
            return jsonify({"error": "invalid email or password"}), 401
        
        # Get stored password - convert to bytes if it's a string
        stored_password = user.password
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return jsonify({"error": "invalid email or password"}), 401

    # Create access token
    access_token = create_access_token(identity={
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "login_time": str(datetime.datetime.now())
    })
    
    return jsonify({
        "message": "Login successful", 
        "access_token": access_token
    }), 200


# ==================== GET METHODS ====================

@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    """GET all users (requires authentication)"""
    engine = get_engine()
    with engine.connect() as conn:
        users = conn.execute(
            db.text("SELECT id, email, phone, created_at FROM users")
        ).fetchall()
        
        users_list = []
        for user in users:
            users_list.append({
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
                "created_at": str(user.created_at)
            })
    
    return jsonify({"users": users_list}), 200


@auth_bp.route("/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id):
    """GET single user by ID (requires authentication)"""
    engine = get_engine()
    with engine.connect() as conn:
        user = conn.execute(
            db.text("SELECT id, email, phone, created_at FROM users WHERE id = :id"),
            {"id": user_id}
        ).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "id": user.id,
            "email": user.email,
            "phone": user.phone,
            "created_at": str(user.created_at)
        }), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """GET current user's profile (from token)"""
    current_user = get_jwt_identity()
    
    engine = get_engine()
    with engine.connect() as conn:
        user = conn.execute(
            db.text("SELECT id, email, phone, created_at FROM users WHERE id = :id"),
            {"id": current_user["id"]}
        ).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "id": user.id,
            "email": user.email,
            "phone": user.phone,
            "created_at": str(user.created_at)
        }), 200


@auth_bp.route("/check-email/<email>", methods=["GET"])
def check_email_exists(email):
    """GET check if email exists (no auth required)"""
    engine = get_engine()
    with engine.connect() as conn:
        user = conn.execute(
            db.text("SELECT id FROM users WHERE email = :email"),
            {"email": email}
        ).first()
        
        return jsonify({
            "email": email,
            "exists": user is not None
        }), 200
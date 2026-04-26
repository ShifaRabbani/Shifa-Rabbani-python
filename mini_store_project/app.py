from flask import Flask, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
import uuid

from routes.product_route import product_bp   
from routes.stock_route import stck_bp        
from routes.invoice_route import invoice_bp   
from routes.auth_route import auth_bp

def create_app():
    app = Flask(__name__, static_folder='frontend', static_url_path='/')
    
    # Configure file upload
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config["JWT_SECRET_KEY"] = "mini-store-secret-key-123"
    
    # Create upload folder if it doesn't exist (FIXED)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    CORS(app)
    JWTManager(app)

    @app.route('/')
    def serve_frontend():
        return app.send_static_file('index.html')

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"message": "Server is running 🚀 OK"})

    # File upload endpoint
    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        
        if ext not in allowed_extensions:
            return jsonify({"error": f"File type not allowed"}), 400
        
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        image_url = f"/static/uploads/{filename}"
        return jsonify({"image_url": image_url}), 200

    # Serve uploaded files
    @app.route('/static/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    app.register_blueprint(product_bp)
    app.register_blueprint(stck_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
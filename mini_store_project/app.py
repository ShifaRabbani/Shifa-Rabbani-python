from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from routes.product_route import product_bp   
from routes.stock_route import stck_bp        
from routes.invoice_route import invoice_bp   
from routes.auth_route import auth_bp
from routes.grocery_route import grocery_bp


def create_app():
    app = Flask(__name__, static_folder='frontend', static_url_path='/')
    CORS(app)
    
    app.config["JWT_SECRET_KEY"] = "mini-store-secret-key-123" 
    JWTManager(app)

    @app.route('/')
    def serve_frontend():
        return app.send_static_file('index.html')

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"message": "Server is running 🚀 OK"})  

    app.register_blueprint(product_bp)
    app.register_blueprint(stck_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(grocery_bp)

    return app



app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


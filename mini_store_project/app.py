from flask import Flask, jsonify

from routes.product_route import product_bp
from routes.stock_route import stck_bp
from routes.invoice_route import invoice_bp


def create_app():
    app = Flask(__name__)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"message": "Server is running 🚀 OK"})  # ✅ fixed!

    app.register_blueprint(product_bp)
    app.register_blueprint(stck_bp)
    app.register_blueprint(invoice_bp)

    return app



app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, jsonify

# from routes.product_route import product_bp
# from routes.stock_route import stck_bp
# from routes.invoice_route import invoice_bp


# def create_app():
#     app = Flask(__name__)

#     @app.route('/health', methods=['GET'])
#     def health():
#         return jsonify({"message": "Server is running 🚀 OK"})  # ✅ fixed!

#     app.register_blueprint(product_bp)
#     app.register_blueprint(stck_bp)
#     app.register_blueprint(invoice_bp)

#     return app



# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)







from flask import Flask, render_template
from database.connection import get_engine
from routes.invoice_route import invoice_bp
from routes.product_route import product_bp
from routes.stock_route import stock_bp
import sqlalchemy as db

app = Flask(__name__)

# Register blueprints
app.register_blueprint(invoice_bp)
app.register_blueprint(product_bp)
app.register_blueprint(stock_bp)

# Add this function here
def create_invoice_table(engine):
    with engine.begin() as conn:
        conn.execute(
            db.text(
                """
                CREATE table if not exists invoice(
                id int auto_increment primary key,
                product_id int not null,
                quantity int not null,
                total_amount decimal(10, 2) not null,
                customer_info varchar(255) null,
                created_at timestamp default current_timestamp,
                constraint fk_invoice_product
                foreign key (product_id) references product(id)
                )
                """
            )
        )

# Create tables when app starts
engine = get_engine()
create_invoice_table(engine)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
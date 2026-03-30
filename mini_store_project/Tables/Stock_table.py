import sqlalchemy as db

def create_stock_table(engine):
    with engine.begin() as conn:
        conn.execute(
            db.text(
                """
                CREATE TABLE IF NOT EXISTS stock (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,
                    CONSTRAINT fk_stock_product
                        FOREIGN KEY (product_id) REFERENCES product(id)
                )
                """
            )
        )
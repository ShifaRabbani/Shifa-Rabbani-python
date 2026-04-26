def create_product_table(engine):
    with engine.begin() as conn:
        conn.execute(
            db.text(
                '''
                CREATE TABLE IF NOT EXISTS product (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    image_url VARCHAR(500) DEFAULT NULL,
                    description TEXT DEFAULT NULL,
                    category VARCHAR(100) DEFAULT 'Uncategorized',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                '''
            )
        )
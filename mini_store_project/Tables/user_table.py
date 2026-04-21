import sqlalchemy as db

def create_user_table(engine):
    with engine.begin() as conn:
        conn.execute(db.text(
            """
            CREATE TABLE IF NOT EXISTS users (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                email      VARCHAR(100)  NOT NULL UNIQUE,
                phone      VARCHAR(20),
                password   VARCHAR(255)  NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ))
    print("Users table ready!")

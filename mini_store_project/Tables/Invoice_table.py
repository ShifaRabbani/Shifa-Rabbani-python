import sqlalchemy as db

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
                constraint fk_invice_prodcut
                foreign key (product_id) references product(id)
                )
"""
            )
        )


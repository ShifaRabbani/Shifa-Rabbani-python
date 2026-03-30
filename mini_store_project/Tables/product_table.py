import sqlalchemy as db

def create_product_table(engine):
    with engine.begin() as conn:
        conn.execute(
            db.text(

                '''
                create table if not exists product(
                id int auto_increment primary key,
                name varchar(100) NOT NULL,
                price decimal(10,2) not null,
                created_at TIMESTAMP default current_timestamp
                
                )
'''
            )
        )

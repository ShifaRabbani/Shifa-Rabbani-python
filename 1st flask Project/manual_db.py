import sqlalchemy as db
from sqlalchemy import text
from flask import Flask, jsonify, request

app = Flask(__name__)

database_url = 'mysql+pymysql://root@127.0.0.1:3307/my_database'
engine = db.create_engine(database_url)

conn = engine.connect()
print("Connection to the database was successful!")

# CREATE TABLE FIRST
conn.execute(text("""
    create table if not exists user_registration (
        id int auto_increment,
        full_name varchar(255),
        email varchar(255),
        password varchar(255),
        deprtemnt varchar(100),
        primary key (id)
    )
"""))
print("Table 'user_registration' created successfully")

result = conn.execute(text("SELECT COUNT(*) as count FROM user_registration"))
count = result.fetchone()[0]

# NOW INSERT DATA
conn.execute(text("""
    insert into user_registration (full_name, email, password,deprtemnt) 
    values 
        ('John Doe', 'john.doe@example.com', 'password123',"Computer Science"),
        ('Jane Smith', 'jane.smith@example.com', 'password456','AI'),
        ('Alice Johnson', 'alice.johnson@example.com', 'password789',"literature"),
        ('Bob Brown', 'bob.brown@example.com', 'password101112',"Computer Science"),
        ('Charlie Davis', 'charlie.davis@example.com', 'password131415','literature'),
        ('Eve Wilson', 'eve.wilson@example.com', 'password161718','AI'),
        ('Frank Thomas', 'frank.thomas@example.com', 'password192021',"Computer Science"),
        ('Grace Lee', 'grace.lee@example.com', 'password222324','literature'),
        ('Hank White', 'hank.white@example.com', 'password252627','AI'),
        ('Ivy Harris', 'ivy.harris@example.com', 'password282930','Computer Science')
"""))
conn.commit()
print("Data inserted successfully")

# if __name__ == '__main__':
#     app.run(debug=True)
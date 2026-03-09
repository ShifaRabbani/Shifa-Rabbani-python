import sqlalchemy as db
from flask import Flask, jsonify, request
from sqlalchemy import text, Table, Column, Integer, String, MetaData

app = Flask(__name__)

database_url = 'mysql+pymysql://root@127.0.0.1:3307/my_database'
engine = db.create_engine(database_url)

conn = engine.connect()
print("Connection to the dataBase was succsessfull!")

conn.execute(text("create table if not exists register " \
"(id int auto_increment," \
"full_name varchar(255)," \
"email varchar(255)," \
"password varchar(255)," \
"deprtemnt varchar(255)," \
"primary key (id))"))

print("Table 'register' created successfully")

conn.execute(text("update register set password = 'newpassword123' where id = 1"))
conn.commit()
print("Data updated successfully")


import sqlalchemy as db
database_url = 'mysql+pymysql://root@127.0.0.1:3307/my_database'
engine = db.create_engine(database_url)
metadata = MetaData()

# Define the table structure
register = Table(
    'register', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255)),
    Column('email', String(255)),
    Column('password', String(255)),
    Column('deprtemnt', String(255))

)

# Create the table if it doesn't exist
metadata.create_all(engine)
print("Table 'register' created successfully")

if __name__ == '__main__':
    app.run(debug=True)
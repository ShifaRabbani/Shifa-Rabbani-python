import sqlalchemy as db
from flask import Flask , jsonify , request
from flask import send_file 
from sqlalchemy import text, Table, Column, Integer, String, MetaData


app = Flask(__name__)

databse_url = 'mysql+pymysql://root@127.0.0.1:3307/study_timer_DB'
engine = db.create_engine(databse_url)

conn = engine.connect()
print("connection to the database was successful:")

conn.execute(text('''
    CREATE TABLE IF NOT EXISTS timers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(300),
        minutes INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
'''))
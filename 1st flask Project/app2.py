import sqlalchemy as db
from flask import Flask, jsonify, request

app = Flask(__name__)

database_url = 'mysql+pymysql://root@127.0.0.1:3307/my_database'
engine = db.create_engine(database_url)

conn = engine.connect()

@app.route('/update_password' , methods=["PUT"])
def update_password():
    payload = request.json

    new_password = payload.get('password')
    user_id = payload.get('user_id')

    if conn:
        conn.execute(
            db.text("UPDATE register SET password = :password WHERE user_id = :user_id"),
            {"password": new_password, "user_id": user_id}
        )
        conn.commit()
    return jsonify({"message": f"Password for ID {user_id} updated successfully"})

@app.route('/delete_user', methods= ['DELETE'])
def del_user():
    payload = request.json

    user_id = payload.get('user_id')

    if conn:
        conn.execute  (db.text("DELETE FROM register WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        return jsonify({"Message": f"USer with user_id {user_id} deleted successfully!"})

@app.route('/add_user', methods=['POST'])
def add_user():
    payload = request.json
    username = payload.get('username')
    email = payload.get('email')
    password = payload.get('password')

    if conn:
        conn.execute(
            db.text("insert into register (full_name, email, password) values (:username, :email, :password)"),
            {"username": username, "email": email, "password": password}
        )
        conn.commit()
        
    return jsonify({"message": f"User with username {username} added successfully"})

@app.route('/getdata', methods=['GET'])
def get_data():
    if conn:
        result = conn.execute(db.text("SELECT * FROM register"))
        data = [dict(row._mapping) for row in result]
        return jsonify({"data": data})



if __name__ == '__main__':
    app.run(debug=True)
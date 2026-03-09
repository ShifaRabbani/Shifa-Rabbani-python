import sqlalchemy as db
from flask import Flask , jsonify , request

app = Flask(__name__)

database_url = 'mysql+pymysql://root@127.0.0.1:3307/my_database'
engine = db.create_engine(database_url)

conn = engine.connect()

@app.route("/ghr")
def ghr():
    return 'ghr a gaya'

@app.route('/data_utha_rha_hon',methods=['GET'])
def getting_data():
    if conn:
        query = conn.execute(db.text('SELECT * FROM user_registration'))
        data = [dict(row._mapping)for row in query]
        return jsonify({"Data":data})

@app.route('/data_dal_rha_hon',methods =['POST'])
def add_data():
    if conn:
        payload = request.json
        full_name = payload.get('username')
        email = payload.get("email")
        password = payload.get('password')
        deprtemnt = payload.get('deprtemnt')

        conn.execute(db.text("insert into user_registration (full_name , email ,password,deprtemnt) values (:username, :email, :password ,:deprtemnt)"), {"username" : full_name , 'email' : email ,"password":password , "deprtemnt":deprtemnt})
        conn.commit()
        return jsonify({'message': f'User with username {full_name} added successfully!'})

@app.route('/data_update_kr_rha_hon',methods =['PUT'])
def update_data():
    if conn:
        payload = request.json
        email = payload.get('email')
        password = payload.get('password')  
        deprtemnt = payload.get('deprtemnt')

        conn.execute(db.text("update user_registration set password = :password where email = :email"),{'email':email , 'password':password , 'deprtemnt':deprtemnt})
        conn.commit()
        return jsonify({"message": f"User with email {email} and {deprtemnt} updated successfully"})  # Fixed

@app.route('/data_delete_kr_rha_hon',methods = ['DELETE'])
def del_data():
    if conn:
        payload = request.json
        user_id =payload.get('user_id')

        conn.execute(db.text("DELETE FROM user_registration WHERE id = :user_id"), {"user_id": user_id})
        conn.commit()
        return jsonify({"message": f"User with ID  {user_id} deleted successfully!"})
    

    

if __name__ == "__main__":
    app.run(debug=True)
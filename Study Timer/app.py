import sqlalchemy as db 
from flask import Flask, jsonify, request, send_file
from sqlalchemy import text
from datetime import datetime
import time

app = Flask(__name__)

database_url = 'mysql+pymysql://root@127.0.0.1:3307/study_timer_DB'
engine = db.create_engine(database_url)

# Function to get fresh connection
def get_connection():
    try:
        # Try to ping the connection
        conn.execute(text("SELECT 1"))
        return conn
    except:
        # Reconnect if connection is dead
        return engine.connect()

# Initial connection
conn = engine.connect()
conn.execute(text('USE study_timer_DB'))

# Create table if not exists
conn.execute(text('''
    CREATE TABLE IF NOT EXISTS timers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(300),
        minutes INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
'''))
conn.commit()

@app.route('/')
def home():
    return send_file('index.html')

# GET all timers from database
@app.route('/timers', methods=['GET'])
def get_timers():
    global conn
    try:
        conn = get_connection()
        query = conn.execute(text("SELECT * FROM timers ORDER BY created_at DESC"))
        data = [dict(row._mapping) for row in query]
        return jsonify({"success": True, "data": data})
    except Exception as e:
        print("Error in get_timers:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

# CREATE new timer
@app.route('/create_time', methods=['POST'])
def create_time():
    global conn
    try:
        conn = get_connection()
        data = request.json
        
        name = data["name"]
        minutes = data["minutes"]
        created_at = datetime.now()
        
        query = text("INSERT INTO timers (name, minutes, created_at) VALUES (:name, :minutes, :created_at)")
        
        conn.execute(query, {
            "name": name, 
            "minutes": minutes,
            "created_at": created_at
        })
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": "Timer created"
        })
    except Exception as e:
        print("Error in create_time:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# DELETE timer by ID
@app.route('/del_timer/<int:timer_id>', methods=['DELETE'])
def del_timer(timer_id):
    global conn
    try:
        conn = get_connection()
        
        # Check if timer exists
        check_query = conn.execute(
            text("SELECT id FROM timers WHERE id = :id"), 
            {"id": timer_id}
        )
        if check_query.rowcount == 0:
            return jsonify({"success": False, "error": "Timer not found"}), 404
        
        # Delete timer
        conn.execute(
            text("DELETE FROM timers WHERE id = :id"), 
            {"id": timer_id}
        )
        conn.commit()
        
        return jsonify({
            "success": True, 
            "message": f"Timer {timer_id} deleted successfully"
        })
        
    except Exception as e:
        print("Error in del_timer:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

# UPDATE timer by ID
@app.route('/update_timer/<int:timer_id>', methods=['PUT'])
def update_timer(timer_id):
    global conn
    try:
        conn = get_connection()
        data = request.json
        
        # Check if timer exists
        check_query = conn.execute(
            text("SELECT id FROM timers WHERE id = :id"), 
            {"id": timer_id}
        )
        if check_query.rowcount == 0:
            return jsonify({"success": False, "error": "Timer not found"}), 404
        
        # Update timer
        query = text("UPDATE timers SET name = :name, minutes = :minutes WHERE id = :id")
        
        conn.execute(query, {
            "name": data['name'],
            "minutes": data['minutes'],
            "id": timer_id
        })
        conn.commit()
        
        return jsonify({
            "success": True, 
            "message": "Timer updated successfully"
        })
        
    except Exception as e:
        print("Error in update_timer:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/style.css')
def style():
    return send_file('style.css')

@app.route('/script.js')
def script():
    return send_file('script.js')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
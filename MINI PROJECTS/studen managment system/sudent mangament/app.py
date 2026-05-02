import flask
from flask import request, jsonify
import mysql.connector
from mysql.connector import Error

app = flask.Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': 'sql@123%Shifa',  # Your MySQL password
    'database': 'student_result_db'
}
def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# API Routes for CRUD Operations

@app.route('/api/add_student', methods=['POST'])
def add_student():
    """Create - Add new student"""
    data = request.get_json()
    name = data.get('name')
    marks = data.get('marks')
    
    if not name or marks is None:
        return jsonify({'error': 'Name and marks required'}), 400
    
    result = 'Pass' if int(marks) >= 40 else 'Fail'
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO students (name, marks, result) VALUES (%s, %s, %s)",
                (name, marks, result)
            )
            connection.commit()
            return jsonify({
                'success': True, 
                'message': f'Student {name} added successfully',
                'result': result
            }), 201
        except Error as e:
            return jsonify({'error': f'Student name might already exist: {e}'}), 400
        finally:
            cursor.close()
            connection.close()
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/get_students', methods=['GET'])
def get_students():
    """Read - Get all students"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, marks, result FROM students ORDER BY id")
        students = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(students), 200
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/get_student/<name>', methods=['GET'])
def get_student(name):
    """Read - Get single student by name"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, marks, result FROM students WHERE name = %s", (name,))
        student = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if student:
            return jsonify(student), 200
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/update_student', methods=['PUT'])
def update_student():
    """Update - Modify student marks"""
    data = request.get_json()
    name = data.get('name')
    new_marks = data.get('marks')
    
    if not name or new_marks is None:
        return jsonify({'error': 'Name and new marks required'}), 400
    
    new_result = 'Pass' if int(new_marks) >= 40 else 'Fail'
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET marks = %s, result = %s WHERE name = %s",
            (new_marks, new_result, name)
        )
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({
                'success': True,
                'message': f'Student {name} updated successfully',
                'new_result': new_result
            }), 200
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/delete_student/<name>', methods=['DELETE'])
def delete_student(name):
    """Delete - Remove student"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE name = %s", (name,))
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({'success': True, 'message': f'Student {name} deleted'}), 200
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/')
def home():
    return flask.render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
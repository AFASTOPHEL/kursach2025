import os
import time
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'test')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'pass')

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

while True:
    try:
        conn = get_db_connection()
        conn.close()
        print("База данных доступна!")
        break
    except Exception as e:
        print(f"Ждем базу... {e}")
        time.sleep(3)

@app.route('/')
def api_root():
    return jsonify({
        "status": "system_up",
        "message": "Привет! Это API платформы научных соревнований.",
        "version": "1.0"
    })

@app.route('/competitions', methods=['GET'])
def get_competitions():
    mock_data = [
        {"id": 1, "name": "Хакатон по ИИ", "date": "2025-10-20"},
        {"id": 2, "name": "Робототехника для всех", "date": "2025-11-05"},
        {"id": 3, "name": "Конкурс стартапов МИРЭА", "date": "2025-12-01"}
    ]
    return jsonify(mock_data)

@app.route('/db-check')
def db_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"db_status": "ok", "version": version})
    except Exception as e:
        return jsonify({"db_status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
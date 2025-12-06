import os
import time
import psycopg2
from flask import Flask, jsonify, request # <-- Добавили jsonify (превращает данные в JSON)

app = Flask(__name__)

# Настройки БД
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'test')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'pass')

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

# Ожидание базы (оставляем как было)
while True:
    try:
        conn = get_db_connection()
        conn.close()
        print("База данных доступна!")
        break
    except Exception as e:
        print(f"Ждем базу... {e}")
        time.sleep(3)

# --- МАРШРУТЫ ---

# 1. Главная страница API
# Когда в браузере: http://localhost/api/
@app.route('/')
def api_root():
    return jsonify({
        "status": "system_up",
        "message": "Привет! Это API платформы научных соревнований.",
        "version": "1.0"
    })

# 2. Пример получения данных (Соревнования)
# Когда в браузере: http://localhost/api/competitions
@app.route('/competitions', methods=['GET'])
def get_competitions():
    # Имитация данных (потом тут будет запрос к БД: SELECT * FROM competitions)
    mock_data = [
        {"id": 1, "name": "Хакатон по ИИ", "date": "2025-10-20"},
        {"id": 2, "name": "Робототехника для всех", "date": "2025-11-05"},
        {"id": 3, "name": "Конкурс стартапов МИРЭА", "date": "2025-12-01"}
    ]
    # jsonify превращает список Python в JSON-формат
    return jsonify(mock_data)

# 3. Проверка базы данных
# Когда в браузере: http://localhost/api/db-check
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
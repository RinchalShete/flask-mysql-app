from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    try:
        connection = mysql.connector.connect(
            host='db',          # matches the service name in docker-compose.yml
            user='root',
            password='rootpass',
            database='flaskdb'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 'Connected to MySQL!'")
        result = cursor.fetchone()
        return jsonify({'message': result[0]})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, jsonify
import sqlite3
import config
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
# Enable CORS
CORS(app)

# Connect to SQLite database
conn = sqlite3.connect(config.SQLITE_FILE,check_same_thread=False)
cursor = conn.cursor()

# Define route to get JSON data from SQLite
@app.route('/api/data')
def get_data():
    table_name = config.TABLE_NAME

    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    count = len(data)

    return jsonify({
        'data': data,
        'count': count
    })

if __name__ == '__main__':
    app.run(debug=True)

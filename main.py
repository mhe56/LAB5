from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        );
        ''')
        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print("User table creation failed - ", str(e))
    finally:
        conn.close()

    if __name__ == '__main__':
        create_db_table()
        app.run()


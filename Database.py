import sqlite3

def connect_to_db():
    conn = sqlite3.connect('Users.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        print("User table creation failed -", str(e))
    finally:
        conn.close()

def insert_user(user):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)", 
                    (user['name'], user['email'], user['phone'], user['address'], user['country']))
        conn.commit()
        return get_user_by_id(cur.lastrowid)
    except Exception as e:
        conn.rollback()
        print("Failed to insert user -", str(e))
    finally:
        conn.close()

def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            user = {key: row[key] for key in row.keys()}
            users.append(user)
    except Exception as e:
        print("Failed to fetch users -", str(e))
    finally:
        conn.close()
    return users

def get_user_by_id(user_id):
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            return {key: row[key] for key in row.keys()}
    except Exception as e:
        print("Failed to get user -", str(e))
    finally:
        conn.close()
    return {}

def update_user(user):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?", 
                    (user['name'], user['email'], user['phone'], user['address'], user['country'], user['user_id']))
        conn.commit()
        return get_user_by_id(user['user_id'])
    except Exception as e:
        conn.rollback()
        print("Failed to update user -", str(e))
    finally:
        conn.close()

def delete_user(user_id):
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        return {"status": "User deleted successfully"}
    except Exception as e:
        conn.rollback()
        print("Failed to delete user -", str(e))
        return {"status": "Cannot delete user"}
    finally:
        conn.close()
        
if __name__ == "__main__":
    print("Starting database creation...")
    create_db_table()


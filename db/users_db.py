import sqlite3

from flask import Flask , g
import os



app = Flask("sangeet")



DB_path = os.path.join(os.getcwd() , "Databases" , "users.db")
def get_db_auth():
    if 'auth_db' not in g:
        g.auth_db = sqlite3.connect(DB_path)
        g.auth_db.row_factory = sqlite3.Row
    return g.auth_db





def init_db_auth():
    with app.app_context():
        db = get_db_auth()
        db.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, 
                       name TEXT, 
                       email TEXT UNIQUE, 
                       password TEXT, 
                       profile_pic TEXT, 
                       status TEXT DEFAULT 'pending',
                       otp TEXT,
                       email_verified INTEGER DEFAULT 0)''')
        db.commit()









init_db_auth()






import sqlite3


from flask import Flask , g
import os

app = Flask("sangeet")


DB_path = os.path.join(os.getcwd() , "Databases" , "tokens.db")





def get_token_db():
    if 'token_db' not in g:
        g.token_db = sqlite3.connect(DB_path)
        g.token_db.row_factory = sqlite3.Row
    return g.token_db



def init_token_db():
    with app.app_context():
        db = get_token_db()
        db.execute('''CREATE TABLE IF NOT EXISTS auth_tokens
                      (id INTEGER PRIMARY KEY,
                       user_id INTEGER,
                       token TEXT UNIQUE,
                       expires_at DATETIME,
                       FOREIGN KEY (user_id) REFERENCES users (id))''')
        db.commit()




init_token_db()










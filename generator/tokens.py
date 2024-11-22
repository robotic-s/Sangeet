import secrets
from  db import tokens_db
from db import users_db
from datetime import datetime , timezone , timedelta


from  db import tokens_db

def generate_token():
    return secrets.token_urlsafe(32)


def verify_auth_token(token):
    token_db = tokens_db.get_token_db()
    auth_db = users_db.get_db_auth()
    token_info = token_db.execute('SELECT user_id, expires_at FROM auth_tokens WHERE token = ?', (token,)).fetchone()
    
    if token_info and datetime.fromisoformat(token_info['expires_at']) > datetime.now(timezone.utc):
        user = auth_db.execute('SELECT * FROM users WHERE id = ?', (token_info['user_id'],)).fetchone()
        return user
    return None

def create_auth_token(user_id):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=5)
    db = tokens_db.get_token_db()
    db.execute('INSERT INTO auth_tokens (user_id, token, expires_at) VALUES (?, ?, ?)',
               (user_id, token, expires_at))
    db.commit()
    return token
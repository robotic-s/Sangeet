from cryptography.fernet import Fernet
import base64
import string
import secrets


def generate_key(password):
    return base64.urlsafe_b64encode(password.encode().ljust(32)[:32])

def encrypt(message , PASSWORD):
    key = generate_key(str(PASSWORD))
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def decrypt(encrypted_message , PASSWORD):
    key = generate_key(str(PASSWORD))
    f = Fernet(key)
    return f.decrypt(encrypted_message.encode()).decode()



def generatepass2(length=128):
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    
    # Combine all character sets
    all_characters = lowercase + uppercase + digits + symbols
    
    # Generate password
    password = ''.join(secrets.choice(all_characters) for _ in range(length))
    
    return password


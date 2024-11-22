import os
import json
import base64
import requests
import smtplib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# SMTP server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("mail")  # Replace with your Gmail address in .env file
SMTP_PASSWORD = os.getenv("pass")  # Replace with your app password in .env file
SENDER_EMAIL = SMTP_USERNAME

def encrypt_layer(data: bytes, key: bytes) -> bytes:
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, AES.block_size))

def encrypt_message(message: dict, keys: list[bytes]) -> str:
    encrypted = json.dumps(message).encode()
    for key in keys:
        encrypted = encrypt_layer(encrypted, key)
    return base64.b64encode(encrypted).decode()

def send_mail_request(to: str, subject: str, body: str) -> bool:
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    # Sample message to encrypt
    message = {"data": "Sensitive information"}
    keys = [get_random_bytes(16), get_random_bytes(16)]  # Use two 16-byte keys for encryption layers

    encrypted_message = encrypt_message(message, keys)
    print(f"Encrypted Message: {encrypted_message}")

    # Sending a test email
    success = send_mail_request("recipient@example.com", "Test Subject", "This is a test email.")
    if success:
        print("Email sent successfully.")
    else:
        print("Failed to send email.")

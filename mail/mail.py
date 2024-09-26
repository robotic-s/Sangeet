import requests
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import json
from dotenv import load_dotenv

import os

from dotenv import load_dotenv
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME =   os.getenv("mail")# Replace with your Gmail address
SMTP_PASSWORD = os.getenv("pass")  # Replace with your app password
SENDER_EMAIL = SMTP_USERNAME

load_dotenv()
def encrypt_layer(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, AES.block_size))

def encrypt_message(message, keys):
    encrypted = json.dumps(message).encode()
    for key in keys:
        encrypted = encrypt_layer(encrypted, key)
    return base64.b64encode(encrypted).decode()

def send_mail_request(to, subject, body):
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




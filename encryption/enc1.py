import base64
import hashlib

def enc(input_string, password="lndlcnlkdndl;nldlkneoknfl;kwnwsdno;enfo;ndl;noen"):
    # Convert the string to bytes
    input_bytes = input_string.encode('utf-8')
    
    # Create a key from the password
    key = hashlib.sha256(password.encode('utf-8')).digest()
    
    # XOR each byte of the input with the corresponding byte of the key
    encrypted_bytes = bytes([input_bytes[i] ^ key[i % len(key)] for i in range(len(input_bytes))])
    
    # Encode the result in base64
    encrypted_string = base64.b64encode(encrypted_bytes).decode('utf-8')
    
    return encrypted_string

def dec(encrypted_string, password="lndlcnlkdndl;nldlkneoknfl;kwnwsdno;enfo;ndl;noen"):
    # Decode the base64 string
    encrypted_bytes = base64.b64decode(encrypted_string.encode('utf-8'))
    
    # Create a key from the password
    key = hashlib.sha256(password.encode('utf-8')).digest()
    
    # XOR each byte of the encrypted data with the corresponding byte of the key
    decrypted_bytes = bytes([encrypted_bytes[i] ^ key[i % len(key)] for i in range(len(encrypted_bytes))])
    
    # Convert the result back to a string
    decrypted_string = decrypted_bytes.decode('utf-8')
    
    return decrypted_string


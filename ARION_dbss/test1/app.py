import os
import pandas as pd
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

app = Flask(__name__)

# Path to store encrypted data and token number
STORAGE_PATH = 'storage'
TOKEN_FILE = 'last_token.txt'

if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

# Initialize the last token number
if not os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, 'w') as f:
        f.write('0')

# Generate RSA keys
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Serialize RSA keys
def serialize_keys(private_key, public_key):
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

# Encrypt a symmetric key with the public RSA key
def encrypt_symmetric_key(symmetric_key, public_key):
    encrypted_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

# Decrypt the symmetric key with the private RSA key
def decrypt_symmetric_key(encrypted_key, private_key):
    symmetric_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return symmetric_key

# Encrypt data with the symmetric key
def encrypt_data(data, symmetric_key):
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = iv + encryptor.update(data) + encryptor.finalize()
    return ciphertext

# Decrypt data with the symmetric key
def decrypt_data(ciphertext, symmetric_key):
    backend = default_backend()
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

# Generate a random key
def generate_random_key(length=32):
    return os.urandom(length)

# Generate a sequential token number
def generate_token_number():
    with open(TOKEN_FILE, 'r+') as f:
        last_token = int(f.read())
        new_token = last_token + 1
        f.seek(0)
        f.write(str(new_token))
    return new_token

# Save keys and token numbers to an Excel file
def save_to_excel(data, filename='keys_tokens.xlsx'):
    df = pd.DataFrame(data, columns=['Token Number', 'Key'])
    df.to_excel(filename, index=False)

# Load keys and token numbers from an Excel file
def load_from_excel(filename='keys_tokens.xlsx'):
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        return df
    else:
        return pd.DataFrame(columns=['Token Number', 'Key'])

private_key, public_key = generate_rsa_keys()

@app.route('/encrypt', methods=['POST'])
def encrypt():
    incoming_data = request.json.get('data')
    if not incoming_data:
        return jsonify({'error': 'No data provided'}), 400

    symmetric_key = generate_random_key()
    token_number = generate_token_number()

    encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, public_key)

    data = load_from_excel()
    new_row = pd.DataFrame({'Token Number': [str(token_number)], 'Key': [encrypted_symmetric_key.hex()]})
    data = pd.concat([data, new_row], ignore_index=True)
    save_to_excel(data)

    encrypted_data = encrypt_data(incoming_data.encode(), symmetric_key)

    file_path = os.path.join(STORAGE_PATH, f'{token_number}.enc')
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

    return jsonify({'message': 'Data encrypted', 'token': str(token_number)})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    token_number = request.json.get('token')
    if not token_number:
        return jsonify({'error': 'No token provided'}), 400

    data = load_from_excel()
    row = data[data['Token Number'] == str(token_number)]

    if row.empty:
        return jsonify({'error': 'Invalid token'}), 400

    encrypted_symmetric_key = bytes.fromhex(row.iloc[0]['Key'])
    symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, private_key)

    file_path = os.path.join(STORAGE_PATH, f'{token_number}.enc')
    if not os.path.exists(file_path):
        return jsonify({'error': 'Encrypted file not found'}), 404

    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_data(encrypted_data, symmetric_key)
    return jsonify({'message': 'Data decrypted', 'data': decrypted_data.decode()})

if __name__ == '__main__':
    app.run(debug=True)

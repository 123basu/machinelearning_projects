import os
import pandas as pd
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

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

# Encrypt a file with the symmetric key
def encrypt_file(file_path, symmetric_key):
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = iv + encryptor.update(plaintext) + encryptor.finalize()
    encrypted_file_path = file_path + '.enc'

    with open(encrypted_file_path, 'wb') as f:
        f.write(ciphertext)

    return encrypted_file_path

# Decrypt a file with the symmetric key
def decrypt_file(encrypted_file_path, symmetric_key):
    backend = default_backend()

    with open(encrypted_file_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    decrypted_file_path = encrypted_file_path.replace('.enc', '.dec')

    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)

    return decrypted_file_path

# Generate a random key
def generate_random_key(length=32):
    return os.urandom(length)

# Generate a token number
def generate_token_number():
    return uuid.uuid4()

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

def main():
    # Generate RSA keys
    private_key, public_key = generate_rsa_keys()
    private_pem, public_pem = serialize_keys(private_key, public_key)

    print("Private Key:")
    print(private_pem.decode('utf-8'))
    print("\nPublic Key:")
    print(public_pem.decode('utf-8'))

    while True:
        choice = input("Enter 'e' to encrypt a file or 'd' to decrypt a file: ").lower()
        if choice == 'e':
            # Generate a random symmetric key
            symmetric_key = generate_random_key()
            token_number = generate_token_number()

            # Encrypt the symmetric key with the RSA public key
            encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, public_key)

            # Save the token number and encrypted symmetric key to an Excel file
            data = load_from_excel()
            new_row = pd.DataFrame({'Token Number': [str(token_number)], 'Key': [encrypted_symmetric_key.hex()]})
            data = pd.concat([data, new_row], ignore_index=True)
            save_to_excel(data)

            # Get the file path to encrypt
            file_path = input("Enter the path of the file to encrypt: ")
            encrypted_file_path = encrypt_file(file_path, symmetric_key)
            print(f"\nEncrypted file saved to: {encrypted_file_path}")

        elif choice == 'd':
            # Load keys and token numbers from the Excel file
            data = load_from_excel()

            # Get the token number from the user
            token_number = input("Enter the token number: ")
            row = data[data['Token Number'] == token_number]

            if not row.empty:
                # Get the encrypted symmetric key from the Excel file
                encrypted_symmetric_key = bytes.fromhex(row.iloc[0]['Key'])

                # Decrypt the symmetric key with the RSA private key
                symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, private_key)

                # Get the file path to decrypt
                encrypted_file_path = input("Enter the path of the file to decrypt: ")
                decrypted_file_path = decrypt_file(encrypted_file_path, symmetric_key)
                print(f"\nDecrypted file saved to: {decrypted_file_path}")
            else:
                print("Invalid token number. Please try again.")
        else:
            print("Invalid choice. Please enter 'e' to encrypt or 'd' to decrypt.")

if __name__ == "__main__":
    main()

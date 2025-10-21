import os
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

# Main function to handle user input and perform encryption/decryption
def main():
    private_key, public_key = generate_rsa_keys()
    private_pem, public_pem = serialize_keys(private_key, public_key)

    print("Private Key:")
    print(private_pem.decode('utf-8'))
    print("\nPublic Key:")
    print(public_pem.decode('utf-8'))

    symmetric_key = os.urandom(32)
    encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, public_key)

    file_path = input("Enter the path of the file to encrypt: ")

    encrypted_file_path = encrypt_file(file_path, symmetric_key)
    print(f"\nEncrypted file saved to: {encrypted_file_path}")

    decrypted_symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, private_key)
    decrypted_file_path = decrypt_file(encrypted_file_path, decrypted_symmetric_key)
    print(f"\nDecrypted file saved to: {decrypted_file_path}")

if __name__ == "__main__":
    main()

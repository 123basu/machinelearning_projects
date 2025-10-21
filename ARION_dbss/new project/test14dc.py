import pandas as pd
import os

# Step 1: Ask for the encrypted data with the public key
def get_encrypted_data():
    while True:
        encrypted_data_with_key = input("Enter the encrypted data with the public key: ")
        if ',' in encrypted_data_with_key:
            return encrypted_data_with_key
        else:
            print("Invalid input. Please enter the encrypted data with the public key.")

# Step 2: Ask for the token number
def get_token_number():
    while True:
        token_number = input("Enter the token number: ")
        if token_number.isdigit():
            return int(token_number)
        else:
            print("Invalid input. Please enter a valid token number.")

# Retrieve the encrypted data and token number
encrypted_data_with_key = get_encrypted_data()
token_number = get_token_number()
parts = encrypted_data_with_key.split(',')
combined_encrypted = parts[0]
lengths = list(map(int, parts[1:5]))
public_key = int(parts[5])

print(f"Combined encrypted data: {combined_encrypted}")
print(f"Lengths: {lengths}")
print(f"Public key: {public_key}")
print(f"Token number: {token_number}")

# Extract lengths of encrypted parts
len_a, len_b, len_c, len_d = lengths

# Extract encrypted parts using lengths
start = 0
encrypted_a = int(combined_encrypted[start:start + len_a])
start += len_a
encrypted_b = int(combined_encrypted[start:start + len_b])
start += len_b
encrypted_c = int(combined_encrypted[start:start + len_c])
start += len_c
encrypted_d = int(combined_encrypted[start:start + len_d])

print(f"Encrypted data parts: {encrypted_a}, {encrypted_b}, {encrypted_c}, {encrypted_d}")

# Step 3: Verify the token number and public key against the Excel sheet
if not os.path.exists('keys.xlsx'):
    print("keys.xlsx file not found. Exiting.")
    exit()

df = pd.read_excel('keys.xlsx')

# Verify token number and public key
if token_number in df['Token Number'].values:
    row = df.loc[df['Token Number'] == token_number]
    if public_key == row['Public Key'].values[0]:
        private_key = row['Private Key'].values[0]
        print(f"Retrieved private key: {private_key}")
    else:
        print("Public key verification failed.")
        exit()
else:
    print("Token number verification failed.")
    exit()

# Step 4: Reverse the mathematical operations to get the original parts
n = 1000  # Match the modulus used in encryption

decrypted_a = (encrypted_a - n**4) // private_key**4
decrypted_b = (encrypted_b - n**3) // private_key**3
decrypted_c = (encrypted_c - n**2) // private_key**2
decrypted_d = (encrypted_d - n)

# Ensure the decrypted parts are integers
decrypted_a = int(decrypted_a)
decrypted_b = int(decrypted_b)
decrypted_c = int(decrypted_c)
decrypted_d = int(decrypted_d)

# Combine the decrypted parts to form the original 16-digit number
decrypted_message = f"{decrypted_a:04d}{decrypted_b:04d}{decrypted_c:04d}{decrypted_d:04d}"
print(f"Decrypted message: {decrypted_message}")

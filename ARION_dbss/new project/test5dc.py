import pandas as pd

# Step 1: Ask for the encrypted data
def get_encrypted_data():
    while True:
        encrypted_data_with_key = input("Enter the encrypted data with the public key: ")
        if ',' in encrypted_data_with_key:
            return encrypted_data_with_key
        else:
            print("Invalid input. Please enter the encrypted data with the public key.")

encrypted_data_with_key = get_encrypted_data()
public_key = int(encrypted_data_with_key.split(',')[-1])
encrypted_data_parts = encrypted_data_with_key.rsplit(',', 5)[:-1]  # Get all parts except the last part

print(f"Encrypted data parts: {encrypted_data_parts}")
print(f"Public key: {public_key}")

# Step 2: Verify the public key against the Excel sheet
df = pd.read_excel('keys.xlsx')

if public_key in df['Public Key'].values:
    private_key = df.loc[df['Public Key'] == public_key, 'Private Key'].values[0]
    print(f"Retrieved private key: {private_key}")
else:
    print("Public key verification failed.")
    exit()

# Step 4: Decrypt the data using the private key
encrypted_a, encrypted_b, encrypted_c, encrypted_d = map(int, encrypted_data_parts)

# Reverse the mathematical operations to get the original parts
decrypted_a = encrypted_a // private_key**4
decrypted_b = encrypted_b // private_key**3
decrypted_c = encrypted_c // private_key**2
decrypted_d = encrypted_d // private_key

# Combine the decrypted parts to form the original 16-digit number
decrypted_message = f"{int(decrypted_a):04d}{int(decrypted_b):04d}{int(decrypted_c):04d}{int(decrypted_d):04d}"
print(f"Decrypted message: {decrypted_message}")



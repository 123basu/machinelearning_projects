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
parts = encrypted_data_with_key.split(',')
combined_encrypted = parts[0]
public_key = int(parts[1])
lengths = list(map(int, parts[2:]))

print(f"Combined encrypted data: {combined_encrypted}")
print(f"Public key: {public_key}")
print(f"Lengths: {lengths}")

# Step 2: Verify the public key against the Excel sheet
df = pd.read_excel('keys.xlsx')

if public_key in df['Public Key'].values:
    private_key = df.loc[df['Public Key'] == public_key, 'Private Key'].values[0]
    print(f"Retrieved private key: {private_key}")
else:
    print("Public key verification failed.")
    exit()

# Extract encrypted parts using lengths
start = 0
encrypted_a = float(combined_encrypted[start:start + lengths[0]])
start += lengths[0]
encrypted_b = float(combined_encrypted[start:start + lengths[1]])
start += lengths[1]
encrypted_c = float(combined_encrypted[start:start + lengths[2]])
start += lengths[2]
encrypted_d = float(combined_encrypted[start:start + lengths[3]])

# Reverse the mathematical operations to get the original parts
n = 1000  # Match the modulus used in encryption

decrypted_a = int(((encrypted_a * 1000) - n**4) / private_key**4)
decrypted_b = int(((encrypted_b * 1000) - n**3) / private_key**3)
decrypted_c = int(((encrypted_c * 1000) - n**2) / private_key**2)
decrypted_d = int(((encrypted_d * 1000) - n))

# Combine the decrypted parts to form the original 16-digit number
decrypted_message = f"{decrypted_a:04d}{decrypted_b:04d}{decrypted_c:04d}{decrypted_d:04d}"
print(f"Decrypted message: {decrypted_message}")



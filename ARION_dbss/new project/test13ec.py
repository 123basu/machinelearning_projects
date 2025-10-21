






import random
import pandas as pd
import os

# Step 1: Ask for a 16-digit number
def get_input_number():
    while True:
        number = input("Enter a 16-digit number: ")
        if len(number) == 16 and number.isdigit():
            return number
        else:
            print("Invalid input. Please enter a 16-digit number.")

number = get_input_number()

# Step 2: Break the 16-digit number into 4 parts
a = int(number[:4])
b = int(number[4:8])
c = int(number[8:12])
d = int(number[12:])

print(f"Parts: a={a}, b={b}, c={c}, d={d}")

# Step 3: Generate a random 16-bit private key and 16-bit public key
private_key = random.getrandbits(16)
public_key = random.getrandbits(16)
token_number = random.randint(100000, 999999)

print(f"Generated private key: {private_key}")
print(f"Generated public key: {public_key}")
print(f"Generated token number: {token_number}")

# Step 4: Apply the encryption algorithm
n = 1000
encrypted_a = (n**4 + a * private_key**4)
encrypted_b = (n**3 + b * private_key**3)
encrypted_c = (n**2 + c * private_key**2)
encrypted_d = (n + d)

# Convert encrypted parts to strings
encrypted_a_str = str(encrypted_a)
encrypted_b_str = str(encrypted_b)
encrypted_c_str = str(encrypted_c)
encrypted_d_str = str(encrypted_d)

# Get lengths of encrypted parts
len_a = len(encrypted_a_str)
len_b = len(encrypted_b_str)
len_c = len(encrypted_c_str)
len_d = len(encrypted_d_str)

# Combine encrypted parts into a single string
combined_encrypted = encrypted_a_str + encrypted_b_str + encrypted_c_str + encrypted_d_str

# Step 5: Create the final encrypted data string with lengths, public key, and token number
encrypted_data_with_key = f"{combined_encrypted},{len_a},{len_b},{len_c},{len_d},{public_key},{token_number}"

print(f"Encrypted data with public key and token: {encrypted_data_with_key}")

# Save the keys and token to an Excel file
data = {
    'Token Number': [token_number],
    'Private Key': [private_key],
    'Public Key': [public_key]
}

file_exists = os.path.exists('keys.xlsx')
df = pd.DataFrame(data)

if file_exists:
    df_existing = pd.read_excel('keys.xlsx')
    df = pd.concat([df_existing, df], ignore_index=True)

df.to_excel('keys.xlsx', index=False)

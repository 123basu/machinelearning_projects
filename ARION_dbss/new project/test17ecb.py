import random
import pandas as pd
import os

# Load the symbols and letters dataset
file_path = r'C:\Users\Kunaal\OneDrive\Documents\Desktop\All the folders\6 sem mini project\numbers_letters_dataset.xlsx'
data = pd.read_excel(file_path)

# Create a map for numbers to symbols
number_to_symbols = {}
for _, row in data.iterrows():
    number = row['number']
    symbols = row[1:].dropna().tolist()
    number_to_symbols[number] = symbols

def map_number_to_symbol(number):
    symbols = number_to_symbols[int(number)]
    return random.choice(symbols)

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

# Step 3: Generate a random 64-bit private key and store it in an Excel file
private_key = random.getrandbits(16)
public_key = random.getrandbits(16)
token_number = random.randint(100000, 999999)

# Create a DataFrame to store keys
data = {
    'Token Number': [token_number],
    'Private Key': [private_key],
    'Public Key': [public_key]
}

# Check if the Excel file exists
keys_file_path = r'C:\Users\Kunaal\OneDrive\Documents\Desktop\All the folders\6 sem mini project\keys.xlsx'
file_exists = os.path.exists(keys_file_path)

# Save to Excel
df = pd.DataFrame(data)
if file_exists:
    df_existing = pd.read_excel(keys_file_path)
    df = pd.concat([df_existing, df], ignore_index=True)
df.to_excel(keys_file_path, index=False)

print(f"Generated private key: {private_key}")
print(f"Generated public key: {public_key}")
print(f"Generated token number: {token_number}")

# Step 4: Apply the enhanced encryption equation
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
public_key_str = str(public_key)

# Get lengths of encrypted parts and public key
len_a = len(encrypted_a_str)
len_b = len(encrypted_b_str)
len_c = len(encrypted_c_str)
len_d = len(encrypted_d_str)
len_pk = len(public_key_str)

# Combine encrypted parts into a single string
combined_encrypted = encrypted_a_str + encrypted_b_str + encrypted_c_str + encrypted_d_str

# Step 5: Map each digit to a random symbol
encrypted_with_symbols = ' '.join(map_number_to_symbol(int(digit)) for digit in combined_encrypted)
lengths_with_symbols = ' '.join(map_number_to_symbol(int(digit)) for digit in f"{len_a:02}{len_b:02}{len_c:02}{len_d:02}")
public_key_with_symbols = ' '.join(map_number_to_symbol(int(digit)) for digit in public_key_str)

# Create the final encrypted data string
encrypted_data_with_key = f"{encrypted_with_symbols},{lengths_with_symbols},{public_key_with_symbols},{token_number}"

print(f"Encrypted data with public key and token: {encrypted_data_with_key}")
 



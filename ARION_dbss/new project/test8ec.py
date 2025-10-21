import random
import pandas as pd
import openpyxl

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

# Step 3: Generate a random private key and store it in an Excel file
private_key = random.randint(1000, 9999)

# Step 5: Generate a random public key
public_key = random.randint(1000000, 9999999)

# Create a DataFrame to store keys
data = {
    'Private Key': [private_key],
    'Public Key': [public_key]
}

# Save to Excel
df = pd.DataFrame(data)
df.to_excel('keys.xlsx', index=False)

print(f"Generated private key: {private_key}")
print(f"Generated public key: {public_key}")

# Step 4: Apply the enhanced encryption equation
n = 1000
encrypted_a = (n**4 + a * private_key**4) / 1000
encrypted_b = (n**3 + b * private_key**3) / 1000
encrypted_c = (n**2 + c * private_key**2) / 1000
encrypted_d = (n + d) / 1000

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

# Step 5: Create the final encrypted data string
encrypted_data_with_key = f"{combined_encrypted},{public_key},{len_a},{len_b},{len_c},{len_d}"

print(f"Encrypted data with public key: {encrypted_data_with_key}")
